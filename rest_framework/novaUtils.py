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

from rest_framework import restUtils, openstackUtils
import json
import re
EXTS = '%s/extensions'
EXTS_ID = EXTS + '/%s'
LIMITS = '%s/limits'
TENANT_USAGE = '%s/os-simple-tenant-usage'
TENANT_USE_ID = TENANT_USAGE + '/%s'
QUOTA_SETS = '%s/os-quota-sets/'
QUOTA_SETS_TID = QUOTA_SETS + '/%s'
QUOTA_SETS_DFLT = QUOTA_SETS_TID + '/defaults'
HMCS = '%s/ibm-hmcs'
HMCS_IDS = HMCS + '/%s'
SVRS = '%s/servers'
SVRS_DETAIL = SVRS + '/detail'
SVR = SVRS + '/%s'
SVR_ACT = SVR + '/action'
SVR_DIAGS = SVR + '/diagnostics'
FLAVS = '%s/flavors'
FLAVS_DETAIL = FLAVS + '/details'
FLAVS_ID = FLAVS + '/%s'
HOSTS = '%s/os-hosts'
HOST_TOPO = '%s/host-storage-topologies'
HOSTS_NAME = HOSTS + '/%s'
HOSTS_UPDATE = HOSTS_NAME + '/update-registration'
HOST_CONNECT = HOSTS_NAME + '/connect'
ALL_VOLS = HOSTS_NAME + '/all-volumes'
HOST_ONBOARD = HOSTS_NAME + '/onboard'
HOST_UNMANAGE = HOSTS_NAME + '/unmanage'
HOST_ONBOARD_ID = HOST_ONBOARD + '/%s'
HYPERV = '%s/os-hypervisors'
HYPERV_DETAL = HYPERV + '/detail'
SERVERS = '%s/servers'
ATTCH_VOL = SERVERS + '/%s' + '/os-volume_attachments'
BULK_ATTCH_VOL = SERVERS + '/%s' + '/action'
DTTCH_VOL = ATTCH_VOL + '/%s'


def listVersion(novaUrl, token):
    #print 'ENTER listVersion'
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address)
    match = re.search('/v\d+\.?\d*/', url)
    if match:
        (url, sep, remainder) = url.partition(match.group(0))
        url += sep
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def listExtensions(novaUrl, token):
    #print 'ENTER listExtensions'
    address = openstackUtils.parseAddress(novaUrl)
    url = EXTS % openstackUtils.parseBaseURL(novaUrl, address)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def showExtension(novaUrl, token, extension_id):
    #print 'ENTER showExtension'
    address = openstackUtils.parseAddress(novaUrl)
    url = EXTS_ID % (openstackUtils.parseBaseURL(novaUrl, address), extension_id)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def listLimits(novaUrl, token):
    #print 'ENTER listLimits'
    address = openstackUtils.parseAddress(novaUrl)
    url = LIMITS % openstackUtils.parseBaseURL(novaUrl, address)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def listTenantUsages(novaUrl, token):
    #print 'ENTER listTenantUsages'
    address = openstackUtils.parseAddress(novaUrl)
    url = TENANT_USAGE % openstackUtils.parseBaseURL(novaUrl, address)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def showTenantUsage(novaUrl, token, tenant_id):
    #print 'ENTER showTenantUsage'
    address = openstackUtils.parseAddress(novaUrl)
    url = TENANT_USE_ID % (openstackUtils.parseBaseURL(novaUrl, address),
                           tenant_id)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)

def showTenantQuotaSet(novaUrl, token, tenant_id):
    #print 'ENTER showTenantQuotaSet'
    address = openstackUtils.parseAddress(novaUrl)
    url = QUOTA_SETS_TID % (openstackUtils.parseBaseURL(novaUrl, address),
                            tenant_id)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)

def showTenantQuotaSetDefaults(novaUrl, token, tenant_id):
    #print 'ENTER showTenantQuotaSetDefaults'
    address = openstackUtils.parseAddress(novaUrl)
    url = QUOTA_SETS_DFLT % (openstackUtils.parseBaseURL(novaUrl, address),
                             tenant_id)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)

def updateTenantQuotaSet(novaUrl, token, tenant_id, quotaSetProps):
    #print 'ENTER updateTenantQuotaSet'
    address = openstackUtils.parseAddress(novaUrl)
    url = QUOTA_SETS_TID % (openstackUtils.parseBaseURL(novaUrl, address),
                            tenant_id)
    putBody = json.dumps({'quota_set': quotaSetProps})
    headers = {'X-Auth-Token': token}
    return restUtils.putJSON(address, url, putBody, headers)

def attachVolume(novaUrl, token, volumeProps, vm_id):
    address = openstackUtils.parseAddress(novaUrl)
    url = ATTCH_VOL % (openstackUtils.parseBaseURL(novaUrl, address),
                     vm_id)
    postBody = json.dumps({'volumeAttachment': volumeProps})
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)

def dettachVolume(novaUrl, token, vm_id, vol_id):
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + "/servers/" + vm_id + "/os-volume_attachments/" + vol_id
    headers = {'X-Auth-Token': token}
    return restUtils.request('DELETE', address, url, headers)

def bulkAttachVolume(novaUrl, token, volumeProps, vm_id):
    address = openstackUtils.parseAddress(novaUrl)
    url = SVR_ACT % (openstackUtils.parseBaseURL(novaUrl, address),
                     vm_id)
    postBody = json.dumps({'bulkVolumeAttach':{'volumeAttachment':volumeProps}})
    headers = {'X-Auth-Token': token}
    print("Attach Request Details")
    print((address+url))
    print(postBody)
    return restUtils.postJSON(address, url, postBody, headers)

def bulkCreateAttachVolume(novaUrl, token, volumeProps, vm_id):
    address = openstackUtils.parseAddress(novaUrl)
    url = SVR_ACT % (openstackUtils.parseBaseURL(novaUrl, address),
                     vm_id)
    postBody = json.dumps({'bulkVolumeAttach':{'volumeAttachment': [volumeProps]}})
    headers = {'X-Auth-Token': token}
    print("Attach Request Details")
    print((address+url))
    print(postBody)
    return restUtils.postJSON(address, url, postBody, headers)

def listHostStorageTopo(novaUrl, token):
    address = openstackUtils.parseAddress(novaUrl)
    url = HOST_TOPO % openstackUtils.parseBaseURL(novaUrl, address)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)

def listServerSummaries(novaUrl, token):
    #print 'ENTER listServerSummaries'
    address = openstackUtils.parseAddress(novaUrl)
    url = SVRS % openstackUtils.parseBaseURL(novaUrl, address)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)

def listServerSummaries_host(novaUrl, token, host_id):
    #print 'ENTER listServerSummaries'
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + "/servers/detail?host=" + host_id
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)

def listServerDetails(novaUrl, token):
    #print 'ENTER listServerDetails'
    address = openstackUtils.parseAddress(novaUrl)
    url = SVRS_DETAIL % openstackUtils.parseBaseURL(novaUrl, address)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)

def showServer(novaUrl, token, server_id):
    #print 'ENTER showServer'
    address = openstackUtils.parseAddress(novaUrl)
    url = SVR % (openstackUtils.parseBaseURL(novaUrl, address),
                 server_id)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)

def showServer_per_host(novaUrl, token, server_id, host_id):
    #print 'ENTER showServer'
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl,
                                      address) + "/" + server_id +'?host=' + host_id
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)

def createServer(novaUrl, token, serverProps):
    #print 'ENTER createServer'
    address = openstackUtils.parseAddress(novaUrl)
    url = SVRS % openstackUtils.parseBaseURL(novaUrl, address)
    postBody = json.dumps({'server': serverProps})
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)

def deleteServer(novaUrl, token, server_id):
    #print 'ENTER deleteServer'
    address = openstackUtils.parseAddress(novaUrl)
    url = SVR % (openstackUtils.parseBaseURL(novaUrl, address),
                 server_id)
    headers = {'X-Auth-Token': token}
    return restUtils.request('DELETE', address, url, headers)

def suspendServer(novaUrl, token, server_id, actionProps):
    address = openstackUtils.parseAddress(novaUrl)
    url = SVR_ACT % (openstackUtils.parseBaseURL(novaUrl, address),
                     server_id)
    postBody = json.dumps(actionProps)
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)

def resumeServer(novaUrl, token, server_id, actionProps):
    address = openstackUtils.parseAddress(novaUrl)
    url = SVR_ACT % (openstackUtils.parseBaseURL(novaUrl, address),
                     server_id)
    postBody = json.dumps(actionProps)
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)

def pauseServer(novaUrl, token, server_id, actionProps):
    address = openstackUtils.parseAddress(novaUrl)
    url = SVR_ACT % (openstackUtils.parseBaseURL(novaUrl, address),
                     server_id)
    postBody = json.dumps(actionProps)
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)

def unpauseServer(novaUrl, token, server_id, actionProps):
    address = openstackUtils.parseAddress(novaUrl)
    url = SVR_ACT % (openstackUtils.parseBaseURL(novaUrl, address),
                     server_id)
    postBody = json.dumps(actionProps)
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)

def createServerAction(novaUrl, token, server_id, actionProps):
    #print 'ENTER createServerAction'
    address = openstackUtils.parseAddress(novaUrl)
    url = SVR_ACT % (openstackUtils.parseBaseURL(novaUrl, address),
                     server_id)
    postBody = json.dumps(actionProps)
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)


def showServerDiagnostics(novaUrl, token, server_id):
    #print 'ENTER showServerDiagnostics'
    address = openstackUtils.parseAddress(novaUrl)
    url = SVR_DIAGS % (openstackUtils.parseBaseURL(novaUrl, address),
                       server_id)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def listFlavorSummaries(novaUrl, token):
    #print 'ENTER listFlavorSummaries'
    address = openstackUtils.parseAddress(novaUrl)
    url = FLAVS % openstackUtils.parseBaseURL(novaUrl, address)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def listFlavorDetails(novaUrl, token):
    #print 'ENTER listFlavorDetails'
    address = openstackUtils.parseAddress(novaUrl)
    url = FLAVS_DETAIL % openstackUtils.parseBaseURL(novaUrl, address)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def showFlavor(novaUrl, token, flavor_id):
    #print 'ENTER showFlavor'
    address = openstackUtils.parseAddress(novaUrl)
    url = FLAVS_ID % (openstackUtils.parseBaseURL(novaUrl, address),
                      flavor_id)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def createFlavor(novaUrl, token, flavorProps):
    #print 'ENTER createFlavor'
    address = openstackUtils.parseAddress(novaUrl)
    url = FLAVS % openstackUtils.parseBaseURL(novaUrl, address)
    postBody = json.dumps({'flavor': flavorProps})
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)


def deleteFlavor(novaUrl, token, flavor_id):
    #print 'ENTER deleteFlavor'
    address = openstackUtils.parseAddress(novaUrl)
    url = FLAVS_ID % (openstackUtils.parseBaseURL(novaUrl, address),
                      flavor_id)
    headers = {'X-Auth-Token': token}
    return restUtils.request('DELETE', address, url, headers)


def listHosts(novaUrl, token):
    #print 'ENTER listHosts'
    address = openstackUtils.parseAddress(novaUrl)
    url = HOSTS % openstackUtils.parseBaseURL(novaUrl, address)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def showHost(novaUrl, token, host_name):
    #print 'ENTER showHost'
    address = openstackUtils.parseAddress(novaUrl)
    url = HOSTS_NAME % (openstackUtils.parseBaseURL(novaUrl, address),
                        host_name)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def listHypervisorSummaries(novaUrl, token):
    #print 'ENTER listHypervisorSummaries'
    address = openstackUtils.parseAddress(novaUrl)
    url = HYPERV % openstackUtils.parseBaseURL(novaUrl, address)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def listHypervisorDetails(novaUrl, token):
    #print 'ENTER listHypervisorDetails'
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + \
        '/os-hypervisors/detail'
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def showHypervisor(novaUrl, token, hypervisor_id):
    #print 'ENTER showHypervisor'
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + \
        '/os-hypervisors/' + str(hypervisor_id)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def listHypervisorServers(novaUrl, token, hypervisor_hostname):
    #print 'ENTER listHypervisorServers'
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + \
        '/os-hypervisors/' + hypervisor_hostname + '/servers'
    headers = {'X-Auth-Token': token}
    resp = restUtils.getJSON(address, url, headers)
    if 'servers' in resp['hypervisors'][0]:
        return resp['hypervisors'][0]
    else:
        return []


def listImageSummaries(novaUrl, token):
    #print 'ENTER listImageSummaries'
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + '/images'
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def listImageDetails(novaUrl, token):
    #print 'ENTER listImageDetails'
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + '/images/detail'
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def showImage(novaUrl, token, image_id):
    #print 'ENTER showImage'
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + '/images/' + image_id
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def deleteImage(novaUrl, token, image_id):
    #print 'ENTER deleteImage'
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + '/images/' + image_id
    headers = {'X-Auth-Token': token}
    return restUtils.request('DELETE', address, url, headers)


def listVolumeAttachments(novaUrl, token, server_id):
    #print 'ENTER listVolumeAttachments'
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + '/servers/' + server_id + '/os-volume_attachments'
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def showVolumeAttachment(novaUrl, token, server_id, attachment_id):
    #print 'ENTER showVolumeAttachment'
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + '/servers/' + \
        server_id + '/os-volume_attachments/' + attachment_id
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def createVolumeAttachment(novaUrl, token, server_id, volumeAttachProps):
    #print 'ENTER createVolumeAttachment'
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + '/servers/' + \
        server_id + '/os-volume_attachments'
    postBody = json.dumps({'volumeAttachment': volumeAttachProps})
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)


def deleteVolumeAttachment(novaUrl, token, server_id, attachment_id):
    #print 'ENTER deleteVolumeAttachment'
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + '/servers/' + \
        server_id + '/os-volume_attachments/' + attachment_id
    headers = {'X-Auth-Token': token}
    return restUtils.request('DELETE', address, url, headers)


""" Function to attach an additional vNIC to a Virtual Machine using Static Network"""

def addvNIC(novaUrl, quantumUrl, token, serverid, network_id, ipaddr, subnet_id):
    address = openstackUtils.parseAddress(novaUrl)
    #print "address : ", address
    port_resp, body_json = get_port(token, quantumUrl)
    print(ipaddr)
    #print len(body_json['ports'])
    #print body_json['ports'][93]['fixed_ips'][0]['ip_address']
    temp = []
    port_id = 0
    for i in range(len(body_json['ports'])):
        print(i)
        if body_json['ports'][i]['fixed_ips']:
            ip = body_json['ports'][i]['fixed_ips'][0]['ip_address']
        #print ip
            if ip == ipaddr:
                port_id = body_json['ports'][i]['id']
                print("ip is found")
                break
            else:
                print("port not present")

    print(port_id)
    if port_id == 0:
        port_resp, bdy_json = create_port(token, quantumUrl, network_id, ipaddr, subnet_id)
        port_id = bdy_json['port']['id']
    print(("Port response", port_resp))
    print(("portId", port_id))
    url = openstackUtils.parseBaseURL(novaUrl, address) + \
        '/servers/' + serverid + '/os-interface'
    print(("url : ", url))
    postBody = json.dumps({"interfaceAttachment": \
                           {"port_id": port_id}})


    print(("postbody:", postBody))
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)
    #print '\nReturning from addvNic function..\n'
    #return resp

def addSRIOVvNIC(novaUrl, quantumUrl, token, serverid, network_id, ipaddr, subnet_id, sriov_vnic_required_vfs, sriov_capacity):
    address = openstackUtils.parseAddress(novaUrl)
    #print "address : ", address
    port_resp, body_json = get_port(token, quantumUrl)
    print(ipaddr)
    #print len(body_json['ports'])
    #print body_json['ports'][93]['fixed_ips'][0]['ip_address']
    temp = []
    port_id = 0
    for i in range(len(body_json['ports'])):
        print(i)
        if body_json['ports'][i]['fixed_ips']:
            ip = body_json['ports'][i]['fixed_ips'][0]['ip_address']
        #print ip
            if ip == ipaddr:
                port_id = body_json['ports'][i]['id']
                print("ip is found")
                break
            else:
                print("port not present")

    print(port_id)
    if port_id == 0:
        port_resp, bdy_json = create_SRIOV_port(token, quantumUrl, network_id, ipaddr, subnet_id, sriov_vnic_required_vfs, sriov_capacity)
        port_id = bdy_json['port']['id']
    print(("Port response", port_resp))
    print(("portId", port_id))
    url = openstackUtils.parseBaseURL(novaUrl, address) + \
        '/servers/' + serverid + '/os-interface'
    print(("url : ", url))
    postBody = json.dumps({"interfaceAttachment": \
                           {"port_id": port_id}})


    print(("postbody:", postBody))
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)

""" Function to attach an additional vNIC to a Virtual Machine using Dynamic Network"""
def addvNIC_dy (novaUrl, token, serverid, network_id):
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + \
        '/servers/' + serverid + '/os-interface'
    postBody = json.dumps({"interfaceAttachment": {"net_id": network_id}})
    headers = {'X-Auth-Token': token}
    print('\nExiting from addvNic function..\n')
    return restUtils.postJSON(address, url, postBody, headers)

""" Fucntion to remove an existing vNIC from a Virtual Machine """
def removevNIC(novaUrl, token, serverid, attachment_id):
    address = openstackUtils.parseAddress(novaUrl)
    url =openstackUtils.parseBaseURL(novaUrl, address) +'/servers/' + serverid +'/os-interface/'+ attachment_id
    headers = {'X-Auth-Token': token}
    return restUtils.request('DELETE', address, url, headers)

"""Function to list all vNIC interfaces attached to a VM"""
def listvNIC(novaUrl, token, serverid):
    address = openstackUtils.parseAddress(novaUrl)
    url =openstackUtils.parseBaseURL(novaUrl, address) +'/servers/' + serverid +'/os-interface'
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)

def create_port(token, quantumUrl, network_id, ipaddr, subnet_id):
    print("Creating port for IP address")
    address = openstackUtils.parseAddress(quantumUrl)
    url = openstackUtils.parseBaseURL(quantumUrl, address) + '/v2.0/ports'
    postBody = json.dumps({"port":{"network_id": network_id, "fixed_ips":[{"subnet_id": subnet_id, "ip_address": ipaddr}]}})
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)

## This function used to create SRIOV ports
def create_SRIOV_port(token, quantumUrl, network_id, ipaddr, subnet_id, sriov_vnic_required_vfs, sriov_capacity):
    print("Creating port for IP address")
    address = openstackUtils.parseAddress(quantumUrl)
    url = openstackUtils.parseBaseURL(quantumUrl, address) + '/v2.0/ports'
    sriov_port_Props = {
                 "name":"powervc_attached",
                 "network_id": network_id,
                 "fixed_ips":[{"subnet_id": subnet_id, "ip_address":ipaddr}],
                 "binding:vnic_type":"direct",
                 "binding:profile":{"delete_with_instance":1,"vnic_required_vfs":sriov_vnic_required_vfs,"capacity":sriov_capacity}
                }
    postBody = json.dumps({'port' : sriov_port_Props})
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)

def get_port(token, quantumUrl):
    address = openstackUtils.parseAddress(quantumUrl)
    url = openstackUtils.parseBaseURL(quantumUrl, address) + '/v2.0/ports'
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)
###  PowerVC extensions  ###

###  PowerVC extensions  ###


def createHost(novaUrl, token, hostProps):
    #print 'ENTER createHost'
    """Originally, this did not provide the 'registration' level for
    'hostProps', which is inconsistent with both 'registerHmc' and
    'updateHmcRegistration'.  So, now we provide it if needed.  The
    reason for not just providing it in all cases was concern for legacy
    code that is already providing the 'registration' level.
    """
    reg_key = 'registration'
    if reg_key not in hostProps:
        hostProps = {reg_key: hostProps}
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + '/os-hosts'
    postBody = json.dumps({'host': hostProps})
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)


def updateHostRegistration(novaUrl, token, host_name, hostProps):
    #print 'ENTER updateHostRegistration'
    """Originally, this did not provide the 'registration' level for
    'hostProps', which is inconsistent with both 'registerHmc' and
    'updateHmcRegistration'.  So, now we provide it if needed.  The
    reason for not just providing it in all cases was concern for legacy
    code that is already providing the 'registration' level.
    """
    reg_key = 'registration'
    if reg_key not in hostProps:
        hostProps = {reg_key: hostProps}
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + '/os-hosts/' + \
        host_name + '/update-registration'
    putBody = json.dumps({'host': hostProps})
    headers = {'X-Auth-Token': token}
    return restUtils.putJSON(address, url, putBody, headers)


def deleteHost(novaUrl, token, host_name):
    #print 'ENTER deleteHost'
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + \
        '/os-hosts/' + host_name
    headers = {'X-Auth-Token': token}
    return restUtils.request('DELETE', address, url, headers)


def listPlacementPolicies(novaUrl, token):
    #print 'ENTER listPlacementPolicies'
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + '/ego/policy/placement'
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def showPlacementPolicy(novaUrl, token, policy_id):
    #print 'ENTER showPlacementPolicy'
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + \
        '/ego/policy/placement/' + str(policy_id)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def updatePlacementPolicy(novaUrl, token, policy_id, policyProps):
    #print 'ENTER updatePlacementPolicy'
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + \
        '/ego/policy/placement/' + str(policy_id)
    putBody = json.dumps({'placement_policy': policyProps})
    headers = {'X-Auth-Token': token}
    return restUtils.putJSON(address, url, putBody, headers)


def HostMaintence(novaUrl, token, host_name, hyperProps):

    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + '/ego/prs/hypervisor_maintenance/' + host_name
    headers = {'X-Auth-Token': token}
    putBody = json.dumps({'Maintenance': hyperProps})
    return restUtils.putJSON(address, url, putBody, headers)

### PowerVC HMC Host Registration Extensions ###


def registerHmc(novaUrl, token, hmcProps):
    '''
    This method handles REST POST request register an HMC with
    PowerVC. Body should contain access_ip, user_id, password,
    and optionally the hmc_display_name.
    :param novaUrl: Url for nova
    :param token: authentication token id
    :returns: dictionary containing the registration info
    '''
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + '/ibm-hmcs'
    putBody = json.dumps({'hmc': {'registration': hmcProps}})
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, putBody, headers)


def unregisterHmc(novaUrl, token, name):
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + '/ibm-hmcs/' + name
    headers = {'X-Auth-Token': token}
    return restUtils.request('DELETE', address, url, headers)

def Hmcs_details(novaUrl, token):
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + '/ibm-hmcs'+'/detail'
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)

def newunregisterationHmc(novaUrl, token, hmcid):
    address = openstackUtils.parseAddress(novaUrl)
    url = HMCS_IDS % (openstackUtils.parseBaseURL(novaUrl, address),hmcid)
    headers = {'X-Auth-Token': token}
    return restUtils.request('DELETE', address, url, headers)


def listexistingHosts(novaUrl, token):
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl,address) + '/os-hypervisors/' + '/detail?include_remote_restart_enabled=true'
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def unregisterneoHostwithpvc(novaUrl, token, host_name):
    #print 'ENTER deleteHost'
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + \
        '/os-hosts/' + host_name + '/uninstall'
    headers = {'X-Auth-Token': token}
    return restUtils.request('DELETE', address, url, headers)

def updateHmcRegistration(novaUrl, token, name, hmcProps):
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + '/ibm-hmcs/' + name
    headers = {'X-Auth-Token': token}
    putBody = json.dumps({'registration': hmcProps})
    return restUtils.putJSON(address, url, putBody, headers)


def listHmcs(novaUrl, token):
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + '/ibm-hmcs'
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def showHmc(novaUrl, token, name):
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + '/ibm-hmcs/' + name
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)

def listHmcHosts(novaUrl, token, name):
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl,
                                    address) + '/ibm-hmcs/' + name + '/hosts'
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)

### PowerVC Onboarding Extensions ###

def addSCGtoFlavor(novaUrl, token, flavor_id, scg_id):
    #print 'ENTER showFlavor'
    address = openstackUtils.parseAddress(novaUrl)
    url = FLAVS_ID % (openstackUtils.parseBaseURL(novaUrl, address),
                      flavor_id + '/os-extra_specs')

    postBody = json.dumps({'extra_specs': scg_id})
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)

def getSCGs(novaUrl, token):
    #print 'ENTER showFlavor'
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + '/storage-connectivity-groups'
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)

def createSCGs(novaUrl, token, scg_props):
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + '/storage-connectivity-groups'
    postBody = json.dumps({'storage_connectivity_group': scg_props})
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)

def listUnmanagedServers(novaUrl, token, hostName):
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl,
                                    address) + \
                                    '/os-hosts/' + hostName + '/all-servers'
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def onboardUnmanagedServers(novaUrl, token, hostName, serversProps):
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl,
                                    address) + \
                                    '/os-hosts/' + hostName + '/onboard'
    postBody = json.dumps({'servers': serversProps})
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)


def listOnboardingTasks(novaUrl, token, hostName):
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl,
                                    address) + '/os-hosts/' + hostName +\
                                    '/onboard'
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def showOnboardingTaskDetails(novaUrl, token, hostName, id):
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl,
                                    address) + '/os-hosts/' + hostName +\
                                    '/onboard/' + str(id)
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)


def unmanageServers(novaUrl, token, hostName, serverProps):
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + \
        '/os-hosts/' + hostName + '/unmanage'
    postBody = json.dumps(serverProps)
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)

### PowerVC Storage Provider Registration Extensions ###


def listVIOSClusters(novaUrl, token, hmcName):
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + \
        '/ibm-hmcs/' + hmcName +\
                                    '/ssps'
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)

#### PowerVC HMC and Host Registrations ####

def register_hmc(novaUrl, token, hmc_ip_list, hmc_userid_list, hmc_password_list, hmc_disp_name):

        hmcProps = {'access_ip': hmc_ip_list,
                    'user_id': hmc_userid_list,
                    'password': hmc_password_list,
                    'hmc_display_name': hmc_disp_name
                    }
        print(("Registering HMC:", str(hmcProps)))
        print(token)

        address = openstackUtils.parseAddress(novaUrl)
        url = openstackUtils.parseBaseURL(novaUrl, address) + '/ibm-hmcs'
        putBody = json.dumps({'hmc': {'registration': hmcProps}})
        print(putBody)
        headers = {'X-Auth-Token': token}
        registrnRespns, registrnRespnsBodyJSON = restUtils.postJSON(address, url, putBody, headers)

        print("Registration of HMC response:")
        return str(registrnRespnsBodyJSON)


def register_host(novaUrl, token, hmc_disp_name, host_name_list, host_display_name_list):

        address = openstackUtils.parseAddress(novaUrl)
        hmc_name = hmc_disp_name
        hmc_uuid = getHMC_uuid(hmc_name, novaUrl, address, token)
        host_name_list = host_name_list
        host_display_name_list = host_display_name_list

        for h in range(len(host_name_list)):

            host_name, host_display_name = host_name_list[h], host_display_name_list[h]

            hostProps = {'host_type': 'powervm',
                     'host_name': host_name,
                     'host_display_name': host_display_name,
                     'hmc_uuids': [hmc_uuid]
                     }
            print(hostProps)
            registrnRespns, registrnRespnsBodyJSON = createHost(novaUrl, token, hostProps)
            print("Registration of Host response:")
            print((str(registrnRespnsBodyJSON)))

        return registrnRespns

## Nova&kvm host registration
def registerNeohosts(novaUrl, token, hostProps):

    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + '/os-hosts'
    putBody = json.dumps({'host': {'registration': hostProps}})
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, putBody, headers)

## Function to create compute template
def createComputeTemplate(novaUrl, token, flavorProps):

    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + '/flavors'
    putBody = json.dumps({'flavor': flavorProps})
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, putBody, headers)

## Function to create compute template os-extra_specs
def createComputeTemplateAdvance(novaUrl, token, flavorProps, computeID):

    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + '/flavors/' + computeID + '/os-extra_specs'
    putBody = json.dumps({'extra_specs': flavorProps})
    headers = {'X-Auth-Token': token}
    print(url)
    print(putBody)
    return restUtils.postJSON(address, url, putBody, headers)

# nova ssh key pair generation
def createKeyPair(novaUrl, token, keyProps):
    #print 'ENTER createServer'
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + '/os-keypairs'
    postBody = json.dumps({'keypair': keyProps})
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, postBody, headers)

def addPPTRatioToFlavor(novaUrl, token, flavorID, pptRatiovalue):
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + '/flavors/' + flavorID + '/os-extra_specs' + '/powervm:ppt_ratio'
    postBody = json.dumps({'powervm:ppt_ratio': pptRatiovalue})
    print(url)
    print(postBody)
    headers = {'X-Auth-Token': token}
    return restUtils.putJSON(address, url, postBody, headers)

def deletePPTRatioToFlavor(novaUrl, token, flavorID):
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + '/flavors/' + flavorID + '/os-extra_specs' + '/powervm:ppt_ratio'
    print(url)
    headers = {'X-Auth-Token': token}
    return restUtils.request('DELETE', address, url, headers)
