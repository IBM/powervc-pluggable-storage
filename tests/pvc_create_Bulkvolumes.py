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
import os


#5 Seconds
SLEEP_INTERVAL = 10
#300 seconds / 5 minutes
TIMEOUT = 300

VOL_NAME_PREFIX = 'vol_name_prefix'
VOL_MULTIATTACH = 'vol_shared'
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
    """
    options needed in config file
    [test_1008_create_bulkvolumes]
    vol_name_prefix = Nilbulkviltest
    vol_count = 128
    vol_type = svc100 base template
    vol_size = 5
    vol_shared = True

    """
    required_options = [VOL_NAME_PREFIX, VOL_MULTIATTACH, VOL_COUNT, VOL_TYPE]



    def test_1008_create_bulkvolumes(self):
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print('option=', option, 'not found in configuration file')
                options_missing = True
        if options_missing:
            print('Provide missing options to the configuration file.')
            os._exit(1)



        vol_name_prefix = self.config_get(VOL_NAME_PREFIX)
        print(VOL_NAME_PREFIX, vol_name_prefix)

        vol_multiattach = self.config_get(VOL_MULTIATTACH)
        print(VOL_MULTIATTACH, vol_multiattach)

        vol_count = self.config_get(VOL_COUNT)
        print(VOL_COUNT, vol_count)

        vol_type = self.config_get(VOL_TYPE)
        print(VOL_TYPE, vol_type)

        vol_size = self.config_get(VOL_SIZE)
        print(VOL_SIZE, vol_size)
        self.main_function(vol_name_prefix, vol_multiattach, vol_count, vol_type, vol_size)

    def main_function (self, vol_name_prefix, vol_multiattach, vol_count, vol_type, vol_size):
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
        except HttpError as e:
            print('HTTP Error: {0}'.format(e.body))
            os._exit(1)

        if volumeType:
            volumeTypeList = volumeType['volume_types']
        if volumeTypeList:
            for voltype in volumeTypeList:
                print('name=', voltype['name'])
                print('id=', voltype['id'])
        filePath = Utils.Create_Status_File("Create_Volumes")
        Utils.Overwrite_File(filePath, "Create_Volumes")
        volumeProps = {
                        "volume" :{
                        "name": vol_name_prefix,
                        "size": vol_size,
                        "display_description": "SVT Volumes",
                        "multiattach": vol_multiattach,
                        "volume_type": vol_type
                        },
                    "count": vol_count
        }

        print(volumeProps)

        try:
            _, volumesDict = cinderUtils.createBulkVolume(cinderUrl,
                                                           self.authent_id,
                                                           volumeProps)
        except HttpError as e:
            print('HTTP Error: {0}'.format(e.body))
            os._exit(1)

if __name__ == '__main__':
    svt_tester_base.main()
