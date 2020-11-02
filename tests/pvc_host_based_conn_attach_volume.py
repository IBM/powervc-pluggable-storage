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

from rest_framework import svt_tester_base
from rest_framework import novaUtils
from rest_framework import cinderUtils
from rest_framework.restUtils import HttpError
import time
from rest_framework import Utils
from datetime import datetime
import pprint
from datetime import datetime
from datetime import timedelta
import os

#5 Seconds
SLEEP_INTERVAL = 5
#300 seconds / 5 minutes
TIMEOUT = 300

SRV_NAME_PREFIX = 'server_name_prefix'
SRC_HOST = 'source_host'
VOL_PRE = 'vol_pre'
VOL_START_IDX = 'vol_start_idx'
CONN_ATTACH = 'conn_attach'

"""
#Sample config file input
[test_1001_attach_volume]
server_name_prefix = e2e
source_host = 828422A_215E30V
vol_pre = data
vol_start_idx = 1
conn_attach = 2
"""

class SVTAttachIntegrated(svt_tester_base.SvtTesterBase):
    required_options = [SRV_NAME_PREFIX, SRC_HOST,
                        VOL_PRE, VOL_START_IDX, CONN_ATTACH]

    def test_1001_attach_volume(self):
        dest_hosts = []
        src_hosts = []
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print('option=', option, 'not found in configuration file')
                options_missing = True
        if options_missing:
            print('Provide missing options to the configuration file.')
            os._exit(1)

        server_name_prefix = self.config_get(SRV_NAME_PREFIX)
        print(SRV_NAME_PREFIX, server_name_prefix)
        src_host = self.config_get(SRC_HOST)
        print(SRC_HOST, src_host)
        vol_pre = self.config_get(VOL_PRE)
        print(VOL_PRE, vol_pre)
        vol_start_idx = self.config_get(VOL_START_IDX)
        print(VOL_START_IDX, vol_start_idx)
        con_attach = self.config_get(CONN_ATTACH)
        print(CONN_ATTACH, con_attach)
        novaUrl = self.getServiceUrl('compute')
        cinderUrl = self.getServiceUrl('volume')
        auth_id = self.authent_id
        number_of_attaches = 0
        number_of_attaches += test_1009_Attach_Volume(cinderUrl, auth_id, src_host,
                                    vol_start_idx, vol_pre,
                                    server_name_prefix, novaUrl, con_attach)
        print("Total number of attach completed: %d", number_of_attaches)
        os._exit(0)

    def test_1001_attach_volume1(self):
        dest_hosts = []
        src_hosts = []
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print('option=', option, 'not found in configuration file')
                options_missing = True
        if options_missing:
            print('Provide missing options to the configuration file.')
            os._exit(1)

        server_name_prefix = self.config_get(SRV_NAME_PREFIX)
        print(SRV_NAME_PREFIX, server_name_prefix)
        src_host = self.config_get(SRC_HOST)
        print(SRC_HOST, src_host)
        vol_pre = self.config_get(VOL_PRE)
        print(VOL_PRE, vol_pre)
        vol_start_idx = self.config_get(VOL_START_IDX)
        print(VOL_START_IDX, vol_start_idx)
        con_attach = self.config_get(CONN_ATTACH)
        print(CONN_ATTACH, con_attach)
        novaUrl = self.getServiceUrl('compute')
        cinderUrl = self.getServiceUrl('volume')
        auth_id = self.authent_id
        number_of_attaches = 0
        number_of_attaches += test_1009_Attach_Volume(cinderUrl, auth_id, src_host,
                                    vol_start_idx, vol_pre,
                                    server_name_prefix, novaUrl, con_attach)
        print("Total number of attach completed: %d", number_of_attaches)
        os._exit(0)

    def test_1001_attach_volume2(self):
        dest_hosts = []
        src_hosts = []
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print('option=', option, 'not found in configuration file')
                options_missing = True
        if options_missing:
            print('Provide missing options to the configuration file.')
            os._exit(1)

        server_name_prefix = self.config_get(SRV_NAME_PREFIX)
        print(SRV_NAME_PREFIX, server_name_prefix)
        src_host = self.config_get(SRC_HOST)
        print(SRC_HOST, src_host)
        vol_pre = self.config_get(VOL_PRE)
        print(VOL_PRE, vol_pre)
        vol_start_idx = self.config_get(VOL_START_IDX)
        print(VOL_START_IDX, vol_start_idx)
        con_attach = self.config_get(CONN_ATTACH)
        print(CONN_ATTACH, con_attach)
        novaUrl = self.getServiceUrl('compute')
        cinderUrl = self.getServiceUrl('volume')
        auth_id = self.authent_id
        number_of_attaches = 0
        number_of_attaches += test_1009_Attach_Volume(cinderUrl, auth_id, src_host,
                                    vol_start_idx, vol_pre,
                                    server_name_prefix, novaUrl, con_attach)
        print("Total number of attach completed: %d", number_of_attaches)
        os._exit(0)

    def test_1001_attach_volume3(self):
        dest_hosts = []
        src_hosts = []
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print('option=', option, 'not found in configuration file')
                options_missing = True
        if options_missing:
            print('Provide missing options to the configuration file.')
            os._exit(1)

        server_name_prefix = self.config_get(SRV_NAME_PREFIX)
        print(SRV_NAME_PREFIX, server_name_prefix)
        src_host = self.config_get(SRC_HOST)
        print(SRC_HOST, src_host)
        vol_pre = self.config_get(VOL_PRE)
        print(VOL_PRE, vol_pre)
        vol_start_idx = self.config_get(VOL_START_IDX)
        print(VOL_START_IDX, vol_start_idx)
        con_attach = self.config_get(CONN_ATTACH)
        print(CONN_ATTACH, con_attach)
        novaUrl = self.getServiceUrl('compute')
        cinderUrl = self.getServiceUrl('volume')
        auth_id = self.authent_id
        number_of_attaches = 0
        number_of_attaches += test_1009_Attach_Volume(cinderUrl, auth_id, src_host,
                                    vol_start_idx, vol_pre,
                                    server_name_prefix, novaUrl, con_attach)
        print("Total number of attach completed: %d", number_of_attaches)
        os._exit(0)

    def test_1001_attach_volume4(self):
        dest_hosts = []
        src_hosts = []
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print('option=', option, 'not found in configuration file')
                options_missing = True
        if options_missing:
            print('Provide missing options to the configuration file.')
            os._exit(1)

        server_name_prefix = self.config_get(SRV_NAME_PREFIX)
        print(SRV_NAME_PREFIX, server_name_prefix)
        src_host = self.config_get(SRC_HOST)
        print(SRC_HOST, src_host)
        vol_pre = self.config_get(VOL_PRE)
        print(VOL_PRE, vol_pre)
        vol_start_idx = self.config_get(VOL_START_IDX)
        print(VOL_START_IDX, vol_start_idx)
        con_attach = self.config_get(CONN_ATTACH)
        print(CONN_ATTACH, con_attach)
        novaUrl = self.getServiceUrl('compute')
        cinderUrl = self.getServiceUrl('volume')
        auth_id = self.authent_id
        number_of_attaches = 0
        number_of_attaches += test_1009_Attach_Volume(cinderUrl, auth_id, src_host,
                                    vol_start_idx, vol_pre,
                                    server_name_prefix, novaUrl, con_attach)
        print("Total number of attach completed: %d", number_of_attaches)
        os._exit(0)

    def test_1001_attach_volume(self):
        dest_hosts = []
        src_hosts = []
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print('option=', option, 'not found in configuration file')
                options_missing = True
        if options_missing:
            print('Provide missing options to the configuration file.')
            os._exit(1)

        server_name_prefix = self.config_get(SRV_NAME_PREFIX)
        print(SRV_NAME_PREFIX, server_name_prefix)
        src_host = self.config_get(SRC_HOST)
        print(SRC_HOST, src_host)
        vol_pre = self.config_get(VOL_PRE)
        print(VOL_PRE, vol_pre)
        vol_start_idx = self.config_get(VOL_START_IDX)
        print(VOL_START_IDX, vol_start_idx)
        con_attach = self.config_get(CONN_ATTACH)
        print(CONN_ATTACH, con_attach)
        novaUrl = self.getServiceUrl('compute')
        cinderUrl = self.getServiceUrl('volume')
        auth_id = self.authent_id
        number_of_attaches = 0
        number_of_attaches += test_1009_Attach_Volume(cinderUrl, auth_id, src_host,
                                    vol_start_idx, vol_pre,
                                    server_name_prefix, novaUrl, con_attach)
        print("Total number of attach completed: %d", number_of_attaches)
        os._exit(0)

###################################################
# Code for Attach servers
###################################################
def test_1009_Attach_Volume(cinderUrl, auth_id, host_name,
                            vol_start_index, vol_name_prefix,
                            server_name_prefix, novaUrl, con_attach):
    try:
        _, volumesDict = cinderUtils.listVolumeDetails(cinderUrl, auth_id)

    except HttpError as e:
        print('HTTP Error: {0}'.format(e.body))
        exit(1)
    vm_list = Utils.get_server_list_host(auth_id, novaUrl, host_name)
    to_be_attached = []
    server_list = []
    count = 0
    vol_idx = vol_start_index
    to_attach_list = []
    eligible_vols = []
    vol_name = vol_name_prefix
    if volumesDict:
        volumeList = volumesDict['volumes']
    for volume in volumeList:
        if volume['status'] == 'available' and \
                volume['name'].startswith(vol_name):
            eligible_vols.append(volume)

    no_of_used_vols = 0
    attach_number = 0
    for vm in vm_list:
        if vm['name'].startswith(server_name_prefix):
            if  vm['OS-EXT-STS:vm_state'] == 'active' and\
                vm['health_status']['health_value'] == 'OK':
                vol_name = vol_name_prefix + str(vol_idx)
                vol_id = 'not set'
                if eligible_vols:
                    if len(eligible_vols) > no_of_used_vols:
                        volume = eligible_vols[no_of_used_vols]
                        vol_metadata = {}
                        vol_id = volume['id']
                        no_of_used_vols = no_of_used_vols + 1
                        volumeProps = {
                                    "volumeId": vol_id,
                                  }
                        #call attach volume function
                        vol_metadata['vol_props'] = volumeProps
                        vol_metadata['vm_id'] = vm['id']
                        to_attach_list.append(vol_metadata)
    attach_number += conn_attach_vols(auth_id, novaUrl, to_attach_list, con_attach)
    return attach_number


def conn_attach_vols(authTokenId, novaUrl, volumes_to_attach, con_attach):
    max = len(volumes_to_attach)
    i = 0
    while i < len(list(range(len(volumes_to_attach)))):
            if ((i == max) and (max-i) == 0):
                    print('Total number of volumes to attach for each iteration is %d' % i)
                    return i
            curr_attach_vol = []
            min = con_attach
            #print "min :", min
            if ((max-i) < min):
                    min=max-i
            for j in range(0, min):
                curr_attach_vol.append(volumes_to_attach[i+j])
                print("The current started servers", curr_attach_vol)
            conn_attach_vols_sub(authTokenId, novaUrl, curr_attach_vol)
            sleep(30)
            i += min
    return i

def conn_attach_vols_sub(authTokenId, novaUrl, curr_attach_vol):
    for vol_det in curr_attach_vol:
        volprops = vol_det['vol_props']
        vmid = vol_det['vm_id']
        print('Attaching Volume=', volprops, vmid)
        novaUtils.attachVolume(novaUrl, authTokenId, volprops, vmid)
        sleep(4)




if __name__ == '__main__':
    svt_tester_base.main()
