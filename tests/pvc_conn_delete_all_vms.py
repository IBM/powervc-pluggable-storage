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

from rest_framework import svt_tester_base
from rest_framework import novaUtils
from rest_framework.restUtils import HttpError
import sys
import time
import os
import Utils
SLEEP_INTERVAL=5
#300 seconds / 5 minmutes
TIMEOUT=300
#Using Flag to validate delete failure

CONCURRENT_DELETES = 'concurrent_deletes'


class SvtDiscoveryTester(svt_tester_base.SvtTesterBase):
    """
    Tester for Deleting all host based VMs

    Test case included:
    test_1001_delete_off_host_servers
    pvc_conn_delete_error_vms.py --test=test_1001_delete_off_error_vms <path to config file>
    if its not executable, use chmod +x pvc_conn_delete_error_vms.py

    options needed in config file
    [DEFAULT]
    host_type = powervm
    install_type = [standard|express]
    access_ip = <ip addresss or hostname of PowerVC server>
    userid = <userid with adminm group access in PowerVC>
    password = <password for the userid>
    project = ibm-default
    auth_version = 3

    [TestCase]
    [test_1001_con_delete_off_all_vms]
    concurrent_deletes = <No. of concurrent deletes>
    """
    required_options = [CONCURRENT_DELETES]

    src_hosts = []

    def test_1001_con_delete_off_all_vms(self):
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print 'option=', option, 'not found in configuration file'
                options_missing = True
        if options_missing:
            print 'Provide missing options to the configuration file.'
            os._exit(1)

        concurrent_deletes = self.config_get(CONCURRENT_DELETES)
        print CONCURRENT_DELETES, concurrent_deletes

        authTokenId = self.authent_id

        print 'Obtaining the Managed Server List...'
        novaUrl = self.getServiceUrl('compute')
        errored_servers = []
        stopped_servers = []
        started_servers = []
        server_list = []
        error_server_list = []
        vm_deleted = []
        try:
            serverListResponse, serverList = novaUtils.listServerSummaries(novaUrl, authTokenId)
            if serverList['servers']:
                for server in serverList['servers']:
                    server_list.append({'name': server['name'],'id': server['id']})

            vm_deleted += conc_delete_servers(authTokenId, novaUrl, server_list, concurrent_deletes)
            print "Total number of VMs deleted: %d", len(vm_deleted) 
        except HttpError, e:
            print 'HTTP Error: {0}'.format(e.body)
            os._exit(1)

def conc_delete_servers(authTokenId, novaUrl, error_server_list, concurrent_deletes):
        maxm = len(error_server_list)
        i = 0
        deleted_servers = []
        while i < range(len(error_server_list)):
                if ((i == maxm) and (maxm-i) == 0):
                        print 'Total number of VMs deleted for each iteration is %d' % i
                        break
                curr_servers_to_be_deleted = []
                minm = concurrent_deletes

                if ((maxm-i) < minm):
                        minm=maxm-i

                for j in range(0, minm):
                    curr_servers_to_be_deleted.append(error_server_list[i+j])
                    print "The current deleted servers", curr_servers_to_be_deleted

                deleted_servers += get_deleted_server_list(authTokenId, novaUrl, curr_servers_to_be_deleted)
                if not deleted_servers:
                        print 'no servers found for deletion, exiting'
                        os._exit(1)
                print 'Deleted Servers=', str(deleted_servers)
                i += minm
        return deleted_servers


def get_deleted_server_list(authTokenId, novaUrl, curr_servers_to_be_deleted):
    deleted_servers = []
    try:
        for server in curr_servers_to_be_deleted:
            print 'Deleting server:name=', server['name'], 'id=', server['id']
            deleteResponse, serverBody = \
                novaUtils.deleteServer(novaUrl, authTokenId, server['id'])
            print 'delete http response =', deleteResponse
            print 'delete response=', serverBody
            deleted_servers.append(server)
    except HttpError, e:
        print 'HTTP Error: {0}'.format(e.body)
        Flag1 = 1
    time_out = 0
    while (len(curr_servers_to_be_deleted) is not 0):
        time_out = time_out + 50
        time.sleep(50)
        del_list = []
        for server in curr_servers_to_be_deleted:
            try:
                servStatus = Utils.get_server_status_dict(authTokenId,
                                                      novaUrl,
                                                      server)
            except HttpError, e:
                if e.code == 404:
                    print 'Deletion complete for Server:{0}'.\
                          format(server['name'])
                    del_list.append(server)
        if time_out is 2000:
            print "Delete wait is timed out, proceeding with next set of delete, please kill \
                   the process if you don't want to continue"
            time.sleep(50)
            break
        for server in del_list:
            curr_servers_to_be_deleted.remove(server)      
    return deleted_servers

if __name__ == '__main__':
    svt_tester_base.main()
