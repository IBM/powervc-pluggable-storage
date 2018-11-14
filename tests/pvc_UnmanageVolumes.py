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

from rest_framework import novaUtils
from rest_framework import quantumUtils
from rest_framework import cinderUtils
from rest_framework import svt_tester_base
from rest_framework import svt_tester_base
from rest_framework import configUtils
from rest_framework.restUtils import HttpError
import re
import time
import os
import sys



volume_name_prefix = 'volume_name_prefix'
vol_unmanage_count = 'vol_unmanage_count'


class SvtUnmanage(svt_tester_base.SvtTesterBase):
    """
    
    Test case included:
    [test_1021_unmanagevolumes]
    volume_name_prefix = ['DND', 'Ub']
    vol_unmanage_count = 3
    """
    required_options = [volume_name_prefix, vol_unmanage_count]

    
    def test_1021_unmanagevolumes(self):

        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print 'option=', option, 'not found in configuration file'
                options_missing = True
        if options_missing:
            print 'Provide missing options to the configuration file.'
            os._exit(1)
        volume_list = []
        volumestoragelist = []
        novaUrl = self.getServiceUrl('compute')
        token = self.authent_id
        cinderUrl = self.getServiceUrl('volume')
        print cinderUrl
        ressto = cinderUtils.showAllStorageProvidersDetail(cinderUrl, token)
        print ressto[1]['storage_providers']
        #storageName = self.config_get('svc_display_name_list')
        volume_name_prefix = self.config_get('volume_name_prefix')
        vol_unmanage_count = int(self.config_get('vol_unmanage_count'))
        unmanagecount = 0;
        for s in range(len(volume_name_prefix)):
            #storagedisplayname = storageName[s]
            volume_name = volume_name_prefix[s]
            argumNo = str(s)
            print "Validating for " + argumNo + " argument"
            #print "Storage name in powervc =>", storagedisplayname
            # Check if svc display name matches in pvc
            print "Check volume existence:", volume_name
            # Get list of all volumes from that storgae
            _, volumesDict = cinderUtils.listVolumeDetails(cinderUrl, token)

            #print "volumesdict", volumesDict
            if volumesDict:
                volumeList = volumesDict['volumes']
                #print "volume list is", volumeList
            if volumeList:
                for volume in volumeList:
                    print 'name=', volume['name'], 'volume id in pvc=', volume['id'], 'status=', volume['status'], 'storage_hostname=', volume['backend_host']
                        
                    #print "volume name from config file is", volume_name
                    if volume_name in volume['name']:
                        print "Volume found in powervc"
                        if volume['status'] == 'available':
                            if vol_unmanage_count > unmanagecount:
                                print "Volume is available for unmanage"
                                #volume_list.append(volume['id'])
                                volumeid = volume['id']
                                host_name = volume['backend_host']
                                try:
                                    configUtils.unmanage_vol(cinderUrl, token, volumeid, host_name)
                                    unmanagecount += 1
                                except HttpError, e:
                                    print 'HTTP Error: {0}'.format(e.body)
                                    
                            else:
                                print "User input threshold is reached. No need to unmanage additional volumes"
                                os._exit(0)                                
            
       
if __name__ == '__main__':
    svt_tester_base.main()
