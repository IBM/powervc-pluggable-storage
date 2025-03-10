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
from tests import Utils
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
CONN_DETTACH = 'conn_dettach'


class SVTDettachIntegrated(svt_tester_base.SvtTesterBase):
    required_options = [SRV_NAME_PREFIX, SRC_HOST,
                        VOL_PRE, VOL_START_IDX, CONN_DETTACH]

    def test_1001_detach_volume(self):
        dest_hosts = []
        src_hosts = []
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print(('option=', option, 'not found in configuration file'))
                options_missing = True
        if options_missing:
            print('Provide missing options to the configuration file.')
            exit(1)

        server_name_prefix = self.config_get(SRV_NAME_PREFIX)
        print((SRV_NAME_PREFIX, server_name_prefix))
        src_host = self.config_get(SRC_HOST)
        print((SRC_HOST, src_host))
        vol_pre = self.config_get(VOL_PRE)
        print((VOL_PRE, vol_pre))
        vol_start_idx = self.config_get(VOL_START_IDX)
        print((VOL_START_IDX, vol_start_idx))
        con_dettach = self.config_get(CONN_DETTACH)
        print((CONN_DETTACH, con_dettach))
        novaUrl = self.getServiceUrl('compute')
        cinderUrl = self.getServiceUrl('volume')
        auth_id = self.authent_id
        number_of_attaches = 0
        number_of_dettaches = 0
        number_of_dettaches += test_1009_Dettach_Volume(cinderUrl, auth_id, src_host,
                                     vol_start_idx, vol_pre, server_name_prefix, novaUrl, con_dettach)
        print(("Total number of dettach completed: %d", number_of_dettaches))
        os._exit(0)

    def test_1001_detach_volume1(self):
        dest_hosts = []
        src_hosts = []
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print(('option=', option, 'not found in configuration file'))
                options_missing = True
        if options_missing:
            print('Provide missing options to the configuration file.')
            exit(1)

        server_name_prefix = self.config_get(SRV_NAME_PREFIX)
        print((SRV_NAME_PREFIX, server_name_prefix))
        src_host = self.config_get(SRC_HOST)
        print((SRC_HOST, src_host))
        vol_pre = self.config_get(VOL_PRE)
        print((VOL_PRE, vol_pre))
        vol_start_idx = self.config_get(VOL_START_IDX)
        print((VOL_START_IDX, vol_start_idx))
        con_dettach = self.config_get(CONN_DETTACH)
        print((CONN_DETTACH, con_dettach))
        novaUrl = self.getServiceUrl('compute')
        cinderUrl = self.getServiceUrl('volume')
        auth_id = self.authent_id
        number_of_attaches = 0
        number_of_dettaches = 0
        number_of_dettaches += test_1009_Dettach_Volume(cinderUrl, auth_id, src_host,
                                     vol_start_idx, vol_pre, server_name_prefix, novaUrl, con_dettach)
        print(("Total number of dettach completed: %d", number_of_dettaches))
        os._exit(0)

    def test_1001_detach_volume2(self):
        dest_hosts = []
        src_hosts = []
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print(('option=', option, 'not found in configuration file'))
                options_missing = True
        if options_missing:
            print('Provide missing options to the configuration file.')
            exit(1)

        server_name_prefix = self.config_get(SRV_NAME_PREFIX)
        print((SRV_NAME_PREFIX, server_name_prefix))
        src_host = self.config_get(SRC_HOST)
        print((SRC_HOST, src_host))
        vol_pre = self.config_get(VOL_PRE)
        print((VOL_PRE, vol_pre))
        vol_start_idx = self.config_get(VOL_START_IDX)
        print((VOL_START_IDX, vol_start_idx))
        con_dettach = self.config_get(CONN_DETTACH)
        print((CONN_DETTACH, con_dettach))
        novaUrl = self.getServiceUrl('compute')
        cinderUrl = self.getServiceUrl('volume')
        auth_id = self.authent_id
        number_of_attaches = 0
        number_of_dettaches = 0
        number_of_dettaches += test_1009_Dettach_Volume(cinderUrl, auth_id, src_host,
                                     vol_start_idx, vol_pre, server_name_prefix, novaUrl, con_dettach)
        print(("Total number of dettach completed: %d", number_of_dettaches))
        os._exit(0)

    def test_1001_detach_volume3(self):
        dest_hosts = []
        src_hosts = []
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print(('option=', option, 'not found in configuration file'))
                options_missing = True
        if options_missing:
            print('Provide missing options to the configuration file.')
            exit(1)

        server_name_prefix = self.config_get(SRV_NAME_PREFIX)
        print((SRV_NAME_PREFIX, server_name_prefix))
        src_host = self.config_get(SRC_HOST)
        print((SRC_HOST, src_host))
        vol_pre = self.config_get(VOL_PRE)
        print((VOL_PRE, vol_pre))
        vol_start_idx = self.config_get(VOL_START_IDX)
        print((VOL_START_IDX, vol_start_idx))
        con_dettach = self.config_get(CONN_DETTACH)
        print((CONN_DETTACH, con_dettach))
        novaUrl = self.getServiceUrl('compute')
        cinderUrl = self.getServiceUrl('volume')
        auth_id = self.authent_id
        number_of_attaches = 0
        number_of_dettaches = 0
        number_of_dettaches += test_1009_Dettach_Volume(cinderUrl, auth_id, src_host,
                                     vol_start_idx, vol_pre, server_name_prefix, novaUrl, con_dettach)
        print(("Total number of dettach completed: %d", number_of_dettaches))
        os._exit(0)

    def test_1001_detach_volume4(self):
        dest_hosts = []
        src_hosts = []
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print(('option=', option, 'not found in configuration file'))
                options_missing = True
        if options_missing:
            print('Provide missing options to the configuration file.')
            exit(1)

        server_name_prefix = self.config_get(SRV_NAME_PREFIX)
        print((SRV_NAME_PREFIX, server_name_prefix))
        src_host = self.config_get(SRC_HOST)
        print((SRC_HOST, src_host))
        vol_pre = self.config_get(VOL_PRE)
        print((VOL_PRE, vol_pre))
        vol_start_idx = self.config_get(VOL_START_IDX)
        print((VOL_START_IDX, vol_start_idx))
        con_dettach = self.config_get(CONN_DETTACH)
        print((CONN_DETTACH, con_dettach))
        novaUrl = self.getServiceUrl('compute')
        cinderUrl = self.getServiceUrl('volume')
        auth_id = self.authent_id
        number_of_attaches = 0
        number_of_dettaches = 0
        number_of_dettaches += test_1009_Dettach_Volume(cinderUrl, auth_id, src_host,
                                     vol_start_idx, vol_pre, server_name_prefix, novaUrl, con_dettach)
        print(("Total number of dettach completed: %d", number_of_dettaches))
        os._exit(0)

    def test_1001_detach_volume5(self):
        dest_hosts = []
        src_hosts = []
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print(('option=', option, 'not found in configuration file'))
                options_missing = True
        if options_missing:
            print('Provide missing options to the configuration file.')
            exit(1)

        server_name_prefix = self.config_get(SRV_NAME_PREFIX)
        print((SRV_NAME_PREFIX, server_name_prefix))
        src_host = self.config_get(SRC_HOST)
        print((SRC_HOST, src_host))
        vol_pre = self.config_get(VOL_PRE)
        print((VOL_PRE, vol_pre))
        vol_start_idx = self.config_get(VOL_START_IDX)
        print((VOL_START_IDX, vol_start_idx))
        con_dettach = self.config_get(CONN_DETTACH)
        print((CONN_DETTACH, con_dettach))
        novaUrl = self.getServiceUrl('compute')
        cinderUrl = self.getServiceUrl('volume')
        auth_id = self.authent_id
        number_of_attaches = 0
        number_of_dettaches = 0
        number_of_dettaches += test_1009_Dettach_Volume(cinderUrl, auth_id, src_host,
                                     vol_start_idx, vol_pre, server_name_prefix, novaUrl, con_dettach)
        print(("Total number of dettach completed: %d", number_of_dettaches))
        os._exit(0)


###########################################################
# Dettach section
###########################################################

def test_1009_Dettach_Volume(cinderUrl, auth_id, host_name, vol_start_index, vol_name_prefix, server_name_prefix, novaUrl, con_dettach):
    volumesDict = {}
    try:
        _, volumesDict = cinderUtils.listVolumeDetails(cinderUrl, auth_id)

    except HttpError as e:
        print(('HTTP Error: {0}'.format(e.body)))
        exit(1)

    if volumesDict:
        volumeList = volumesDict['volumes']
    volumes_to_dettach = []
    dettach_number = 0
    for volume in volumeList:
        if volume['name'].startswith(vol_name_prefix):
            # Find the corresponding server
            vol_metadata = {}
            if volume['attachments']:
                vm_id = volume['attachments'][0]['server_id']
                vol_id = volume['attachments'][0]['id']
                # Now fire the dettach command.
                vol_metadata['vm_id'] = vm_id
                vol_metadata['vol_id'] = vol_id
                volumes_to_dettach.append(vol_metadata)
    dettach_number += conn_dettach_vols(auth_id, novaUrl, volumes_to_dettach, con_dettach)
    return dettach_number

def conn_dettach_vols(authTokenId, novaUrl, volumes_to_dettach, con_dettach):
        max = len(volumes_to_dettach)
        i = 0
        while i < len(list(range(len(volumes_to_dettach)))):
                if ((i == max) and (max-i) == 0):
                        print(('Total number of volumes to detach for each iteration is %d' % i))
                        return i
                curr_dettach_vol = []
                min = con_dettach
                #print "min :", min
                if ((max-i) < min):
                        min=max-i
                for j in range(0, min):
                        curr_dettach_vol.append(volumes_to_dettach[i+j])
                        print(("The current started servers", volumes_to_dettach))
                        #print "j:", j
                conn_dettach_vols_sub(authTokenId, novaUrl, curr_dettach_vol)
                time.sleep(10)
                i += min
        return i

def conn_dettach_vols_sub(authTokenId, novaUrl, curr_dettach_vol):
    started_servers = []
    for vol_det in curr_dettach_vol:
        volid = vol_det['vol_id']
        vmid = vol_det['vm_id']
        print(('Dettaching Volume=', vmid, volid))
        novaUtils.dettachVolume(novaUrl, authTokenId, vmid, volid)
        time.sleep(4)

if __name__ == '__main__':
    svt_tester_base.main()
