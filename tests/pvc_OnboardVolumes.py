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
import pexpect
import subprocess
import paramiko
import re
import time
import os
import sys
from subprocess import Popen, PIPE, STDOUT


volume_name_list = 'volume_name_list'
vol_onboard_count = 'vol_onboard_count'
#Image_name = 'Image_name'
storageName = 'svc_display_name_list'


class SvtonboardVolume(svt_tester_base.SvtTesterBase):
    """

    [test_1020_onboardvolumes]
    volume_name_list = ['DND_Ub']
    svc_display_name_list = ['svc_61']
    vol_onboard_count = 9


    """
    required_options = [volume_name_list, vol_onboard_count]

    def onBoardVolume(self, storageName, volume_name_list, vol_onboard_count, ressto, cinderUrl, token):

        for s in range(len(storageName)):
            storagedisplayname = storageName[s]
            #volume_name = volume_name_list[s]
            argumNo = str(s)
            print "Validating for " + argumNo +  " storage " + storagedisplayname + " argument"
            print "Storage name given in config file =>", storagedisplayname
            for j in range(len(ressto[1]['storage_providers'])):
                host_name = ressto[1]['storage_providers'][j]['storage_hostname']
                servicelist = ressto[1]['storage_providers'] [j]['service']
                storagebasename = servicelist['host_display_name']
                #print servicelist
                print "storage base name=>", storagebasename
                print "storage host name=>", host_name
                # Check if svc display name matches in pvc
                if storagebasename in storagedisplayname:
                    print "Storgae found in powervc"
                    print "***********************"
                    for n in range(len(volume_name_list)):
                        onboardcount = 0;
                        #storagedisplayname = storageName[s]
                        volume_name = volume_name_list[n]
                        print "Check volume existence:", volume_name
                        # Get list of all volumes from that storgae
                        _, allvolumes = cinderUtils.listExistingVolumes(cinderUrl, token, host_name)
                        #print "all volumes", allvolumes
                        allvol = allvolumes['volumes']
                        for volume in allvol:
                            #print 'name=', volume['name'], 'volumeid in storage=', volume['id']
                            # Check if volume name from config file exist in storage
                            if volume_name in volume['name'] :
                                print "volume managed=>", volume['managed']
                                #check if volume is managed by other powervc, if its false, then onboard volume.
                                if volume['managed'] == False:
                                    print "Before onboard count is", + onboardcount
                                    if vol_onboard_count > onboardcount:
                                        configUtils.onboard_vol(cinderUrl, token, volume['id'], host_name)
                                        onboardcount += 1
                                        print "count is", + onboardcount

                                        time.sleep(10)
                                        print "onboarding volume", volume['id'] + "in", host_name
                                        #volumestoragelist.append(volume['id'])
                                    else:
                                        print "User input threshold is reached. No need to onboard additional volumes from this storage"

                else:
                    print "Storage not found in ", storagebasename

    def test_1020_onboardvolumes(self):

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
        #novaUrl = self.getServiceUrl('compute')
        token = self.authent_id
        cinderUrl = self.getServiceUrl('volume')
        print cinderUrl
        ressto = cinderUtils.showAllStorageProvidersDetail(cinderUrl, token)
        print ressto[1]['storage_providers']
        storageName = self.config_get('svc_display_name_list')
        volume_name_list = self.config_get('volume_name_list')
        vol_onboard_count = int(self.config_get('vol_onboard_count'))
        self.onBoardVolume(storageName, volume_name_list, vol_onboard_count, ressto, cinderUrl, token)

    def test_1020_onboardvolumes2(self):

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
        #novaUrl = self.getServiceUrl('compute')
        token = self.authent_id
        cinderUrl = self.getServiceUrl('volume')
        print cinderUrl
        ressto = cinderUtils.showAllStorageProvidersDetail(cinderUrl, token)
        print ressto[1]['storage_providers']
        storageName = self.config_get('svc_display_name_list')
        volume_name_list = self.config_get('volume_name_list')
        vol_onboard_count = int(self.config_get('vol_onboard_count'))
        self.onBoardVolume(storageName, volume_name_list, vol_onboard_count, ressto, cinderUrl, token)


if __name__ == '__main__':
    svt_tester_base.main()
