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


VOL_NAME_PREFIX = 'vol_name_prefix'
SERVER_NAME_PREFIX = 'server_name_prefix'
SERVER_COUNT = 'server_count'
VOL_COUNT = 'vol_count'
VOL_SIZE = 'vol_size'

class SvtVolumeTester(svt_tester_base.SvtTesterBase):
    required_options = [VOL_NAME_PREFIX, VOL_NAME_PREFIX, SERVER_COUNT, VOL_COUNT, VOL_SIZE]
    ''' 
    [test_1008_create_and_attach_bulkvolumes]
    
    vol_name_prefix = Nilxiv     => Volume name which will be created g
    server_name_prefix = Nil_XIV => Name of server on which bulk create and attach needs to execute
    server_count = 5             => No of server on which bulk create and attach needs to execute   
    vol_count = 3                => No of volumes needs to attach each vm
    vol_size = 2                 => size of volume 
    '''

    def test_1008_create_and_attach_bulkvolumes(self):
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
        vol_count = self.config_get(VOL_COUNT)
        print VOL_COUNT, vol_count
        vol_size = self.config_get(VOL_SIZE)
        print VOL_SIZE, vol_size
        server_name_prefix = self.config_get(SERVER_NAME_PREFIX)
        print SERVER_NAME_PREFIX, server_name_prefix
        server_count = self.config_get(SERVER_COUNT)
        print SERVER_COUNT, server_count

        self.main_function(vol_name_prefix, server_name_prefix, vol_count,  vol_size, server_count)

    def main_function (self, vol_name_prefix, server_name_prefix, vol_count,  vol_size, server_count):
        novaUrl = self.getServiceUrl('compute')
        auth_id = self.authent_id
        cinderUrl = self.getServiceUrl('volume')
        try:
            _, volumeType = cinderUtils.listVolumeTypes(cinderUrl, self.authent_id)
        except HttpError, e:
            print 'HTTP Error: {0}'.format(e.body)
            os._exit(1)
                
        attached_vm_count = 0
        getvmdetails_list = Utils.get_server_dets(auth_id, novaUrl) 
        for vmdet in getvmdetails_list:
            if vmdet['name'].startswith(server_name_prefix):                   
                #print "get vm details", vmdet                
                vm_id = vmdet['id'] 
                #print "Vm details with id and name ", vm_id, vm['name']
                vmhealth1 = vmdet ['health_status'] ['health_value']            
                #print "vm health is", vmhealth1                
                print "vm health value ", vmdet['name'] + " is ", vmhealth1
                if vmhealth1 == 'OK':                 
                    if attached_vm_count < server_count:
                        vol_name_prefixwithcount = vol_name_prefix + str(attached_vm_count)                            
                        volumeProps = {
                                        "volume" :{
                                        "name": vol_name_prefixwithcount,
                                        "size": vol_size,
                                       "display_description": "SVT Volumes",
                                        },
                                    "count": vol_count
                        }
                        print volumeProps
                        try:
                            _, volumesDict = novaUtils.bulkCreateAttachVolume(novaUrl, self.authent_id, volumeProps, vm_id)
                            attached_vm_count = attached_vm_count + 1
                        except HttpError, e:
                            print 'HTTP Error: {0}'.format(e.body)
                            os._exit(1)
                else:
                    print "RMC is inactive for VM", vmdet['name']
        time.sleep(300)
        print "Volume attachment process is completed for", str(attached_vm_count) + " vms"
if __name__ == '__main__':
    svt_tester_base.main()
