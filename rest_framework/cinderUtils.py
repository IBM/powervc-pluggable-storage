"""
  Copyright IBM Corp. 2018.
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
      http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
"""

from rest_framework import openstackUtils
from rest_framework import restUtils
import json
import string
VOLS = '%s/volumes'
BULKVOLS = '%s/bulk-volumes'
VOLS_DETAIL = VOLS + '/detail'
VOLS_ID = VOLS + '/%s'
VOL_ACTION = VOLS_ID + '/action'
VOL_TYPES = '%s/types'
VOL_TYPE_ID = VOL_TYPES + '/%s'
HOSTS = '%s/os-hosts'
HOSTS_NAME = HOSTS + '/%s'
HOSTS_UPDATE = HOSTS_NAME + '/update-registration'
HOST_CONNECT = HOSTS_NAME + '/connect'
ALL_VOLS = HOSTS_NAME + '/all-volumes'
HOST_ONBOARD = HOSTS_NAME + '/onboard'
HOST_UNMANAGE = HOSTS_NAME + '/unmanage'
HOST_ONBOARD_ID = HOST_ONBOARD + '/%s'
STOR_PROV = '%s/storage-providers'
STOR_PROV_ID = STOR_PROV + '/%s'
STOR_PROV_DETAILS = STOR_PROV + '/detail'
SERVERS = '%s/servers'
ATTCH_VOL = SERVERS + '/%s' + '/os-volume_attachments'
DTTCH_VOL = ATTCH_VOL + '/%s'
emc_sa_id = 'emc_sa_id'


def listVolumeSummaries(cinderUrl, token):

    #print 'ENTER listVolumeSummaries'
    address = openstackUtils.parseAddress(cinderUrl)
    url = VOLS % openstackUtils.parseBaseURL(cinderUrl, address)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def listVolumeDetails(cinderUrl, token):
    #print 'ENTER listVolumeDetails'
    address = openstackUtils.parseAddress(cinderUrl)
    url = VOLS_DETAIL % openstackUtils.parseBaseURL(cinderUrl, address)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)



def data_resize(cinderUrl, token, vol_id, new_value):
    address = openstackUtils.parseAddress(cinderUrl)
    url = VOL_ACTION % (openstackUtils.parseBaseURL(cinderUrl, address),
                     vol_id)
    headers = {'X-Auth-Token': token}
    postBody = json.dumps({"ibm-extend":{"new_size":new_value}})
    return restUtils.postJSON(address, url, postBody, headers)



def showVolume(cinderUrl, token, volume_id):
    #print 'ENTER showVolume'
    address = openstackUtils.parseAddress(cinderUrl)
    url = VOLS_ID % (openstackUtils.parseBaseURL(cinderUrl, address),
                     volume_id)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def createVolume(cinderUrl, token, volumeProps):
    #print 'ENTER createVolume'
    address = openstackUtils.parseAddress(cinderUrl)
    url = VOLS % openstackUtils.parseBaseURL(cinderUrl, address)
    postBody = json.dumps({'volume': volumeProps})
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)

def createBulkVolume(cinderUrl, token, volumeProps):
    #print 'ENTER createVolume'
    address = openstackUtils.parseAddress(cinderUrl)
    url = BULKVOLS % openstackUtils.parseBaseURL(cinderUrl, address)
    print(url)
    postBody = json.dumps(volumeProps)
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)


def deleteVolume(cinderUrl, token, volume_id):
    #print 'ENTER deleteVolume'
    address = openstackUtils.parseAddress(cinderUrl)
    url = VOLS_ID % (openstackUtils.parseBaseURL(cinderUrl, address),
                     volume_id)
    headers = {'X-Auth-Token': token}
    return restUtils.request('DELETE', address, url, headers)


def listVolumeTypes(cinderUrl, token):
    #print 'ENTER listVolumeTypes'
    address = openstackUtils.parseAddress(cinderUrl)
    url = VOL_TYPES % openstackUtils.parseBaseURL(cinderUrl, address)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def showVolumeType(cinderUrl, token, volume_type_id):
    #print 'ENTER showVolumeType'
    address = openstackUtils.parseAddress(cinderUrl)
    url = VOL_TYPE_ID % (openstackUtils.parseBaseURL(cinderUrl, address),
                         volume_type_id)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def createVolumeType(cinderUrl, token, volumeProps):
    #print 'ENTER createVolumeType'
    address = openstackUtils.parseAddress(cinderUrl)
    url = VOL_TYPES % openstackUtils.parseBaseURL(cinderUrl, address)
    postBody = json.dumps({'volume_type': volumeProps})
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)


def deleteVolumeType(cinderUrl, token, volume_type_id):
    #print 'ENTER deleteVolumeType'
    address = openstackUtils.parseAddress(cinderUrl)
    url = VOL_TYPE_ID % (openstackUtils.parseBaseURL(cinderUrl, address),
                         volume_type_id)
    headers = {'X-Auth-Token': token}
    return restUtils.request('DELETE', address, url, headers)


def listHosts(cinderUrl, token):
    #print 'ENTER listHosts'
    address = openstackUtils.parseAddress(cinderUrl)
    url = HOSTS % openstackUtils.parseBaseURL(cinderUrl, address)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)['hosts']


def showHost(cinderUrl, token, host_name):
    #print 'ENTER showHost'
    address = openstackUtils.parseAddress(cinderUrl)
    url = HOSTS_NAME % (openstackUtils.parseBaseURL(cinderUrl, address),
                        host_name)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)

###  PowerVC extensions  ###


def createHost(cinderUrl, token, hostProps):
    #print 'ENTER createHost'
    address = openstackUtils.parseAddress(cinderUrl)
    url = HOSTS % openstackUtils.parseBaseURL(cinderUrl, address)
    postBody = json.dumps({'host': hostProps})
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)

# TODO Check This implementation /os-hosts/{host_name}


def updateHostRegistration(cinderUrl, token, host_name, hostProps):
    #print 'ENTER updateHostRegistration'
    address = openstackUtils.parseAddress(cinderUrl)
    url = HOSTS_UPDATE % (openstackUtils.parseBaseURL(cinderUrl, address),
                          host_name)
    putBody = json.dumps({'host': hostProps})
    headers = {'X-Auth-Token': token}
    return restUtils.putJSON(address, url, putBody, headers)


def deleteHost(cinderUrl, token, host_name):
    #print 'ENTER deleteHost'
    address = openstackUtils.parseAddress(cinderUrl)
    url = HOSTS_NAME % (openstackUtils.parseBaseURL(cinderUrl, address),
                        host_name)
    headers = {'X-Auth-Token': token}
    return restUtils.request('DELETE', address, url, headers)


def createHostConnection(cinderUrl, token, host_name, connectionProps):
    #print 'ENTER createHostConnection'
    address = openstackUtils.parseAddress(cinderUrl)
    url = HOST_CONNECT % (openstackUtils.parseBaseURL(cinderUrl, address),
                          host_name)
    postBody = json.dumps({'host': connectionProps})
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)

### PowerVC Onboarding Extensions ###


def listExistingVolumes(cinderUrl, token, hostName):
    address = openstackUtils.parseAddress(cinderUrl)
    url = ALL_VOLS % (openstackUtils.parseBaseURL(cinderUrl, address),
                      hostName)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def onboardExistingVolumes(cinderUrl, token, hostName, volsProps):
    address = openstackUtils.parseAddress(cinderUrl)
    url = HOST_ONBOARD % (openstackUtils.parseBaseURL(cinderUrl, address),
                          hostName)
    postBody = json.dumps({'volumes': volsProps})
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)


def listOnboardingTasks(cinderUrl, token, hostName):
    address = openstackUtils.parseAddress(cinderUrl)
    url = HOST_ONBOARD % (openstackUtils.parseBaseURL(cinderUrl, address),
                          hostName)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def showOnboardingTaskDetails(cinderUrl, token, hostName, ident):
    address = openstackUtils.parseAddress(cinderUrl)
    url = HOST_ONBOARD_ID % (openstackUtils.parseBaseURL(cinderUrl, address),
                             hostName, ident)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def unmanageServers(cinderUrl, token, hostName, volsProps):
    address = openstackUtils.parseAddress(cinderUrl)
    url = HOSTS_NAME % (openstackUtils.parseBaseURL(cinderUrl, address),
                        hostName)
    postBody = json.dumps(volsProps)
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)

### PowerVC Storage Provider Registration Extensions ###


def registerStorageProvider(cinderUrl, token, volsProps):
    address = openstackUtils.parseAddress(cinderUrl)
    url = HOSTS % openstackUtils.parseBaseURL(cinderUrl, address)
    postBody = json.dumps(volsProps)
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)

""" Handled by deleteHost
def unregisterStorageProvider(cinderUrl, token, hostName):
    address = openstackUtils.parseAddress(cinderUrl)
    url = openstackUtils.parseBaseURL(cinderUrl,
                                      address) + '/os-hosts/' + host_name
    headers = {'X-Auth-Token': token}
    return restUtils.request('DELETE', address, url, headers)
"""
""" Should be handled by updateHosts
def updateStorageProvider(cinderUrl, token, hostName, hostProps):
    address = openstackUtils.parsAddress(cinderUrl)
"""

""" Handled by listHosts
def listStorageHosts(cinderUrl, token):
    address = openstackUtils.parsAddress(cinderUrl)
"""

""" Handled by showHosts
def showStorageHostDetails(cinderUrl, token, hostName, hostProps):
    address = openstackUtils.parsAddress(cinderUrl)
"""


def listStorageProviders(cinderUrl, token):
    address = openstackUtils.parseAddress(cinderUrl)
    url = STOR_PROV % openstackUtils.parseBaseURL(cinderUrl, address)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def showStorageProviderDetails(cinderUrl, token, provider_id):
    address = openstackUtils.parseAddress(cinderUrl)
    url = STOR_PROV_ID % (openstackUtils.parseBaseURL(cinderUrl, address),
                          provider_id)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def showAllStorageProvidersDetail(cinderUrl, token):
    address = openstackUtils.parseAddress(cinderUrl)
    url = STOR_PROV_DETAILS % openstackUtils.parseBaseURL(cinderUrl, address)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)

def listStorageProviders(cinderUrl, token):
    address = openstackUtils.parseAddress(cinderUrl)
    url = STOR_PROV % openstackUtils.parseBaseURL(cinderUrl, address)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def showStorageProviderDetails(cinderUrl, token, provider_id):
    address = openstackUtils.parseAddress(cinderUrl)
    url = STOR_PROV_ID % (openstackUtils.parseBaseURL(cinderUrl, address),
                          provider_id)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)

#For Create Consistency groups
def createConsistencyGroups(cinderUrl, token, connectionProps):
    address = openstackUtils.parseAddress(cinderUrl)
    url = openstackUtils.parseBaseURL(cinderUrl, address) + '/consistencygroups'
    postBody = json.dumps({'consistencygroup': connectionProps})
    print(url)
    print(postBody)
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)

def listcgDetails(cinderUrl, token):
    #print 'ENTER listVolumeDetails'
    address = openstackUtils.parseAddress(cinderUrl)
    url = openstackUtils.parseBaseURL(cinderUrl, address) + '/consistencygroups' + '/detail'
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)

#For Create Consistency groups from src
def createConsistencyGroupssrc(cinderUrl, token, connectionProps):
    address = openstackUtils.parseAddress(cinderUrl)
    url = openstackUtils.parseBaseURL(cinderUrl, address) + '/consistencygroups' + '/create_from_src'
    postBody = json.dumps({'consistencygroup-from-src': connectionProps})
    print(url)
    print(postBody)
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)

#List Consistency Group
def listConsistencyGroups(cinderUrl, token):
    address = openstackUtils.parseAddress(cinderUrl)
    url = openstackUtils.parseBaseURL(cinderUrl, address) + '/consistencygroups' + '/detail'
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)

# Add Volumes into Consistency Group
def addVolumeToConsistencyGroups(cinderUrl, token, cgID, connectionProps):
    address = openstackUtils.parseAddress(cinderUrl)
    url = openstackUtils.parseBaseURL(cinderUrl, address) + '/consistencygroups/' + cgID + '/update'
    postBody = json.dumps({'consistencygroup': connectionProps})
    print(url)
    print(postBody)
    headers = {'X-Auth-Token': token}
    return restUtils.putJSON(address, url, postBody, headers)

def removeVolumeToConsistencyGroups(cinderUrl, token, cgID, connectionProps):
    address = openstackUtils.parseAddress(cinderUrl)
    url = openstackUtils.parseBaseURL(cinderUrl, address) + '/consistencygroups/' + cgID + '/update'
    postBody = json.dumps({'consistencygroup': connectionProps})
    print(url)
    print(postBody)
    headers = {'X-Auth-Token': token}
    return restUtils.putJSON(address, url, postBody, headers)

# Delete consistency Group
def deleteConsistencyGroups(cinderUrl, token, cgID):
    address = openstackUtils.parseAddress(cinderUrl)
    url = openstackUtils.parseBaseURL(cinderUrl, address) + '/consistencygroups/' + cgID + '/delete'
    postBody = json.dumps({'consistencygroup': {'force': 'true'}})
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)

#Consistency group snapshot
def createConsistencySnapshots(cinderUrl, token, connectionProps):
    address = openstackUtils.parseAddress(cinderUrl)
    url = openstackUtils.parseBaseURL(cinderUrl, address) + '/cgsnapshots'
    postBody = json.dumps({'cgsnapshot': connectionProps})
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)

def createGenericGroupType(cinderUrl, token, connectionProps):
    address = openstackUtils.parseAddress(cinderUrl)
    url = openstackUtils.parseBaseURL(cinderUrl, address) +'/group_types'
    postBody = json.dumps({'group_type': connectionProps})
    print(postBody)
    headers = {'X-Auth-Token': token,'OpenStack-API-Version': 'volume latest'}
    print(headers)
    return restUtils.postJSON(address, url, postBody, headers)

def ShowGenericGroupType(cinderUrl, token, group_type_ID):
    address = openstackUtils.parseAddress(cinderUrl)
    url = openstackUtils.parseBaseURL(cinderUrl, address) + '/group_types/' + group_type_ID
    headers = {'X-Auth-Token': token,'OpenStack-API-Version': 'volume latest'}
    return restUtils.getJSON(address, url, headers)

def UpdateGenericGroupType(cinderUrl, token, group_type_ID , connectionProps):
    address = openstackUtils.parseAddress(cinderUrl)
    url = openstackUtils.parseBaseURL(cinderUrl, address) + '/group_type/' + group_type_ID
    postBody = json.dumps({'group_type': connectionProps})
    headers = {'X-Auth-Token': token,'OpenStack-API-Version': 'volume latest'}
    return restUtils.putJSON(address, url, postBody, headers)

def ListGenericGroupType(cinderUrl, token):
    address = openstackUtils.parseAddress(cinderUrl)
    url = openstackUtils.parseBaseURL(cinderUrl, address) + '/group_types'
    headers = {'X-Auth-Token': token,'OpenStack-API-Version': 'volume latest'}
    return restUtils.getJSON(address, url, headers)

def deletegenericGroupType(cinderUrl, token, group_type_ID):
    address = openstackUtils.parseAddress(cinderUrl)
    url = openstackUtils.parseBaseURL(cinderUrl, address) + '/consistencygroups/' + group_type_ID + '/delete'
    headers = {'X-Auth-Token': token,'OpenStack-API-Version': 'volume latest'}
    return restUtils.deleteJSON(address, url,headers)

def createGenericGroup(cinderUrl, token, connectionProps):
    address = openstackUtils.parseAddress(cinderUrl)
    url = openstackUtils.parseBaseURL(cinderUrl, address) + '/groups'
    postBody = json.dumps({'group': connectionProps})
    print(postBody)
    headers = {'X-Auth-Token': token,'OpenStack-API-Version': 'volume latest'}
    return restUtils.postJSON(address, url, postBody, headers)

def ShowGenericGroup(cinderUrl, token, group_ID):
    address = openstackUtils.parseAddress(cinderUrl)
    url = openstackUtils.parseBaseURL(cinderUrl, address) + '/groups/' + group_ID
    headers = {'X-Auth-Token': token,'OpenStack-API-Version': 'volume latest'}
    return restUtils.getJSON(address, url, headers)

def ListGenericGroup(cinderUrl, token):
    address = openstackUtils.parseAddress(cinderUrl)
    url = openstackUtils.parseBaseURL(cinderUrl, address) + '/groups'
    headers = {'X-Auth-Token': token,'OpenStack-API-Version': 'volume latest'}
    return restUtils.getJSON(address, url, headers)

def UpdateGenericGroup(cinderUrl, token, group_ID , connectionProps):
    address = openstackUtils.parseAddress(cinderUrl)
    url = openstackUtils.parseBaseURL(cinderUrl, address) + '/groups/' + group_ID
    postBody = json.dumps({'group': connectionProps})
    headers = {'X-Auth-Token': token,'OpenStack-API-Version': 'volume latest'}
    return restUtils.putJSON(address, url, postBody, headers)

def SnapshotGenericGroup(cinderUrl, token, connectionProps):
    address = openstackUtils.parseAddress(cinderUrl)
    url = openstackUtils.parseBaseURL(cinderUrl, address) + '/group_snapshots'
    postBody = json.dumps({'group_snapshot': connectionProps})
    headers = {'X-Auth-Token': token,'OpenStack-API-Version': 'volume latest'}
    return restUtils.postJSON(address, url, postBody, headers)

def ibmstoragereg(cinderUrl, token, host_type, disp_name, access_ip, pool_name, username, pwd):
        hostProps = { "host_type": host_type,
                      "access_ip": access_ip,
                      "user_id": username,
                      "password": pwd,
                      "volume_pool_name": pool_name,
                      "auto_add_host_key": "true",
                      "host_display_name": disp_name,
                     }
        reg_key = 'Registration'

        address = openstackUtils.parseAddress(cinderUrl)
        url = openstackUtils.parseBaseURL(cinderUrl, address) + '/os-hosts'
        postbody = json.dumps({'host' : { 'registration' : hostProps}})
        headers = {'X-Auth-Token': token}
        registrnRespns, registrnRespnsBodyJSON = restUtils.postJSON(address, url, postbody, headers)

#List Consistency group snapshots
def listConsistencySnapshots(cinderUrl, token):
    address = openstackUtils.parseAddress(cinderUrl)
    url = openstackUtils.parseBaseURL(cinderUrl, address) + '/cgsnapshots' + '/detail'
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)

#List Consistency group snapshots
def deleteConsistencySnapshots(cinderUrl, token, snapID):
    address = openstackUtils.parseAddress(cinderUrl)
    url = openstackUtils.parseBaseURL(cinderUrl, address) + '/cgsnapshots/' + snapID
    print(url)
    headers = {'X-Auth-Token': token}
    return restUtils.deleteJSON(address, url, headers)

#Storage Add Functions
def emc_reg(cinderUrl, token, emc_host_type, emc_disp_name, emc_access_ip, emc_pool_name, emc_userid, emc_pwd, emc_port, emc_storage_array_id,emc_storage_array_id_zeros):
        emc_sa_id = str(emc_storage_array_id)

        for i in range(0,emc_storage_array_id_zeros):
                emc_sa_id = str(0) + str(emc_sa_id)

        print("EMC Registration storage array id : ", emc_sa_id)
        hostProps = { "host_type": emc_host_type,
                      "access_ip": emc_access_ip,
                      "host_display_name": emc_disp_name,
                      "wbem_port": str(emc_port),
                      "user_id": emc_userid,
                      "password": emc_pwd,
                      "storage_array_id": emc_sa_id,
                      "volume_pool_name": emc_pool_name,
                     }
        reg_key = 'Registration'
        print("EMC Registration : hostProps", hostProps)

        address = openstackUtils.parseAddress(cinderUrl)
        url = openstackUtils.parseBaseURL(cinderUrl, address) + '/os-hosts'
        postbody = json.dumps({'host' : { 'registration' : hostProps}})
        headers = {'X-Auth-Token': token}

        print("EMC Registration : postbody", postbody)
        registrnRespns, registrnRespnsBodyJSON = restUtils.postJSON(address, url, postbody, headers)


        return str(registrnRespnsBodyJSON)

def svc_reg(cinderUrl, token, svc_host_type, svc_disp_name, svc_access_ip, svc_pool_name, svc_userid, svc_pwd):
        hostProps = { "host_type": svc_host_type,
                      "access_ip": svc_access_ip,
                      "user_id": svc_userid,
                      "password": svc_pwd,
                      "volume_pool_name": svc_pool_name,
                      "auto_add_host_key": "true",
                      "host_display_name": svc_disp_name,
                     }
        reg_key = 'Registration'

        address = openstackUtils.parseAddress(cinderUrl)
        url = openstackUtils.parseBaseURL(cinderUrl, address) + '/os-hosts'
        postbody = json.dumps({'host' : { 'registration' : hostProps}})
        headers = {'X-Auth-Token': token}
        registrnRespns, registrnRespnsBodyJSON = restUtils.postJSON(address, url, postbody, headers)


def vmax_reg(cinderUrl, token, vmax_host_type, vmax_disp_name, vmax_access_ip, vmax_pool_name, vmax_userid, vmax_pwd, vmax_port, vmax_storage_array_id):
        vmax_sa_id = str(vmax_storage_array_id)
        for i in range(0,3):
                vmax_sa_id = str(0) + str(vmax_sa_id)

        print("vmax Registration storage array id : ", vmax_sa_id)
        hostProps = { "host_type": vmax_host_type,
                      "access_ip": vmax_access_ip,
                      "host_display_name": vmax_disp_name,
                      "wbem_port": str(vmax_port),
                      "user_id": vmax_userid,
                      "password": vmax_pwd,
                      "storage_array_id":vmax_sa_id,
                      "volume_pool_name": vmax_pool_name,
                     }
        reg_key = 'Registration'
        print("vmax Registration : hostProps", hostProps)

        address = openstackUtils.parseAddress(cinderUrl)
        url = openstackUtils.parseBaseURL(cinderUrl, address) + '/os-hosts'
        postbody = json.dumps({'host' : { 'registration' : hostProps}})
        headers = {'X-Auth-Token': token}

        print("vmax Registration : postbody", postbody)
        registrnRespns, registrnRespnsBodyJSON = restUtils.postJSON(address, url, postbody, headers)
        return str(registrnRespnsBodyJSON)

def getStoragelist(cinderUrl, token):
    address = openstackUtils.parseAddress(cinderUrl)
    url = get_storage_DETAILS % openstackUtils.parseBaseURL(cinderUrl, address)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def hds_reg(cinderUrl, token, hds_host_type,hds_access_ip,hds_display_name,hds_user_id,hds_password,hds_horcm_port1,hds_horcm_port2,hds_hitachi_ldev_start,hds_hitachi_ldev_end,hds_volume_pool_name,hds_fc_ports_arry):

        hostProps = { "host_type": hds_host_type,
                      "access_ip": hds_access_ip,
                      "host_display_name": hds_display_name,
                      "user_id": hds_user_id,
                      "password": hds_password,
                      "volume_pool_name": hds_volume_pool_name,
                      "horcm_port1" : hds_horcm_port1,
                      "horcm_port2" : hds_horcm_port2,
                      "hitachi_ldev_start":hds_hitachi_ldev_start,
                      "hitachi_ldev_end":hds_hitachi_ldev_end,
                      "fc_ports":hds_fc_ports_arry,

                     }
        reg_key = 'Registration'
        print("HDS Registration : hostProps", hostProps)

        address = openstackUtils.parseAddress(cinderUrl)
        url = openstackUtils.parseBaseURL(cinderUrl, address) + '/os-hosts'
        postbody = json.dumps({'host' : { 'registration' : hostProps}})
        headers = {'X-Auth-Token': token}

        print("HDS Registration : postbody", postbody)
        registrnRespns, registrnRespnsBodyJSON = restUtils.postJSON(address, url, postbody, headers)
        return str(registrnRespnsBodyJSON)

def update_GPFS_host(cinderUrl, token, host_name):
    #print 'ENTER updateClusteronHost'
      address = openstackUtils.parseAddress(cinderUrl)
      url = openstackUtils.parseBaseURL(cinderUrl, address) + '/spectrum-scale-clusters/' + '1'
      putBody = json.dumps({'cluster':{'compute-hosts':[{'hostname':host_name,'scale-version':"*latest"}]}})
      headers = {'X-Auth-Token': token}
      return restUtils.put(url, put_body)





