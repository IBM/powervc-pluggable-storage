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
from datetime import datetime
from datetime import timedelta
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
CONCURRENT_RESIZES = 'concurrent_resizes'
RESIZE_FLAVOR = 'resize_flavor'
DEPLOY_FLAVOR = 'deploy_flavor'
TIME_DURATION = 'time_duration'
TIME_UNITS = 'time_units'


class SvtCaptureTester(svt_tester_base.SvtTesterBase):
    """
    Tester for inactive and active of host based Servers

    Test case included:
    test_1009_resize_off_servers
    pvc_host_based_resize_off_servers.py --test=test_1009_resize_off_servers <path to config file>
    if its not executable, use chmod +x pvc_host_based_resize_off_servers.py

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
    [test_1009_resize_off_servers]
    source_host =  <source host from which the VMs would be resized>
    server_name_prefix = <Prefix of VMs that needs to be resized on source host>
    concurrent_resizes = <No. of concurrent resizes>
    resize_flavor = <Flavor used to resize the VM>
    deploy_flavor = <Flavor of the deployed VM>
    time_duration = <time to run the test based on the time_units specified>
    time_units = <seconds, minutes, hours, days>
    """
    required_options = [SRV_NAME_PREFIX, SRC_HOST, CONCURRENT_RESIZES, RESIZE_FLAVOR, DEPLOY_FLAVOR, TIME_DURATION, TIME_UNITS]

    src_hosts = []

    def test_1009_active_resize_off_servers(self):
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print('option=', option, 'not found in configuration file')
                options_missing = True
        if options_missing:
            print('Provide missing options in the configuration file.')
            os._exit(1)

        server_name_prefix = self.config_get(SRV_NAME_PREFIX)
        print(SRV_NAME_PREFIX, server_name_prefix)
        src_host = self.config_get(SRC_HOST)
        print(SRC_HOST, src_host)
        concurrent_resizes = self.config_get(CONCURRENT_RESIZES)
        print(CONCURRENT_RESIZES, concurrent_resizes)
        resize_flavor = self.config_get(RESIZE_FLAVOR)
        print(RESIZE_FLAVOR, resize_flavor)
        deploy_flavor = self.config_get(DEPLOY_FLAVOR)
        print(DEPLOY_FLAVOR, deploy_flavor)
        time_duration = self.config_get(TIME_DURATION)
        print(TIME_DURATION, time_duration)
        time_units = self.config_get(TIME_UNITS)
        print(TIME_UNITS, time_units)

        if time_units == 'seconds':
            stop_delta = timedelta(seconds=time_duration)
        elif time_units == 'minutes':
            stop_delta = timedelta(minutes=time_duration)
        elif time_units == 'hours':
            stop_delta = timedelta(hours=time_duration)
        elif time_units == 'days':
            stop_delta = timedelta(days=time_duration)
        else:
            print('Unexpected time units, '\
                'should be seconds, minutes, hours, days')
            os._exit(1)

        start = datetime.now()
        elapsed_delta = datetime.now() - start
        no_of_resizes = 0
        resize_flag = 0
        while elapsed_delta < stop_delta:

            authTokenId = self.authent_id

            print('Obtaining the Servers/VMs List...')
            server_list = []
            novaUrl = self.getServiceUrl('compute')
            try:
                vm_list = Utils.get_server_list_host(authTokenId, novaUrl, src_host)
                server_list = []
                to_be_resized = []

                for vm in vm_list:
                    if vm['name'].startswith(server_name_prefix):
                                             print('name=', vm['name'], 'id=', vm['id'])
                                             to_be_resized.append(vm)
                print('The number of VMs from the VMslist containing the s pre-fix is %d' % len(to_be_resized))

#               if to_be_resized:
 #                   for server in to_be_resized:
  #                      print 'name=', server['name'], 'id=', server['id']
   #                     server_list.append(server)
    #            print 'The number of servers in the serverlist is %d' % len(server_list)
                server_list = to_be_resized
                started_servers = get_started_server_list(authTokenId, novaUrl, server_list)
            except HttpError as e:
                print('HTTP Error: {0}'.format(e.body))
                os._exit(1)
            if not started_servers:
                print('no started servers found, exiting')
                os._exit(1)

            try:
                print('The VMs in Active state which will be resized: ')
                for server in started_servers:
                    print(server['name'])
                if resize_flag == 0:
                    flavor = resize_flavor
                    resize_flag = 0
                else:
                    flavor = deploy_flavor
                    resize_flag = 0
                no_of_resizes += resize_servers(authTokenId, novaUrl, started_servers, concurrent_resizes, flavor)
                elapsed_delta = datetime.now() - start
                print('elapsed_delta = {0}'.format(elapsed_delta))
            except Exception as e:
                print('Exception encountered ', str(e))
                print("Total successful Active resizes so far",no_of_resizes)
                os._exit(1)
            except IOError as e:
                 print("I/O error({0}): {1}".format(e.errno, e.strerror))
                 print("Total successful Active resizes so far ",no_of_resizes)
                 os._exit(1)
            break

        print("Total number of resizes completed : %d", no_of_resizes)


def get_started_server_list(authTokenId, novaUrl, server_list):
    print('Obtaining the Active VMs List...')

    started_servers = []
    sleep_needed = False
    for server in server_list:
        print('Getting Initial VM state...')
        serverState = \
            server['OS-EXT-STS:vm_state']
        sys.stdout.write('Server state = {0} \n'.format(serverState))
        serverHealth = \
            server['health_status']
        sys.stdout.write('Server health = {0} \n'.format(serverHealth))
        sys.stdout.flush()
        if serverState == 'active' and serverHealth['health_value'] == 'OK':
            started_servers.append(server)
        elif serverState == 'stopped':
            Utils.send_start_server_request(authTokenId, novaUrl, server)
            sleep_needed = True
            started_servers.append(server)

    if sleep_needed:
        print('Start initiated on all the Stopped VMs, Please wait.....')
        time.sleep(90)
    print("The number of active VMs in the started_server list is %d", len(started_servers))
    return started_servers


def resize_servers(authTokenId, novaUrl, started_servers, concurrent_resizes, flavor):
    max = len(started_servers)
    i = 0
    while i < list(range(len(started_servers))) and i < 8:
        if ((i == max) and (max-i) == 0):
                print('Total number of VMs to be resized for each iteration is %d' % i)
                return i
        curr_started_server = []
        min = concurrent_resizes
                #print "min :", min
        if ((max-i) < min):
                min=max-i
        for j in range(0, min):
                curr_started_server.append(started_servers[i+j])
        for server in curr_started_server:
                print("The current active servers is %s", server['name'])
                        #print "j:", j
        resize_servers_sub(authTokenId, novaUrl, curr_started_server, flavor)
        i += min
    return i


def resize_servers_sub(authTokenId, novaUrl, curr_started_servers, flavor1):



        resize_flavorId = None
        deploy_flavorId = None
        flavor_list = Utils.get_flavor_list(authTokenId, novaUrl)
        print('flavor list is %s', flavor_list)
        for flavor in flavor_list:
            if flavor['name'] == flavor1:
                resize_flavorId = flavor['id']
                print(flavor['name'], resize_flavorId)

        if not resize_flavorId:
            print("Resize Flavor, {0} not found".format(flavor1))
            os._exit(1)

        print('Final VMs to resize are ')
        for server in curr_started_servers:
            print(server['name'])
        for server in curr_started_servers:
            print('Request Resize {0} to flavor {1}'.format(server['name'],
                                                    flavor1))
            try:
                    print('Re-sizing VMs...')
                    Utils.resize_server(authTokenId, novaUrl, server,\
                                    resize_flavorId)
            except Exception as e:
                print('Exception encountered', str(e))
                #print "Total successful Active resizes so far is",success_count
                os._exit(1)

            time.sleep(1)
        for server in curr_started_servers:
            server_detail = Utils.get_server(authTokenId, novaUrl,
                                             server['id'])

            servStatus = Utils.get_server_status_dict(authTokenId,
                                                      novaUrl, server)
            print('Waiting for active state after resize')
            while servStatus:
                print('\n \n servStatus Response=', servStatus)
                if not servStatus['task_state'] and \
                    servStatus['vm_state'] == 'active':
                    print('Active Resize of VM {0} complete successfully'.\
                        format(server['name']))
                   # success_count =success_count + 1
                    break
                elif servStatus['vm_state'] == 'error':
                    print('Error encountered in Active resize for VM with name {0} and id {1}' \
                        .format(server['name'], server ['id']))
                    #print "Total successful Active resizes so far is",success_count
                    raise Exception ("error in Active resize")

                time.sleep(1)
                servStatus = Utils.get_server_status_dict(authTokenId,
                                                          novaUrl,
                                                          server)

if __name__ == '__main__':
    svt_tester_base.main()
