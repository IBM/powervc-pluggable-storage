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
import fnmatch
import os

#5 Seconds
SLEEP_INTERVAL = 5
#300 seconds / 5 minutes
TIMEOUT = 300
Flag1 = 0
class SvtVolumeTester(svt_tester_base.SvtTesterBase):
    def test_1008_list_delete_volumes(self):

        authTokenId = self.authent_id

        cinderUrl = self.getServiceUrl('volume')

        _, volumeType = cinderUtils.listVolumeTypes(cinderUrl, self.authent_id)

        if volumeType:
            volumeTypeList = volumeType['volume_types']
        if volumeTypeList:
            for type in volumeTypeList:
                print 'name=', type['name']
                print 'id=', type['id']

        print 'Obtaining the volume List...to be deleted'

        try:
            _, volumesDict = cinderUtils.listVolumeDetails(cinderUrl,
                                                         self.authent_id)

            to_be_deleted = []
            notto_be_deleted=[]
            volume_id_list = []
            volume_dnd=[]

            if volumesDict:
                volumeList = volumesDict['volumes']
                print 'Printing the volumeList =', volumeList
                #print "harsha_____________________________"
            if volumeList:
                for volume in volumeList:
                    volume_name = volume['name']
                    if (fnmatch.fnmatch(volume_name.upper(),'*DND*')):
                        notto_be_deleted.append(volume)
                        print 'not to be deleted since start with dnd'
                    else:
                        to_be_deleted.append(volume)

            if to_be_deleted:
               for vol in to_be_deleted:
                   print 'name=', vol['name'], 'id=', vol['id']
                   volume_id_list.append({'id': vol['id']})
            get_deleted_volume_list(cinderUrl, authTokenId, volume_id_list)

            print 'The number of volumes in the volume list is %d' % len(volume_id_list)

        except HttpError, e:
            print 'HTTP Error: {0}'.format(e.body)
            os._exit(1)
def get_deleted_volume_list(cinderUrl, authTokenId, volume_id_list):
    #Below varibles are used for Report generation
    global total_Success
    global total_failure
    global success_V
    global failed_V
    success_V = []
    failed_V = []
    total_Success = 0
    total_failure = 0
    Flag1 = 0
    filePath = Utils.Create_Status_File("Delete_Volumes")
    Utils.Overwrite_File(filePath, "Delete_Volumes")
    i = 0
    for vols in volume_id_list:
        print 'Getting the vols details', vols
        print 'The Deleted Volume ids =', vols['id']
        try:
            deleteResponse, imageBody = \
                cinderUtils.deleteVolume(cinderUrl, authTokenId, vols['id'])
        except HttpError, e:
            print 'HTTP Error: {0}'.format(e.body)
            print "There is some issue with deleting this volume, continuing with next volume"
            Flag1 = 1
        if i is 5:
            time.sleep(20)
            i = 0
        print 'delete http response =', deleteResponse
        print 'delete response=', imageBody
        i = i + 1
    print 'Please wait concurrent deletes are In progress'
    time.sleep(30)

    if Flag1 == 1:
        print "Some of volume deletes are failed, please check the code"
        os._exit(1)
    else:
        print "All volumes are Successfully deleted"

if __name__ == '__main__':
    svt_tester_base.main()