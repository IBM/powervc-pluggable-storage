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

import inspect
import unittest
from datetime import datetime
from datetime import timedelta
from rest_framework import svt_test_runner
from tests_svt.Utils import DEFAULT_TIMEOUT_SECS, DEFAULT_SLEEP_INTERVAL_SECS
from rest_framework.svt_test_runner import SvtTesterContext

from collections import namedtuple
VmTuple = namedtuple('VmTuple', ['id', 'name'])

CONFIG_DEFAULT_SECTION = 'TestCase'

local_storage_only = False  # Default changeable by config files
cwd = None
module_name = None
config_dir_path = None
config_files = None
property_list = []
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


class SvtTesterBase(unittest.TestCase):
    _default_timeout = None
    _default_sleep_interval = None

    @classmethod
    def set_tester_context(cls, svt_tester_context):
        SvtTesterBase._svt_tester_context = svt_tester_context

    def __init__(self, methodName='runTest'):
        super(SvtTesterBase, self).__init__(methodName)

    @property
    def svt_context(self):
        return SvtTesterBase._svt_tester_context

    @property
    def authent_id(self):
        fmt = '%Y-%m-%dT%H:%M:%S.%f%Z'
        expiry_time_str =\
            self.authent_token['token']['expires_at'].replace('Z', 'UTC')
        expiry_time = datetime.strptime(expiry_time_str, fmt)
        timediff = expiry_time - datetime.utcnow()
        if timediff < timedelta(minutes=180):
            authToken, authTokenId, serviceCatalog =\
                svt_test_runner.\
                    _collect_authentication_response(self.config,
                                                     self.config_section)
            self.\
                set_tester_context(SvtTesterContext(authTokenId, authToken,
                                                    serviceCatalog,
                                                    self.config,
                                                    self.config_section))
            print 'authent_id', authTokenId
        return self.svt_context.authent_id

    @property
    def authent_token(self):
        return self.svt_context.authent_token

    @property
    def service_catalog_of_endpoint_records(self):
        return self.svt_context.service_endpoint_catalog

    @property
    def default_timeout(self):
        if SvtTesterBase._default_timeout is None:
            return DEFAULT_TIMEOUT_SECS
        else:
            return SvtTesterBase._default_timeout

    @default_timeout.setter
    def default_timeout(self, seconds):
        SvtTesterBase._default_timeout = seconds

    @property
    def default_sleep_interval(self):
        if SvtTesterBase._default_sleep_interval is None:
            return DEFAULT_SLEEP_INTERVAL_SECS
        else:
            return SvtTesterBase._default_sleep_interval

    @default_sleep_interval.setter
    def default_sleep_interval(self, seconds):
        SvtTesterBase._default_sleep_interval = seconds

    @property
    def config(self):
        return self.svt_context.config

    @property
    def config_section(self):
        """Returns the (config-file) section name used for this test.

        If the section name was not externally set for this test instance,
        then it defaults to the name of this test instance's test-method.
        The section name can be optionally given to this tester via the
        SvtTesterContext.  For example, a test runner could use a section
        name from a command-line argument (e.g., see svt_test_runner, '-s').
        """
        if self.svt_context.config_section is None:
            return self.id().rpartition('.')[2]
        else:
            return self.svt_context.config_section

    def config_has_option(self, property_namestring):
        return self.config.has_option(self.svt_context.config_section,
                               property_namestring)

    def config_get(self, property_namestring):
        value = self.config.get(self.svt_context.config_section,
                                property_namestring)
        if value.isdigit():
            value = int(value)
        elif ((value.startswith('[') and value.endswith(']')) or
                (value.startswith('{') and value.endswith('}')) or
                (value == 'True') or (value == 'False')):
            value = eval(value)
        return value

    def getServiceUrl(self, service):
        url = None
        for svc_endpoint_rec in self.service_catalog_of_endpoint_records:
            if svc_endpoint_rec['type'] == service:
                for endpoint in svc_endpoint_rec['endpoints']:
                    if endpoint['interface'] == 'public':
                        url = endpoint['url']
                        break
                break
        return url

    @property
    def novaUrl(self):
        return self.getServiceUrl('compute')

    @property
    def cinderUrl(self):
        return self.getServiceUrl('volume')

    @property
    def glanceUrl(self):
        return self.getServiceUrl('image')

    @property
    def keystoneUrl(self):
        return self.getServiceUrl('identity')

    @property
    def neutronUrl(self):
        return self.getServiceUrl('network')

    @property
    def quantumUrl(self):
        return self.neutronUrl

    @property
    def validatorUrl(self):
        return self.getServiceUrl('ttv')

    def setUp(self):
        print "TEST:", self.id()

    # Utility Methods

    def hmc_extract_uuid_list(self, hmc_list):
        return filter(lambda hmc: hmc['hmc_uuid'], hmc_list)

    def host_extract_compute_node_list(self, host_list):
        return filter(lambda host: host['service'] == 'compute', host_list)


def main():
    # Use inspection to determine the Tester class to run
    calling_frame = inspect.stack()[1]
    calling_module = inspect.getmodule(calling_frame[0])
    svt_tester_class = None
    for obj in inspect.getmembers(calling_module, inspect.isclass):
        clazz = obj[1]
        if issubclass(clazz, SvtTesterBase):
            # The 1st Tester found in the module file will be run
            svt_tester_class = clazz
            break
    if svt_tester_class is None:
        print "No Tester (subclass of SvtTesterBase) found in module= ", \
            str(calling_module.__name__)
    else:
        svt_test_runner.main(svt_tester_class)
