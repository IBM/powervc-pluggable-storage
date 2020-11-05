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
from rest_framework import Utils
import sys
import time
import os

#5 Seconds
SLEEP_INTERVAL = 5
#300 seconds / 5 minutes
TIMEOUT = 1500

SRV_NAME_PREFIX = 'server_name_prefix'
SRC_HOST = 'source_host'
CONCURRENT_CAPTURES = 'concurrent_captures'
TIME_DURATION = 'time_duration'
TIME_UNITS = 'time_units'


class SvtCaptureTester(svt_tester_base.SvtTesterBase):
    """
    Tester for Capturing all powered off Servers

    Test case included:
    test_1001_capture_off_servers
    pvc_capture_all_off_servers.py --test=test_1001_capture_off_servers <path to config file>
    if its not executable, use chmod +x pvc_delete_servers.py

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
    [test_1001_capture_off_servers]
    source_host =  <source host from which the VMs would be captured>
    server_name_prefix = <Prefix of VMs that needs to be captured on source host>
    concurrent_captures = 8
    time_duration = <time to run the test based on the time_units specified>
    time_units = <seconds, minutes, hours, days>
    """
    required_options = [SRV_NAME_PREFIX, SRC_HOST, CONCURRENT_CAPTURES, TIME_DURATION, TIME_UNITS]

    src_hosts = []

    def test_1001_capture_off_servers(self):
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print(('option=', option, 'not found in configuration file'))
                options_missing = True
        if options_missing:
            print('Provide missing options to the configuration file.')
            os._exit(1)

        server_name_prefix = self.config_get(SRV_NAME_PREFIX)
        print((SRV_NAME_PREFIX, server_name_prefix))
        src_host = self.config_get(SRC_HOST)
        print((SRC_HOST, src_host))
        concurrent_captures = self.config_get(CONCURRENT_CAPTURES)
        print((CONCURRENT_CAPTURES, concurrent_captures))
        time_duration = self.config_get(TIME_DURATION)
        print((TIME_DURATION, time_duration))
        time_units = self.config_get(TIME_UNITS)
        print((TIME_UNITS, time_units))

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
        no_of_captures = 0
        while(elapsed_delta < stop_delta):
            authTokenId = self.authent_id
            print('Obtaining the Managed Shutdown Server List...')
            server_list = []
            novaUrl = self.getServiceUrl('compute')
            try:
                vm_list = Utils.get_server_list_host(authTokenId, novaUrl, src_host)
                server_list = []
                to_be_captured = vm_list
                if to_be_captured:
                    for server in to_be_captured:
                        print(('name=', server['name'], 'id=', server['id']))
                        server_list.append({'name': server['name'],
                                            'id': server['id']})
                print(('The number of servers in the serverlist is %d' % len(server_list)))

                stopped_servers = get_shutdown_server_list(authTokenId, novaUrl, vm_list)
            except HttpError as e:
                print(('HTTP Error: {0}'.format(e.body)))
                os._exit(1)
            if not stopped_servers:
               print('no stopped servers found, exiting')
               os._exit(1)
            print(('stopped servers=', str(stopped_servers)))
            glanceUrl = self.getServiceUrl('image')
            no_of_captures += capture_servers(authTokenId, novaUrl, glanceUrl,stopped_servers, TIMEOUT, SLEEP_INTERVAL, concurrent_captures)
            elapsed_delta = datetime.now() - start
            print(('elapsed_delta = {0}'.format(elapsed_delta)))
        print(("Total number of captures done : %d", no_of_captures))

def get_shutdown_server_list(authTokenId, novaUrl, server_list):
    print('Obtaining the Shutdown Managed Server List...')

    stopped_servers = []
    for server in server_list:
        print('Getting Initial VM state...')
        serverState = \
            server['OS-EXT-STS:vm_state']
        sys.stdout.write('Server state = {0} \n'.format(serverState))
        sys.stdout.flush()
        if serverState == 'stopped':
            stopped_servers.append(server)
        elif serverState == 'active':
            stopped_servers.append(server)
    print('Stop initiated on all the Active VMs, Please wait.....')
    print(('The number of stopped servers in the stopped_server list is %d' % len(stopped_servers)))
    return stopped_servers


def capture_servers(authTokenId, novaUrl, glanceUrl, stopped_servers,
                    TIMEOUT, SLEEP_INTERVAL, concurrent_captures):
    max = len(stopped_servers)
    i = 0
    while i < len(list(range(len(stopped_servers)))):
        if ((i == max) and (max-i) == 0):
            print(('Total number of VMs captured for each iteration is %d' % i))
            return i
        curr_stopped_server = []
        min = concurrent_captures
        if((max-i) < min):
            min=max-i
        for j in range(0, min):
            curr_stopped_server.append(stopped_servers[i+j])
            print(("The current stopped servers", curr_stopped_server))
        capture_servers_sub(authTokenId, novaUrl, glanceUrl, curr_stopped_server, TIMEOUT, SLEEP_INTERVAL)
        i += min
    return i

def capture_servers_sub(authTokenId, novaUrl, glanceUrl, curr_stopped_servers,
                    timeout=TIMEOUT, sleep_interval=SLEEP_INTERVAL):
    print('Capturing VM...')
    actionProps = {'createImage': {'name': 'svt_rest_test_capture_dj',
                                   'metadata': {}
                                   }
                   }
    image_list = []
    for server in curr_stopped_servers:
        if isinstance(server, svt_tester_base.VmTuple):
            server = {'id': server.id, 'name': server.name}
        try:
            print(('Capturing server=', server['name'], server['id']))
            createServerActionResponse, \
            createServerActionResponseBodyJSON = \
            novaUtils.createServerAction(novaUrl, authTokenId,
                                         server['id'], actionProps)
        except HttpError as e:
            print(('HTTP Error: {0}'.format(e.body)))
            continue
        image_id = ''
        for header, value in createServerActionResponse.getheaders():
            # print 'header = {0}'.format(header)
            # print 'value = {0}'.format(value)
            if header == 'location':
                image_id = value.split('/')
                image_id = image_id[-1]

        print(('Captured image id = %s for server %s' % \
            (image_id, server['name'])))
        image_list.append({'image_id': image_id, 'server': server})

    print('Getting Image state...')
    runtime = 0
    capture_list = []
    list_captured = []
    capture_list.extend(image_list)
    completed_list = []
    sys.stdout.write('Checking for active state for %d images ' % \
                     len(image_list))
    sys.stdout.flush()
    while runtime <= timeout and capture_list:
        success_list = []
        failed_list = []
        sys.stdout.write('.')
        sys.stdout.flush()
        for image in capture_list:
            showImageResponse, showImageResponseBodyJSON = \
                glanceUtils.showImage(glanceUrl, authTokenId,
                                      image['image_id'])
            imageState = showImageResponseBodyJSON['status']
            if imageState == 'active':
                success_list.append(image)
            elif imageState == 'error':
                failed_list.append(image)
        for image in failed_list:
            capture_list.remove(image)
        for image in success_list:
            capture_list.remove(image)
            completed_list.append(image)
        if capture_list:
            time.sleep(SLEEP_INTERVAL)
            runtime = runtime + SLEEP_INTERVAL

    print('')

    if runtime > timeout:
        print(('ERROR: All Image captures did not' + \
            ' complete within expected timeframe.'))
        print(('%d of %d Captures completed.' % (len(completed_list),
                                                len(image_list))))
    print('')
    return completed_list

if __name__ == '__main__':
    svt_tester_base.main()
