#Copyright IBM Corp. 2018.
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#http://www.apache.org/licenses/LICENSE-2.0
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

import ConfigParser
import getopt
import os
import socket
import sys
import traceback
import unittest

from rest_framework import keystoneUtils, log, test_runner_utility


def end_with_separator(pathstring):
    """Ensure that non-empty path ends with a separator character."""
    if (len(pathstring) > 0 and not pathstring.endswith(os.sep)):
        return pathstring + os.sep
    else:
        return pathstring

CONFIG_DEFAULT_PATH = end_with_separator('svt_config/config_13Q4_PVC_V1.2')
CONFIG_DEFAULT_FILE = 'svt_default_config.conf'
CONFIG_DEFAULT_SECTION = 'TestCase'

CMD_OPTION_FOR_TEST_NAME = "--test"

TESTER_UTILITY = test_runner_utility.TestRunnerUtility()

default_dict = {'install_type': None, 'access_ip': None, 'userid': None,
                 'password': None, 'hmc_ip_list': None,
                 'hmc_userid_list': None, 'hmc_password_list': None,
                 'hmc_display_name_list': None, 'host_name_list': None,
                 'host_display_name_list': None, 'host_type': None,
                 'local_storage_only': None, 'project': 'ibm-default',
                 'auth_version': 3}
props = ['install_type', 'access_ip', 'userid', 'password', 'hmc_ip_list',
         'hmc_userid_list', 'hmc_password_list', 'hmc_display_name_list',
         'host_name_list', 'host_display_name_list', 'host_type',
         'local_storage_only', 'project', 'auth_version']


class SvtTesterContext(object):
    def __init__(self, authentication_id, authentication_token,
                 service_catalog_of_endpoint_records,
                 config_parser, config_section=None):
        self.authent_id = authentication_id
        self.authent_token = authentication_token
        self.service_endpoint_catalog = service_catalog_of_endpoint_records
        self.config = config_parser
        self.config_section = config_section


def parse_authentication_response(authent_tuple, user):
    """Parse 2 versions of Keystone results, based on 'authent_id'."""
    authent_token = authent_tuple[1]
    if authent_token is None:
        print 'Unable to authenticate user %s' % (user)
        sys.exit(2)
    authent_id = authent_tuple[0]
    if authent_id is None:
        authent_id = authent_token['access']['token']['id']
        service_catalog = authent_token['access']['serviceCatalog']
    else:
        service_catalog = authent_token['token']['catalog']
    return authent_token, authent_id, service_catalog


def _collect_authentication_response(configParser, section):
    access_ip = configParser.get(section, 'access_ip')
    user = configParser.get(section, 'userid')
    pwd = configParser.get(section, 'password')
    project = configParser.get(section, 'project')
    domain = 'Default'
    authVersion = configParser.getint(section, 'auth_version')
    if authVersion == 2:
        return parse_authentication_response((None,
                                              keystoneUtils.authv2(access_ip,
                                                                   user, pwd,
                                                                   project)),
                                             user)
    elif authVersion == 3:
        return parse_authentication_response(keystoneUtils.authv3(access_ip,
                                                                  domain,
                                                                  user, pwd,
                                                                  project),
                                             user)
    else:
        print 'Unrecognized auth version: \'%s\'' % (authVersion)
        sys.exit(2)


def _process_cwd_and_module_name():
    module_name = os.path.basename(sys.argv[0])
    cwd = os.getcwd()
    print 'module_name=', module_name
    return end_with_separator(cwd)


def text_for_help():
    return ("HELP:\n"
            "Command-line Options:\n"
            "    -d CONFIG-DIRECTORY[=" + CONFIG_DEFAULT_PATH + "]\n"
            "    -s CONFIG-SECTION[=TEST-METHOD-NAME]\n"
            "    --help\n"
            "    --test=TEST-METHOD-NAME\n"
            "\n"
            "Command-line Arguments (without any Option keys):\n"
            "    LIST-OF-CONFIG-FILES...[=" + CONFIG_DEFAULT_FILE + "]\n"
            "\n")


def _process_cmdline_options():
    """
    """
    cwd = _process_cwd_and_module_name()
    test_name = None
    section_name = None
    options, args = getopt.getopt(sys.argv[1:], 'd:s:', ["test=", "help"])
    print "options: ", options, ", args: ", args
    config_dir_path = ""
    display_test_help = False
    for option, value in options:
        if option == '-d':  # Specifies a config_dir_path for the config files
            if value == os.curdir:
                config_dir_path = end_with_separator(cwd)
            else:
                config_dir_path = end_with_separator(value)
        elif option == '-s':  # Specifies a stanza-name to use from the config
            section_name = value
        elif option == CMD_OPTION_FOR_TEST_NAME:
            test_name = value
        elif option == "--help":
            display_test_help = True
            print text_for_help()
    config_files = []
    if len(args) == 0:
        args.append(CONFIG_DEFAULT_FILE)
    for cfg_filename in args:
        config_files.append(config_dir_path + cfg_filename)
    return config_files, section_name, test_name, display_test_help


def _process_config_and_test():
    """Use cmd-line options or defaults t
    """
    config_files, section_name, test_name, display_test_help = \
        _process_cmdline_options()
    if display_test_help:
        return None, section_name, test_name, display_test_help
    print "config_files: " + str(config_files)
    # Read in configuration
    configParser = ConfigParser.ConfigParser()
    files_parsed = configParser.read(config_files)
    if config_files != files_parsed:
        print 'files_parsed=', str(files_parsed)
        config_files = [CONFIG_DEFAULT_PATH + config_files[0]]
        print "config_files (2nd try): " + str(config_files)
        files_parsed = configParser.read(config_files)
    if config_files != files_parsed:
        print 'files_parsed=', str(files_parsed)
        config_files = [CONFIG_DEFAULT_PATH + CONFIG_DEFAULT_FILE]
        print "config_files (3rd try): " + str(config_files)
        files_parsed = configParser.read(config_files)
    print 'files_parsed = ', files_parsed
    print 'alt___parsed =', \
        str(['svt_config/config_13Q4_PVC_V1.2/svtconfig1b.conf'])
    if len(files_parsed) == 0:
        print "Could not find config file(s)."
        configParser = None
    else:
        # Determine the section_name
        if section_name is None:
            # Section not given in command-line args, so try alternatives
            if test_name in configParser.sections():
                section_name = test_name
            else:
                section_name = CONFIG_DEFAULT_SECTION
        # Verify the section name
        if section_name in configParser.sections():
            print "Config Section= ", section_name
        else:
            print "WARNING: Section", str(section_name), "not found in config."
            print "  Verify access to config: run-directory > path > file."
    return configParser, section_name, test_name, display_test_help


def main(svt_tester_class=None):
    try:
        log.init()
        print "svt_tester_class=", str(svt_tester_class)
        # Process input arguments these should be configuration files
        configParser, config_section, test_name, display_test_help = \
            _process_config_and_test()
        if display_test_help:
            print 'classdoc', svt_tester_class.__doc__
            return
        if configParser is None:
            print "No configuration.  Exiting..."
            exit()
        # set up test
        authToken, authTokenId, serviceCatalog = \
            _collect_authentication_response(configParser, config_section)
        #print 'service_catalog=', serviceCatalog
        print 'authTokenId=', authTokenId
        print 'authToken=', str(authToken)
        # Initialize the tester and run it
        svt_tester_class.set_tester_context(SvtTesterContext(authTokenId,
            authToken, serviceCatalog, configParser, config_section))
        if test_name is not None:
            test_suite = unittest.TestSuite(
                tests=[svt_tester_class(test_name)])
        else:
            test_suite = unittest.TestLoader().loadTestsFromTestCase(
                svt_tester_class)
            log.write("Loaded from class '" + svt_tester_class.__name__ + "'= "
                      + str(test_suite.countTestCases()))
            if test_suite.countTestCases() < 1:
                raise ValueError("No tests found in SVT Tester class: '"
                                 + svt_tester_class.__name__ + "'")
            elif test_suite.countTestCases() > 1:
                print "Found", test_suite.countTestCases(), "test methods. ",\
                    "Identify ONE test method to run via cmd-line option:",\
                    CMD_OPTION_FOR_TEST_NAME + "=TEST-METHOD-NAME"
                print "Exiting..."
                exit()
        test_result = unittest.TextTestRunner().run(test_suite)
        print str(test_result)
    except IOError, err:
        print ">>> IOError <<<"
        print traceback.format_exc()
        if (isinstance(err, socket.error) or
                isinstance(err, socket.herror) or
                isinstance(err, socket.gaierror) or
                isinstance(err, socket.timeout)):
            print "If a DNS issue, add config IP(s) to 'hosts' file."
    finally:
        log.done()

if __name__ == '__main__':
    main()
