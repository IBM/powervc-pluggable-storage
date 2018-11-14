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
import Utils
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
VOL_COUNT='volume_count'

"""
#Sample config file input

[test_1005_bulk_volume_attach]
server_name_prefix = rose
source_host = 9179MHC_1086D5R
vol_pre = rosevol
vol_start_idx = 1
conn_attach = 2
volume_count = 3
"""

class SVTBulkAttachVolumeTest(svt_tester_base.SvtTesterBase):
    required_options = [SRV_NAME_PREFIX, SRC_HOST,
                        VOL_PRE, VOL_START_IDX, CONN_ATTACH]

    def test_1005_bulk_volume_attach(self):
        print "inside attach volume script"
        dest_hosts = []
        src_hosts = []
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print 'option=', option, 'not found in configuration file'
                options_missing = True
        if options_missing:
            print 'Provide missing options to the configuration file.'
            os._exit(1)

        server_name_prefix = self.config_get(SRV_NAME_PREFIX)
        print SRV_NAME_PREFIX, server_name_prefix
        src_host = self.config_get(SRC_HOST)
        print SRC_HOST, src_host
        vol_pre = self.config_get(VOL_PRE)
        print VOL_PRE, vol_pre
        vol_start_idx = self.config_get(VOL_START_IDX)
        print VOL_START_IDX, vol_start_idx
        con_attach = self.config_get(CONN_ATTACH)
        print CONN_ATTACH, con_attach
        volume_count = self.config_get(VOL_COUNT)
        print VOL_COUNT, volume_count
        novaUrl = self.getServiceUrl('compute')
        cinderUrl = self.getServiceUrl('volume')
        auth_id = self.authent_id
        number_of_attaches = 0
        number_of_attaches += test_1009_Attach_Volume(cinderUrl, auth_id, src_host,
                                    vol_start_idx, vol_pre,
                                    server_name_prefix,volume_count, novaUrl, con_attach)
        print "Total number of attach completed: %d", number_of_attaches
        os._exit(0)

    def test_1005_bulk_volume_attach1(self):
        print "inside attach volume script"
        dest_hosts = []
        src_hosts = []
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print 'option=', option, 'not found in configuration file'
                options_missing = True
        if options_missing:
            print 'Provide missing options to the configuration file.'
            os._exit(1)

        server_name_prefix = self.config_get(SRV_NAME_PREFIX)
        print SRV_NAME_PREFIX, server_name_prefix
        src_host = self.config_get(SRC_HOST)
        print SRC_HOST, src_host
        vol_pre = self.config_get(VOL_PRE)
        print VOL_PRE, vol_pre
        vol_start_idx = self.config_get(VOL_START_IDX)
        print VOL_START_IDX, vol_start_idx
        con_attach = self.config_get(CONN_ATTACH)
        print CONN_ATTACH, con_attach
        volume_count = self.config_get(VOL_COUNT)
        print VOL_COUNT, volume_count
        novaUrl = self.getServiceUrl('compute')
        cinderUrl = self.getServiceUrl('volume')
        auth_id = self.authent_id
        number_of_attaches = 0
        number_of_attaches += test_1009_Attach_Volume(cinderUrl, auth_id, src_host,
                                    vol_start_idx, vol_pre,
                                    server_name_prefix,volume_count, novaUrl, con_attach)
        print "Total number of attach completed: %d", number_of_attaches
        os._exit(0)


    def test_1005_bulk_volume_attach2(self):
        print "inside attach volume script"
        dest_hosts = []
        src_hosts = []
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print 'option=', option, 'not found in configuration file'
                options_missing = True
        if options_missing:
            print 'Provide missing options to the configuration file.'
            os._exit(1)

        server_name_prefix = self.config_get(SRV_NAME_PREFIX)
        print SRV_NAME_PREFIX, server_name_prefix
        src_host = self.config_get(SRC_HOST)
        print SRC_HOST, src_host
        vol_pre = self.config_get(VOL_PRE)
        print VOL_PRE, vol_pre
        vol_start_idx = self.config_get(VOL_START_IDX)
        print VOL_START_IDX, vol_start_idx
        con_attach = self.config_get(CONN_ATTACH)
        print CONN_ATTACH, con_attach
        volume_count = self.config_get(VOL_COUNT)
        print VOL_COUNT, volume_count
        novaUrl = self.getServiceUrl('compute')
        cinderUrl = self.getServiceUrl('volume')
        auth_id = self.authent_id
        number_of_attaches = 0
        number_of_attaches += test_1009_Attach_Volume(cinderUrl, auth_id, src_host,
                                    vol_start_idx, vol_pre,
                                    server_name_prefix,volume_count, novaUrl, con_attach)
        print "Total number of attach completed: %d", number_of_attaches
        os._exit(0)

    def test_1005_bulk_volume_attach3(self):
        print "inside attach volume script"
        dest_hosts = []
        src_hosts = []
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print 'option=', option, 'not found in configuration file'
                options_missing = True
        if options_missing:
            print 'Provide missing options to the configuration file.'
            os._exit(1)

        server_name_prefix = self.config_get(SRV_NAME_PREFIX)
        print SRV_NAME_PREFIX, server_name_prefix
        src_host = self.config_get(SRC_HOST)
        print SRC_HOST, src_host
        vol_pre = self.config_get(VOL_PRE)
        print VOL_PRE, vol_pre
        vol_start_idx = self.config_get(VOL_START_IDX)
        print VOL_START_IDX, vol_start_idx
        con_attach = self.config_get(CONN_ATTACH)
        print CONN_ATTACH, con_attach
        volume_count = self.config_get(VOL_COUNT)
        print VOL_COUNT, volume_count
        novaUrl = self.getServiceUrl('compute')
        cinderUrl = self.getServiceUrl('volume')
        auth_id = self.authent_id
        number_of_attaches = 0
        number_of_attaches += test_1009_Attach_Volume(cinderUrl, auth_id, src_host,
                                    vol_start_idx, vol_pre,
                                    server_name_prefix,volume_count, novaUrl, con_attach)
        print "Total number of attach completed: %d", number_of_attaches
        os._exit(0)

    def test_1005_bulk_volume_attach4(self):
        print "inside attach volume script"
        dest_hosts = []
        src_hosts = []
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print 'option=', option, 'not found in configuration file'
                options_missing = True
        if options_missing:
            print 'Provide missing options to the configuration file.'
            os._exit(1)

        server_name_prefix = self.config_get(SRV_NAME_PREFIX)
        print SRV_NAME_PREFIX, server_name_prefix
        src_host = self.config_get(SRC_HOST)
        print SRC_HOST, src_host
        vol_pre = self.config_get(VOL_PRE)
        print VOL_PRE, vol_pre
        vol_start_idx = self.config_get(VOL_START_IDX)
        print VOL_START_IDX, vol_start_idx
        con_attach = self.config_get(CONN_ATTACH)
        print CONN_ATTACH, con_attach
        volume_count = self.config_get(VOL_COUNT)
        print VOL_COUNT, volume_count
        novaUrl = self.getServiceUrl('compute')
        cinderUrl = self.getServiceUrl('volume')
        auth_id = self.authent_id
        number_of_attaches = 0
        number_of_attaches += test_1009_Attach_Volume(cinderUrl, auth_id, src_host,
                                    vol_start_idx, vol_pre,
                                    server_name_prefix,volume_count, novaUrl, con_attach)
        print "Total number of attach completed: %d", number_of_attaches
        os._exit(0)


    def test_1005_bulk_volume_attach5(self):
        print "inside attach volume script"
        dest_hosts = []
        src_hosts = []
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print 'option=', option, 'not found in configuration file'
                options_missing = True
        if options_missing:
            print 'Provide missing options to the configuration file.'
            os._exit(1)

        server_name_prefix = self.config_get(SRV_NAME_PREFIX)
        print SRV_NAME_PREFIX, server_name_prefix
        src_host = self.config_get(SRC_HOST)
        print SRC_HOST, src_host
        vol_pre = self.config_get(VOL_PRE)
        print VOL_PRE, vol_pre
        vol_start_idx = self.config_get(VOL_START_IDX)
        print VOL_START_IDX, vol_start_idx
        con_attach = self.config_get(CONN_ATTACH)
        print CONN_ATTACH, con_attach
        volume_count = self.config_get(VOL_COUNT)
        print VOL_COUNT, volume_count
        novaUrl = self.getServiceUrl('compute')
        cinderUrl = self.getServiceUrl('volume')
        auth_id = self.authent_id
        number_of_attaches = 0
        number_of_attaches += test_1009_Attach_Volume(cinderUrl, auth_id, src_host,
                                    vol_start_idx, vol_pre,
                                    server_name_prefix,volume_count, novaUrl, con_attach)
        print "Total number of attach completed: %d", number_of_attaches
        os._exit(0)



    ###################################################
# Code for Attach servers
###################################################
def test_1009_Attach_Volume(cinderUrl, auth_id, host_name,
                            vol_start_index, vol_name_prefix,
                            server_name_prefix,volume_count, novaUrl, con_attach):
    try:
        _, volumesDict = cinderUtils.listVolumeDetails(cinderUrl, auth_id)

    except HttpError, e:
        print 'HTTP Error: {0}'.format(e.body)
        exit(1)
    print " inside test_1009_Attach_Volume() "
    vm_list = Utils.get_server_list_host(auth_id, novaUrl, host_name)
    print "length of vm list="
    print len(vm_list)
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
        print volume['name'],volume['status']
        #if volume['status'] == 'available' and \
        if volume['status'] == 'available' and volume['name'] is not None  and \
                volume['name'].startswith(vol_name):
            eligible_vols.append(volume)
    print "length of eligibile volumes="
    print len(eligible_vols)
    print "eligible volumes"
    print eligible_vols
    no_of_used_vols = 0
    attach_number = 0
    no_of_vol =0
    elgible_vol_count = len(eligible_vols)
    if volume_count > elgible_vol_count:
        print "There are no enough volumes available for bulk volume attach"
        print "Number of volumes needed for attach=",volume_count
        print "Number of volumes available=",elgible_vol_count
        os._exit(1)

    for vm in vm_list:
        #print "chocolate -vm name",vm['name']
        if vm['name'].startswith(server_name_prefix):
            """
            if  vm['OS-EXT-STS:vm_state'] == 'active' and\
                vm['health_status']['health_value'] == 'OK':
            """
            if  vm['OS-EXT-STS:vm_state'] == 'active':

                vol_name = vol_name_prefix + str(vol_idx)
                vol_id = 'not set'
                if eligible_vols:
                    if len(eligible_vols) > no_of_used_vols:
                        if elgible_vol_count >= volume_count:
                            #print " yes am in "
                            volumeproperties = []
                            for x in range(volume_count):
                                volume = eligible_vols[no_of_used_vols]
                                vol_id = volume['id']
                                #create attach volume properties
                                volumeProps = {
                                    "volumeId": vol_id,
                                }
                                volumeproperties.append(volumeProps)
                                no_of_used_vols = no_of_used_vols + 1
                                elgible_vol_count = elgible_vol_count-1
                        #call attach volume function
                        vol_metadata = {}
                        vol_metadata['vol_props'] = volumeproperties
                        vol_metadata['vm_id'] = vm['id']
                        to_attach_list.append(vol_metadata)

    attach_number += conn_attach_vols(auth_id, novaUrl, to_attach_list, con_attach)
    time.sleep(300)
    return attach_number


def conn_attach_vols(authTokenId, novaUrl, volumes_to_attach, con_attach):
    max = len(volumes_to_attach)
    i = 0
    while i < range(len(volumes_to_attach)):
            if ((i == max) and (max-i) == 0):
                    print 'Total number of volumes to attach for each iteration is %d' % i
                    return i
            curr_attach_vol = []
            min = con_attach
            #print "min :", min
            if ((max-i) < min):
                    min=max-i
            for j in range(0, min):
                    curr_attach_vol.append(volumes_to_attach[i+j])
                    print "The current started servers", curr_attach_vol
                    #print "j:", j
            conn_attach_vols_sub(authTokenId, novaUrl, curr_attach_vol)
	    time.sleep(30)
            i += min
    return i

def conn_attach_vols_sub(authTokenId, novaUrl, curr_attach_vol):
    for vol_det in curr_attach_vol:
        volprops = vol_det['vol_props']
        vmid = vol_det['vm_id']
	print 'Attaching Volume=', volprops, vmid
        novaUtils.bulkAttachVolume(novaUrl, authTokenId, volprops, vmid)
    	time.sleep(4)


if __name__ == '__main__':
    svt_tester_base.main()
