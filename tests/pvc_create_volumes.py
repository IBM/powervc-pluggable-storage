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
import os


#5 Seconds
SLEEP_INTERVAL = 10
#300 seconds / 5 minutes
TIMEOUT = 300

#SVC_ADDR = 'svc_addr'
#SVC_USER = 'svc_user'
#SVC_PWD = 'svc_pwd'
#SVC_POOL = 'svc_pool'
#HOST_NAME = 'host_name'
VOL_NAME_PREFIX = 'vol_name_prefix'
VOL_START_INDEX = 'vol_start_index'
VOL_COUNT = 'vol_count'
VOL_TYPE = 'vol_type'
VOL_SIZE = 'vol_size'

#Below varibles are used for Report generation
global total_Success
global total_failure
global success_V
global failed_V
global filePath


class SvtVolumeTester(svt_tester_base.SvtTesterBase):
    required_options = [VOL_NAME_PREFIX, VOL_START_INDEX, VOL_COUNT, VOL_TYPE]

    def test_1008_create_volumes1(self):
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print 'option=', option, 'not found in configuration file'
                options_missing = True
        if options_missing:
            print 'Provide missing options to the configuration file.'
            os._exit(1)

        vol_name_prefix = self.config_get(VOL_NAME_PREFIX)
        print VOL_NAME_PREFIX, vol_name_prefix

        vol_start_index = self.config_get(VOL_START_INDEX)
        print VOL_START_INDEX, vol_start_index

        vol_count = self.config_get(VOL_COUNT)
        print VOL_COUNT, vol_count

        vol_type = self.config_get(VOL_TYPE)
        print VOL_TYPE, vol_type

        vol_size = self.config_get(VOL_SIZE)
        print VOL_SIZE, vol_size
        self.main_function(vol_name_prefix, vol_start_index, vol_count, vol_type, vol_size)

    def test_1008_create_volumes2(self):
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print 'option=', option, 'not found in configuration file'
                options_missing = True
        if options_missing:
            print 'Provide missing options to the configuration file.'
            os._exit(1)

        vol_name_prefix = self.config_get(VOL_NAME_PREFIX)
        print VOL_NAME_PREFIX, vol_name_prefix

        vol_start_index = self.config_get(VOL_START_INDEX)
        print VOL_START_INDEX, vol_start_index

        vol_count = self.config_get(VOL_COUNT)
        print VOL_COUNT, vol_count

        vol_type = self.config_get(VOL_TYPE)
        print VOL_TYPE, vol_type

        vol_size = self.config_get(VOL_SIZE)
        print VOL_SIZE, vol_size
        self.main_function(vol_name_prefix, vol_start_index, vol_count, vol_type, vol_size)

    def test_1008_create_volumes3(self):
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print 'option=', option, 'not found in configuration file'
                options_missing = True
        if options_missing:
            print 'Provide missing options to the configuration file.'
            os._exit(1)

        vol_name_prefix = self.config_get(VOL_NAME_PREFIX)
        print VOL_NAME_PREFIX, vol_name_prefix

        vol_start_index = self.config_get(VOL_START_INDEX)
        print VOL_START_INDEX, vol_start_index

        vol_count = self.config_get(VOL_COUNT)
        print VOL_COUNT, vol_count

        vol_type = self.config_get(VOL_TYPE)
        print VOL_TYPE, vol_type

        vol_size = self.config_get(VOL_SIZE)
        print VOL_SIZE, vol_size
        self.main_function(vol_name_prefix, vol_start_index, vol_count, vol_type, vol_size)

    def test_1008_create_volumes4(self):
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print 'option=', option, 'not found in configuration file'
                options_missing = True
        if options_missing:
            print 'Provide missing options to the configuration file.'
            os._exit(1)

        vol_name_prefix = self.config_get(VOL_NAME_PREFIX)
        print VOL_NAME_PREFIX, vol_name_prefix

        vol_start_index = self.config_get(VOL_START_INDEX)
        print VOL_START_INDEX, vol_start_index

        vol_count = self.config_get(VOL_COUNT)
        print VOL_COUNT, vol_count

        vol_type = self.config_get(VOL_TYPE)
        print VOL_TYPE, vol_type

        vol_size = self.config_get(VOL_SIZE)
        print VOL_SIZE, vol_size
        self.main_function(vol_name_prefix, vol_start_index, vol_count, vol_type, vol_size)

    def test_1008_create_volumes5(self):
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print 'option=', option, 'not found in configuration file'
                options_missing = True
        if options_missing:
            print 'Provide missing options to the configuration file.'
            os._exit(1)

        vol_name_prefix = self.config_get(VOL_NAME_PREFIX)
        print VOL_NAME_PREFIX, vol_name_prefix

        vol_start_index = self.config_get(VOL_START_INDEX)
        print VOL_START_INDEX, vol_start_index

        vol_count = self.config_get(VOL_COUNT)
        print VOL_COUNT, vol_count

        vol_type = self.config_get(VOL_TYPE)
        print VOL_TYPE, vol_type

        vol_size = self.config_get(VOL_SIZE)
        print VOL_SIZE, vol_size
        self.main_function(vol_name_prefix, vol_start_index, vol_count, vol_type, vol_size)


    def test_1008_create_volumes(self):
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print 'option=', option, 'not found in configuration file'
                options_missing = True
        if options_missing:
            print 'Provide missing options to the configuration file.'
            os._exit(1)

        #svc_addr = self.config_get(SVC_ADDR)
        #print SVC_ADDR, svc_addr

        #svc_user = self.config_get(SVC_USER)
        #print SVC_USER, svc_user

        #svc_pwd = self.config_get(SVC_PWD)
        #print SVC_PWD, svc_pwd

        #svc_pool = self.config_get(SVC_POOL)
        #print SVC_POOL, svc_pool

        #host_name = self.config_get(HOST_NAME)
        #print HOST_NAME, host_name

        vol_name_prefix = self.config_get(VOL_NAME_PREFIX)
        print VOL_NAME_PREFIX, vol_name_prefix

        vol_start_index = self.config_get(VOL_START_INDEX)
        print VOL_START_INDEX, vol_start_index

        vol_count = self.config_get(VOL_COUNT)
        print VOL_COUNT, vol_count

        vol_type = self.config_get(VOL_TYPE)
        print VOL_TYPE, vol_type

        vol_size = self.config_get(VOL_SIZE)
        print VOL_SIZE, vol_size
        self.main_function(vol_name_prefix, vol_start_index, vol_count, vol_type, vol_size)

    def main_function (self, vol_name_prefix, vol_start_index, vol_count, vol_type, vol_size):
        #Below varibles are used for Report generation
        global total_Success
        global total_failure
        global success_V
        global failed_V
        global filePath
        success_V = []
        failed_V = []
        total_Success = 0
        total_failure = 0
        cinderUrl = self.getServiceUrl('volume')
        try:
            _, volumeType = cinderUtils.listVolumeTypes(cinderUrl, self.authent_id)
        except HttpError, e:
            print 'HTTP Error: {0}'.format(e.body)
            os._exit(1)

        if volumeType:
            volumeTypeList = volumeType['volume_types']
        if volumeTypeList:
            for voltype in volumeTypeList:
                print 'name=', voltype['name']
                print 'id=', voltype['id']
        filePath = Utils.Create_Status_File("Create_Volumes")
        Utils.Overwrite_File(filePath, "Create_Volumes")
        while vol_start_index < vol_count:
            vol_name = vol_name_prefix+str(vol_start_index)
            volumeProps = {
                           "display_name": vol_name,
                           "size": vol_size,
                           "display_description": "SVT Volumes",
                           "volume_type": vol_type
            }
            print volumeProps

            try:
                _, volumesDict = cinderUtils.createVolume(cinderUrl,
                                                           self.authent_id,
                                                           volumeProps)
                if volumesDict:
                    volume=volumesDict.get('volume')
                    print 'Printing Volume=', volume
                    #print 'name=', volume['display_name']
                    print 'id=', volume['id']
                    success_V.append(str(vol_name))
                    success_V.append("\n")
                    total_Success = total_Success + 1
                else:
                    failed_V.append(str(vol_name))
                    failed_V.append("\n")
                    total_failure = total_failure + 1
                Utils.Report_Update_volumes(filePath, "Create_Volume", total_Success, total_failure, success_V, failed_V)
                vol_start_index = vol_start_index + 1
                time.sleep(5)
            except HttpError, e:
                print 'HTTP Error: {0}'.format(e.body)
                os._exit(1)

if __name__ == '__main__':
    svt_tester_base.main()
