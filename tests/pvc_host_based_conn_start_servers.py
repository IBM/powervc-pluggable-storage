#!/usr/bin/python
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

from rest_framework import glanceUtils
from rest_framework import novaUtils
from rest_framework import svt_tester_base
from rest_framework.restUtils import HttpError
from . import Utils
import sys
import time
import os

#5 Seconds
SLEEP_INTERVAL = 5
#300 seconds / 5 minutes
TIMEOUT = 300

SRV_NAME_PREFIX = 'server_name_prefix'
SRC_HOST = 'source_host'
CONCURRENT_STARTS = 'concurrent_starts'

class SvtStartServerTester(svt_tester_base.SvtTesterBase):
    """
    Tester for Starting all host based powered off Servers

    Test case included:
    test_1001_host_Based_start_servers
    pvc_host_based_start_servers.py --test=test_1001_host_Based_start_servers <path to config file>
    if its not executable, use chmod +x pvc_host_based_start_servers.py

    options needed in config file
    [DEFAULT]
    host_type = powervm
    install_type = [standard|express]
    access_ip = <ip addresss or hostname of PowerVC server>
    userid = <userid with admin group access in PowerVC>
    password = <password for the userid>
    project = ibm-default
    auth_version = 3

    [TestCase]
    [test_1001_host_Based_start_servers]
    source_hosts =  <source host from which the VMs would be started>
    server_name_prefix = <Prefix of VMs that needs to be started on source host>
    concurrent_starts = <No. of concurrent starts>
    """
    required_options = [SRV_NAME_PREFIX, SRC_HOST, CONCURRENT_STARTS]

    src_hosts = []

    def test_1001_host_Based_start_servers(self):
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print('option=', option, 'not found in configuration file')
                options_missing = True
        if options_missing:
            print('Provide missing options to the configuration file.')
            exit(1)

        server_name_prefix = self.config_get(SRV_NAME_PREFIX)
        print(SRV_NAME_PREFIX, server_name_prefix)
        src_host = self.config_get(SRC_HOST)
        print(SRC_HOST, src_host)
        concurrent_starts = self.config_get(CONCURRENT_STARTS)
        print(CONCURRENT_STARTS, concurrent_starts)

        authTokenId = self.authent_id

        print('Obtaining the Managed Server List...')
        server_list = []
        novaUrl = self.getServiceUrl('compute')
        try:
            vm_list = Utils.get_server_list_host(authTokenId, novaUrl, src_host)
            server_list = []
            to_be_started = vm_list

            if to_be_started:
                for server in to_be_started:
                    print('name=', server['name'], 'id=', server['id'])
                    server_list.append({'name': server['name'],
                                        'id': server['id']})
            print('The number of servers in the serverlist is %d' % len(server_list))
            max = conc_start_servers(authTokenId, novaUrl, server_list, concurrent_starts)
            return max
        except HttpError as e:
            print('HTTP Error: {0}'.format(e.body))
            exit(1)

def conc_start_servers(authTokenId, novaUrl, server_list, concurrent_starts):
        max = len(server_list)
        i = 0
        while i < list(range(len(server_list))):
                #print "i :", i
                if ((i == max) and (max-i) == 0):
                        print('Total number of servers started for each iteration is %d' % i)
                        os._exit(0)
                curr_stopped_server = []
                min = concurrent_starts
                #print "min :", min
                if ((max-i) < min):
                        min=max-i
                for j in range(0, min):
                        curr_stopped_server.append(server_list[i+j])
                        print("The current stopped servers", curr_stopped_server)
                        #print "j:", j
                started_servers = get_started_server_list(authTokenId, novaUrl, curr_stopped_server)
                if not started_servers:
                        print('no started servers found, exiting')
                        exit(1)
                print('started servers=', str(started_servers))
                i += min
        return max

def get_started_server_list(authTokenId, novaUrl, server_list):
    print('Obtaining the Managed Started Server List...')

    started_servers = []
    for server in server_list:
        print('Getting Initial VM state...')
        showServerResponse, showServerResponseBodyJSON = \
            novaUtils.showServer(novaUrl, authTokenId, server['id'])

        serverState = \
            showServerResponseBodyJSON['server']['OS-EXT-STS:vm_state']
        sys.stdout.write('Server state = {0} \n'.format(serverState))
        sys.stdout.flush()
        if serverState == 'active':
            started_servers.append(server)
        elif serverState == 'stopped':
            Utils.send_start_server_request(authTokenId, novaUrl, server)
            started_servers.append(server)
    print('Start initiated on all the Stopped VMs, Please wait.....')
    time.sleep(30)
    print('The number of started servers in the started_server list is %d' % len(started_servers))
    return started_servers

if __name__ == '__main__':
    svt_tester_base.main()
