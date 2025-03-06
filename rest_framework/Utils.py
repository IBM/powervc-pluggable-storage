'''
Created on Oct 11, 2013

@author: djurgens
'''
from rest_framework import novaUtils
from rest_framework import glanceUtils
from rest_framework import quantumUtils
from rest_framework import cinderUtils
from rest_framework.restUtils import HttpError
import sys
from datetime import datetime
from datetime import timedelta
import time
import string
import operator
import ssl
import os
#pip install ipaddr (for install ipaddr)
try:
    import ipaddr
except ImportError:
    print ("pip install ipaddr (for install ipaddr to do IPV6 test)")

DEFAULT_SLEEP_INTERVAL_SECS = 3
DEFAULT_TIMEOUT_SECS = 180


def find_all_VMs(self, novaUrl, authent_id):
    try:
        serverListResponse, serverList = \
            novaUtils.listServerSummaries(novaUrl, authent_id)
        return serverList
    except HttpError as e:
        print('HTTP Error: {0}'.format(e.body))
        raise e


def delete_server(authTokenId, novaUrl, server):
    try:
        novaUtils.deleteServer(novaUrl, authTokenId, server['id'])
    except HttpError as e:
        print('Http Error {0}'.format(e.body))

def host_maintenence(auth_id, novaUrl, server, actionProps):
        print('ENTER Utils:host_maintenence')
        response, body = novaUtils.host_maintenence_mode(novaUrl, auth_id, server, actionProps)
def remote_restart_by_host(auth_id, novaUrl, server, actionProps):
        print('ENTER Utils:remote_restart_by_host')
        response, body = novaUtils.remote_restart_host(novaUrl, auth_id, server, actionProps)
def remote_restart_by_server(auth_id, novaUrl, server, actionProps):
        try:
                print('ENTER Utils:remote_restart_by_server')
                response, body = novaUtils.remote_restart_server(novaUrl, auth_id, server, actionProps)
                print("Response", response)
                print("Body", body)
        except HttpError as e:
                print('Http Error {0}'.format(e.body))


def start_server(authTokenId, novaUrl, server,
                 timeout=None, sleep_interval=None):
    if timeout is None:
        timeout = DEFAULT_TIMEOUT_SECS
    if sleep_interval is None:
        sleep_interval = DEFAULT_SLEEP_INTERVAL_SECS
    serverState = get_server_state(authTokenId, novaUrl, server)
    result = False
    if (serverState != 'active' and
            serverState != 'error'):
        send_start_server_request(authTokenId, novaUrl, server)
        result = wait_for_server_state(authTokenId, novaUrl, server,
                                       'active', timeout, sleep_interval)
    elif serverState == 'active':
        result = True
    return result


def stop_server(authTokenId, novaUrl, server,
                timeout=None, sleep_interval=None):
    if timeout is None:
        timeout = DEFAULT_TIMEOUT_SECS
    if sleep_interval is None:
        sleep_interval = DEFAULT_SLEEP_INTERVAL_SECS
    serverState = get_server_state(authTokenId, novaUrl, server)
    result = False
    if serverState == 'active':
        send_stop_server_request(authTokenId, novaUrl, server)
        result = wait_for_server_state(authTokenId, novaUrl, server,
                                       'stopped', timeout, sleep_interval)
    elif serverState == 'stopped':
        result = True
    return result


def send_start_server_request(authTokenId, novaUrl, server):
    actionProps = {'os-start': None}
    response, body = novaUtils.createServerAction(novaUrl, authTokenId,
                                                  server['id'], actionProps)


def send_stop_server_request(authTokenId, novaUrl, server):
    actionProps = {'os-stop': None}
    response, body = novaUtils.createServerAction(novaUrl, authTokenId,
                                                  server['id'], actionProps)


def get_server_status_dict(authTokenId, novaUrl, server):
    '''Returns the value of the following items from a Server Details:
    task_state: server['OS-EXT-STS:task_state']
    vm_state: server['OS-EXT-STS:vm_state']
    power_state = server['OS-EXT-STS:power_state']
    host = server['OS-EXT-SRV-ATTR:host']
    health_value = server['health_status']['health_value']
    '''
    serverStatus = dict()
    for i in range(5):
        try:
            responseTuple = novaUtils.showServer(novaUrl, authTokenId,
                                                 server['id'])
            if responseTuple and responseTuple[1] and\
                'server' in responseTuple[1]:
                break
        except ssl.SSLError as e:
            time.sleep(1)
            if i == 4:
                print('SSLError: {0}'.format(e))
                raise e
        except HttpError as e:
            if e.code == 404:
                raise e
            else:
                if i == 4:
                    print('{0}'.format(e))
                    raise e
                else:
                    continue
        except Exception as err:
            if i == 4:
                print('{0}'.format(err))
                raise err
    servDetail = None
    if responseTuple[1] and 'server' in responseTuple[1]:
        servDetail = responseTuple[1]['server']
    if servDetail and 'OS-EXT-STS:task_state' in servDetail:
        serverStatus['task_state'] = servDetail['OS-EXT-STS:task_state']
    if servDetail and 'OS-EXT-STS:vm_state' in servDetail:
        serverStatus['vm_state'] = servDetail['OS-EXT-STS:vm_state']
    if servDetail and 'OS-EXT-STS:power_state' in servDetail:
        serverStatus['power_state'] = servDetail['OS-EXT-STS:power_state']
    if servDetail and 'OS-EXT-SRV-ATTR:host' in servDetail:
        serverStatus['host'] = servDetail['OS-EXT-SRV-ATTR:host']
    if servDetail and 'health_status' in servDetail:
        if servDetail['health_status'].get("health_value"):
            serverStatus['health_value'] = \
                servDetail['health_status']['health_value']
        else:
                serverStatus['health_value'] = ""
    return serverStatus
def get_server_host_status_dict(authTokenId, novaUrl, server):
    '''Returns the value of the following items from a Server Details:
    task_state: server['OS-EXT-STS:task_state']
    vm_state: server['OS-EXT-STS:vm_state']
    power_state = server['OS-EXT-STS:power_state']
    host = server['OS-EXT-SRV-ATTR:hypervisor_hostname']
    health_value = server['health_status']['health_value']
    '''
    serverStatus = dict()
    for i in range(5):
        try:
            responseTuple = novaUtils.showServer(novaUrl, authTokenId,
                                                 server['id'])
            if responseTuple and responseTuple[1] and\
                'server' in responseTuple[1]:
                break
        except ssl.SSLError as e:
            time.sleep(1)
            if i == 4:
                print('SSLError: {0}'.format(e))
                raise e
        except HttpError as e:
            if e.code == 404:
                raise e
            else:
                if i == 4:
                    print('{0}'.format(e))
                    raise e
                else:
                    continue
        except Exception as err:
            if i == 4:
                print('{0}'.format(err))
                raise err
    servDetail = None
    if responseTuple[1] and 'server' in responseTuple[1]:
        servDetail = responseTuple[1]['server']
    if servDetail and 'OS-EXT-STS:task_state' in servDetail:
        serverStatus['task_state'] = servDetail['OS-EXT-STS:task_state']
    if servDetail and 'OS-EXT-STS:vm_state' in servDetail:
        serverStatus['vm_state'] = servDetail['OS-EXT-STS:vm_state']
    if servDetail and 'OS-EXT-STS:power_state' in servDetail:
        serverStatus['power_state'] = servDetail['OS-EXT-STS:power_state']
    if servDetail and 'OS-EXT-SRV-ATTR:hypervisor_hostname' in servDetail:
        serverStatus['host'] = servDetail['OS-EXT-SRV-ATTR:hypervisor_hostname']
    #print servDetail;
    if servDetail and 'health_status' in servDetail:
        if servDetail['health_status'].get("health_value"):
            serverStatus['health_value'] = \
                servDetail['health_status']['health_value']
        else:
                serverStatus['health_value'] = ""
    return serverStatus

def get_server_status_dict_host(authTokenId, novaUrl, server, host_id):
    '''Returns the value of the following items from a Server Details:
    task_state: server['OS-EXT-STS:task_state']
    vm_state: server['OS-EXT-STS:vm_state']
    power_state = server['OS-EXT-STS:power_state']
    host = server['OS-EXT-SRV-ATTR:host']
    health_value = server['health_status']['health_value']
    '''
    serverStatus = dict()
    for i in range(5):
        try:
            responseTuple = novaUtils.showServer(novaUrl, authTokenId,
                                                 server['id'], host_id)
            if responseTuple and responseTuple[1] and\
                'server' in responseTuple[1]:
                break
        except ssl.SSLError as e:
            time.sleep(1)
            if i == 4:
                print('SSLError: {0}'.format(e))
                raise e
        except HttpError as e:
            if e.code == 404:
                raise e
            else:
                if i == 4:
                    print('{0}'.format(e))
                    raise e
                else:
                    continue
        except Exception as err:
            if i == 4:
                print('{0}'.format(err))
                raise err
    servDetail = None
    if responseTuple[1] and 'server' in responseTuple[1]:
        servDetail = responseTuple[1]['server']
    if servDetail and 'OS-EXT-STS:task_state' in servDetail:
        serverStatus['task_state'] = servDetail['OS-EXT-STS:task_state']
    if servDetail and 'OS-EXT-STS:vm_state' in servDetail:
        serverStatus['vm_state'] = servDetail['OS-EXT-STS:vm_state']
    if servDetail and 'OS-EXT-STS:power_state' in servDetail:
        serverStatus['power_state'] = servDetail['OS-EXT-STS:power_state']
    if servDetail and 'OS-EXT-SRV-ATTR:host' in servDetail:
        serverStatus['host'] = servDetail['OS-EXT-SRV-ATTR:host']
    print(servDetail);
    if servDetail and 'health_status' in servDetail:
        if servDetail['health_status'].get("health_value"):
            serverStatus['health_value'] = \
                servDetail['health_status']['health_value']
        else:
                serverStatus['health_value'] = ""
    return serverStatus

def get_host_list(authTokenId, novaUrl):
    print('Running novaUtils.listHosts')
    for i in range(5):
        try:
            responseTuple = novaUtils.listHypervisorDetails(novaUrl, authTokenId)
            if responseTuple and responseTuple[1] and\
                'hypervisors' in responseTuple[1]:
                break
        except ssl.SSLError as e:
            print('SSLError: {0}'.format(e))
            time.sleep(1)
            if i == 4:
                raise
    hypDetail = None
    if responseTuple[1] and 'hypervisors' in responseTuple[1]:
        hypDetail = responseTuple[1]['hypervisors']
    return hypDetail
def get_host_status(authTokenId, novaUrl, host_name):
    """Returns the value of the server's state for the given state-type.
    """
    hostStatus = {'hypervisor_hostname' : None, 'status' : None, 'state' : None, 'maintenance_migrate_action' : None }
    for i in range(5):
        try:
            responseTuple = novaUtils.listHypervisorDetails(novaUrl, authTokenId)
            if responseTuple and responseTuple[1] and\
                'hypervisors' in responseTuple[1]:
                break
        except ssl.SSLError as e:
            print('SSLError: {0}'.format(e))
            time.sleep(1)
            if i == 4:
                raise
    hypDetail = None
    if responseTuple[1] and 'hypervisors' in responseTuple[1]:
        hypDetail = responseTuple[1]['hypervisors']
    for hdetail in hypDetail:
        if hdetail['hypervisor_hostname'] == host_name:
                hostStatus['hypervisor_hostname'] = hdetail['hypervisor_hostname']
                hostStatus['status'] = hdetail['status']
                hostStatus['state'] = hdetail['state']
                hostStatus['maintenance_migrate_action'] = hdetail['maintenance_migrate_action']
    return hostStatus

def get_server_state(authTokenId, novaUrl, server, state_type='vm_state'):
    """Returns the value of the server's state for the given state-type.

    :param state_type: Alternate state-types: 'task_state', 'power_state'
    """
    serverState = None
    for i in range(5):
        try:
            response, body = \
                novaUtils.showServer(novaUrl, authTokenId, server['id'])
            if response and body:
                break
        except ssl.SSLError as e:
            print('SSLError: {0}'.format(e.body))
            time.sleep(1)
            if i == 4:
                raise
    if body:
        serverState = body['server']['OS-EXT-STS:' + state_type]
    return serverState


def get_server_state_and_health(token, novaUrl, server, state_type='vm_state'):
    ''' Returns the value of the server's state for the give state-type
    and the value of the health_status
    :param state_type: Alternate state-types: 'task_state', 'power_state'
    '''
    serverState = None
    health_status = dict()
    for i in range(5):
        try:
            response, body = \
                novaUtils.showServer(novaUrl, token, server['id'])
            if response and body:
                break
        except ssl.SSLError as e:
            print('SSLError: {0}'.format(e))
            time.sleep(1)
            if i == 4:
                raise e
    if body:
        if 'server' in body:
            serverState = body['server']['OS-EXT-STS:' + state_type]
            health_status = body['server']['health_status']
    return serverState, health_status


def get_migration_status(token, novaUrl, server, from_host, to_host):
    for i in range(5):
        try:
            response, body = \
                novaUtils.showServer(novaUrl, token, server['id'])
            if response and body:
                break
        except ssl.SSLError as e:
            print('SSLError: {0}'.format(e.body))
            time.sleep(1)
            if i == 4:
                raise e
    trace = 'vm_state:{0} task_state:{1} power_state:{2} host:{3} health:{4}'
    if body and 'server' in body:
        server = body['server']
        vm_state = server['OS-EXT-STS:vm_state']
        task_state = server['OS-EXT-STS:task_state']
        power_state = server['OS-EXT-STS:power_state']
        host = server['OS-EXT-SRV-ATTR:host']
        health = server['health_status']['health_value']
        print(trace.format(vm_state, task_state, power_state, host, health))
        if vm_state == 'error':
            return 'error'
        elif task_state == None:
            if vm_state == 'active':
                if health == 'OK':
                    if power_state == 1:
                        if host != from_host:
                            return 'success'
                        else:
                            return 'failed'
        return 'waiting'


def wait_for_server_state(authTokenId, novaUrl, server, state, timeout,
                          sleep_interval, state_type='vm_state'):
    serverState = get_server_state(authTokenId, novaUrl, server)
    if serverState == state:
        return True
    elif serverState == 'error':
        return False
    start = datetime.now()
    delta = timedelta(seconds=timeout)
    while datetime.now() < start + delta:
        time.sleep(sleep_interval)
        serverState = get_server_state(authTokenId, novaUrl, server,
                                       state_type)
        print('---Server={0}, State={1}'.format(server['name'], serverState))
        if serverState == state:
            return True
        elif serverState == 'error':
            return False
    return False


def get_host_storage_topo_list(authTokenId, novaUrl):
    responseTuple = novaUtils.listHostStorageTopo(novaUrl, authTokenId)
    host_storage_topo_list = responseTuple[1]['host_list']
    return host_storage_topo_list


def get_server_list(authTokenId, novaUrl):
    responseTuple = novaUtils.listServerSummaries(novaUrl, authTokenId)
    server_list = responseTuple[1]['servers']
    return server_list


def get_server_list_host(authTokenId, novaUrl, host_src):
    responseTuple = novaUtils.listServerSummaries_host(novaUrl,
                                                       authTokenId, host_src)
    server_list = responseTuple[1]['servers']
    return server_list

def get_server_dets(authTokenId, novaUrl):
    responseTuple = novaUtils.listServerDetails(novaUrl, authTokenId)
    servers_detail_list = responseTuple[1]['servers']
    return servers_detail_list


def get_server_details(authTokenId, novaUrl,
                       fields=['name', 'id', 'created', 'addresses']):
    responseTuple = novaUtils.listServerDetails(novaUrl, authTokenId)
    servers_detail_list = responseTuple[1]['servers']
    details_list = []
    if fields == ['*ALL'] or '*ALL' in fields:
        details_list = servers_detail_list
    else:
        for server in servers_detail_list:
            server_dict = {}
            for key in fields:
                server_dict[key] = server[key]
            details_list.append(server_dict)

    return details_list


def get_server(authTokenId, novaUrl, server_id, fields=['*ALL']):
    responseTuple = novaUtils.showServer(novaUrl, authTokenId, server_id)
    if responseTuple and 'server' in responseTuple[1]:
        if fields == ['*ALL']:
            return responseTuple[1]['server']
        else:
            server = {}
            for key in fields:
                if key in responseTuple[1]['server']:
                    server[key] = responseTuple[1]['server'][key]
            return server
    else:
        return None



def get_image(cls, tester, name):
    authTokenId = tester.authent_id
    glanceUrl = tester.getServiceUrl('image')
    imageRef = None
    listImagesResponse, listImagesResponseBodyJSON = \
        glanceUtils.listImages(glanceUrl, authTokenId)

    for image in listImagesResponseBodyJSON['images']:
        print('image name=', image['name'])
        if image['name'] == name:
            imageRef = image['id']
            print('Image for {0} found: {1}'.format(name, imageRef))
    return imageRef


def get_flavor_list(authTokenId, novaUrl):
    responseTuple = novaUtils.listFlavorSummaries(novaUrl, authTokenId)
    flavor_list = responseTuple[1]['flavors']
    return flavor_list


def get_flavor(authTokenId, novaUrl, flavor_id):
    reponseTuple = novaUtils.showFlavor(novaUrl, authTokenId, flavor_id)
    flavor = reponseTuple[1]['flavor']
    return flavor


def wait_for_server_deletion(authTokenId, novaUrl, server,
                             timeout, sleep_interval):
    start = datetime.now()
    delta = timedelta(seconds=timeout)
    while datetime.now() < start + delta:
        server_list = get_server_list(authTokenId, novaUrl)
        foundServer = None
        for serverx in server_list:
            if serverx['id'] == server['id']:
                foundServer = serverx
                break
        if not foundServer:
            return True
    if foundServer:
        return False
    else:
        return True


def stop_all_servers(authTokenId, novaUrl, server_list, timeout=None,
                 sleep_interval=None):
    count = 0
    for server in server_list:
        try:
            result = stop_server(authTokenId, novaUrl, server, timeout,
                                 sleep_interval)
            if result:
                count += 1
        except HttpError as err:
            print('HTTP Error: {0}'.format(err.body))
    return count


def start_all_servers(authTokenId, novaUrl, server_list, timeout=None,
                      sleep_interval=None):
    count = 0
    for server in server_list:
        try:
            result = start_server(authTokenId, novaUrl, server, timeout,
                                  sleep_interval)
            if result:
                count += 1
        except HttpError as err:
            print('HTTP Error: {0}'.format(err.body))
    return count


def unique_server_name(name_prefix, ip_address):
    if not ip_address:
        return None
    ip_octet_list = ip_address.split('.', 4)
    for i in range(len(ip_octet_list)):
        ip_octet_list[i] = ip_octet_list[i].zfill(3)

    suffix_list = ip_octet_list[2:4]
    unique_name = name_prefix + '_' + '_'.join(suffix_list)
    return unique_name


def create_server(authTokenId, novaUrl, imageRef, name, ip, network_id,
                  flavor_id=2, host_name=None):
    server_name = name
    vm_entry = {
                "name": server_name,
                "imageRef": imageRef,
                "max_count": 1,
                "min_count": 1,
                "networks": [
                             {
                              "fixed_ip": ip,
                              "uuid": network_id,
                             }
                            ],
                "flavorRef": flavor_id
               }
    if host_name:
        vm_entry['availability_zone'] = ':' + host_name

    response, bodyJSON = \
        novaUtils.createServer(novaUrl, authTokenId, vm_entry)
    server = None
    host_key = 'OS-EXT-SVRS-ATTR:host'
    server = {'name': name, 'id': bodyJSON['server']['id']}
    return server


def create_vscsi_scg(authent_id, novaUrl, viosid, scgName, bdConnect):
    boot_data = bdConnect.lower()
    bdc = 'pv_'+boot_data
    scg_props = {
                    "display_name": scgName,
                    "fc_storage_access": "false",
                    "auto_add_vios": "true",
                    "include_untagged": "false",
                    "enabled": "true",
                    "vios_ids": viosid,
                    "exact_redundancy": "false",
                    "vios_redundancy": 1,
                    "boot_connectivity": [bdc],
                    "data_connectivity": [bdc]
                }
    print(scg_props)
    scg_response, scg_dict = novaUtils.createSCGs(novaUrl, authent_id, scg_props)
    return scg_response


def create_npiv_scg(authent_id, novaUrl, viosid, scgName, bdConnect):
    boot_data = bdConnect.lower()
    scg_props = {
                    "display_name": scgName,
                    "fc_storage_access": "true",
                    "auto_add_vios": "true",
                    "include_untagged": "false",
                    "enabled": "true",
                    "vios_ids": viosid,
                    "exact_redundancy": "false",
                    "vios_redundancy": 1,
                    "fabric_set_req": "at_least_one",
                    "fabric_set_npiv": ["*"],
                    "ports_per_fabric_npiv": 1,
                    "boot_connectivity": [boot_data],
                    "data_connectivity": [boot_data]
                }
    print(scg_props)
    scg_response, scg_dict = novaUtils.createSCGs(novaUrl, authent_id, scg_props)
    return scg_response

def generate_npiv_scg(authent_id, novaUrl, viosid, scgName, bdConnect, ddConnect):
    boot_data = bdConnect.lower()
    data_disk = ddConnect.lower()
    scg_props = {
                    "display_name": scgName,
                    "fc_storage_access": "true",
                    "auto_add_vios": "true",
                    "include_untagged": "false",
                    "enabled": "true",
                    "vios_ids": viosid,
                    "exact_redundancy": "false",
                    "vios_redundancy": 1,
                    "fabric_set_req": "at_least_one",
                    "fabric_set_npiv": ["*"],
                    "ports_per_fabric_npiv": 1,
                    "boot_connectivity": [boot_data],
                    "data_connectivity": [data_disk]
                }
    print(scg_props)
    scg_response, scg_dict = novaUtils.createSCGs(novaUrl, authent_id, scg_props)
    return scg_response

def generate_vscsi_scg(authent_id, novaUrl, viosid, scgName, bd_Connect,dd_Connect):
    boot_data = bd_Connect.lower()
    data_disk = dd_Connect.lower()
    bdc = 'pv_'+data_disk
    ddc = 'pv_'+boot_data
    scg_props = {
                    "display_name": scgName,
                    "fc_storage_access": "false",
                    "auto_add_vios": "true",
                    "include_untagged": "false",
                    "enabled": "true",
                    "vios_ids": viosid,
                    "exact_redundancy": "false",
                    "vios_redundancy": 1,
                    "boot_connectivity": [bdc],
                    "data_connectivity": [ddc]
                }
    print(scg_props)
    scg_response, scg_dict = novaUtils.createSCGs(novaUrl, authent_id, scg_props)
    return scg_response

def generate_vscsi_npiv_scg(authent_id, novaUrl, viosid, scgName, bd_Connect,dd_Connect):
    boot_data = bd_Connect.lower()
    data_disk = dd_Connect.lower()
    bdc = 'pv_'+boot_data
    ddc = data_disk
    scg_props = {
                    "display_name": scgName,
                    "fc_storage_access": "true",
                    "auto_add_vios": "true",
                    "include_untagged": "false",
                    "enabled": "true",
                    "vios_ids": viosid,
                    "exact_redundancy": "false",
                    "vios_redundancy": 1,
            "fabric_set_req": "at_least_one",
            "fabric_set_npiv": ["*"],
            "ports_per_fabric_npiv": 1,
                    "boot_connectivity": [bdc],
                    "data_connectivity": [ddc]
                }
    print(scg_props)
    scg_response, scg_dict = novaUtils.createSCGs(novaUrl, authent_id, scg_props)
    return scg_response



def create_server_with_key(authTokenId, novaUrl, imageRef, name, ip, network_id,
                  flavor_id=2, host_name=None):
    server_name = name
    key_Props = {
                 "name": server_name
                }

    response, bodyJSON = \
        novaUtils.createKeyPair(novaUrl, authTokenId, key_Props)

    vm_entry = {
                "name": server_name,
                "imageRef": imageRef,
                "max_count": 1,
                "min_count": 1,
                "key_name":server_name,
                "networks": [
                             {
                              "fixed_ip": ip,
                              "uuid": network_id,
                             }
                            ],
                "flavorRef": flavor_id,

               }
    if host_name:
        vm_entry['availability_zone'] = ':' + host_name

    response, bodyJSON = \
        novaUtils.createServer(novaUrl, authTokenId, vm_entry)
    server = None
    host_key = 'OS-EXT-SVRS-ATTR:host'
    if bodyJSON and 'server' in bodyJSON:
        server = {'name': name, 'id': bodyJSON['server']['id']}
    return server

def create_server_sriov(authTokenId, novaUrl, neutronUrl, imageRef, name, ip, network_id, sriov_capacity, sriov_vnic_required_vfs,
                  flavor_id=2, host_name=None):
    print(novaUrl)
    sriov_port_Props = {
                 "name":"powervc_attached",
                 "network_id": network_id,
                 "fixed_ips":[{"ip_address":ip}],
                 "binding:vnic_type":"direct",
                 "binding:profile":{"delete_with_instance":1,"vnic_required_vfs":sriov_vnic_required_vfs,"capacity":sriov_capacity}
                }

    response, bodyJSON = \
        quantumUtils.createSriovPorts(neutronUrl, authTokenId, sriov_port_Props)
    print(bodyJSON['port']['id'])
    sriov_port = bodyJSON['port']['id']

    vm_entry = {
                "name": name,
                "imageRef": imageRef,
                "max_count": 1,
                "min_count": 1,
                "networks": [
                             {
                              "port":sriov_port
                             }
                            ],
                "flavorRef": flavor_id,

               }
    if host_name:
        vm_entry['availability_zone'] = ':' + host_name

    response, bodyJSON = \
        novaUtils.createServer(novaUrl, authTokenId, vm_entry)
    server = None
    host_key = 'OS-EXT-SVRS-ATTR:host'
    if bodyJSON and 'server' in bodyJSON:
        server = {'name': name, 'id': bodyJSON['server']['id']}
    return server

""" new create_server module for deploying multidisk VMS """
def create_server_md(authTokenId, novaUrl, imageRef, name, ip, network_id,block_device_mapping_list,
                  host_aggregate_id, collocation_rule_id, flavor_id=2, host_name=None ):
    print("entering create_server_md")
    server_name = name
    vm_entry = {
                "name": server_name,
                "imageRef": imageRef,
                "max_count": 1,
                "min_count": 1,
                "networks": [
                             {
                              "fixed_ip": ip,
                              "uuid": network_id,
                             }
                            ],
                "flavorRef": flavor_id,
                "block_device_mapping_v2" : block_device_mapping_list
                }

    if host_name:
        vm_entry['availability_zone'] = ':' + host_name

    scheduler_hints_value = {
                                            "host_aggregate_id":
                                            str(host_aggregate_id),
                                            "group": str(collocation_rule_id)
                            }
    vm_entry = {'server': vm_entry,
                'os:scheduler_hints': scheduler_hints_value}

    response, bodyJSON = \
        novaUtils.createServer(novaUrl, authTokenId, json.dumps(vm_entry))
    server = None
    host_key = 'OS-EXT-SVRS-ATTR:host'
    if bodyJSON and 'server' in bodyJSON:
        server = {'name': name, 'id': bodyJSON['server']['id']}
    return server

def get_named_image(authTokenId, glanceUrl, image_name):
    imageRef = None
    response, bodyJSON = glanceUtils.listImages(glanceUrl, authTokenId)

    for image in bodyJSON['images']:
        if image['name'] == image_name:
            imageRef = image['id']
    return imageRef


def get_named_network_id(authTokenId, quantumUrl, network_name):
    networkId = None
    response, bodyJSON = quantumUtils.listNetworks(quantumUrl, authTokenId)
    for network in bodyJSON['networks']:
        if network['name'] == network_name:
            print('network=', network)
            networkId = network['id']
    return networkId

def get_subnet_id(authTokenId, quantumUrl, network_id):
    response, bodyJSON = quantumUtils.showNetwork(quantumUrl, authTokenId, network_id)
    subnet_id = bodyJSON['network']['subnets']
    return subnet_id[0]

def get_netmask(authTokenId, quantumUrl, network_id, ip_address):
    response, bodyJSON = quantumUtils.showNetwork(quantumUrl, authTokenId,
                                                      network_id)
    if bodyJSON and 'network' in bodyJSON and 'subnets' in bodyJSON['network']:
        subnets = bodyJSON['network']['subnets']
        for subnet_id in subnets:
            responseTuple = quantumUtils.showSubnet(quantumUrl, authTokenId,
                                                    subnet_id)
            if responseTuple and 'subnet' in responseTuple[1]:
                subnet = responseTuple[1]['subnet']
                base_ip, netmask_list = \
                    netmask_from_cidr(subnet['cidr'])
                s1 = get_subnet_list(base_ip, netmask_list)
                ip_list = ip_as_list(ip_address)
                s2 = get_subnet_list(ip_list, netmask_list)
                if s1 == s2:
                    temp = []
                    for i in range(len(netmask_list)):
                        temp.append(str(netmask_list[i]))
                    netmask = '.'.join(temp)
                    return netmask
    return None


def next_ip(start_ip, netmask, incr):
    ip_list = ip_as_list(start_ip)
    netmask_list = ip_as_list(netmask)
    subnet_list = get_subnet_list(ip_list, netmask_list)
    new_ip_list = increment_ip(ip_list, netmask_list, incr)
    if new_ip_list:
        temp = []
        for i in range(len(new_ip_list)):
            temp.append(str(new_ip_list[i]))
        ip = '.'.join(temp)
        return ip
    else:
        return None


def ip_as_list(ip):
    str_list = ip.split('.', 4)
    ip_list = []
    for i in range(len(str_list)):
        ip_list.append(int(str_list[i]))
    return ip_list


def netmask_from_cidr(cidr):
    cidr_list = cidr.split('/', 2)
    cidr_one_bits = int(cidr_list[1])
    subnet_list = []
    while len(subnet_list) < 4:
        if cidr_one_bits >= 8:
            subnet_list.append(pow(2, 8) - 1)
            cidr_one_bits -= 8
        elif cidr_one_bits < 8 and cidr_one_bits > 0:
            subnet_list.append((pow(2, 8) - 1) -
                               (pow(2, 8 - cidr_one_bits) - 1))
            cidr_one_bits = 0
        elif cidr_one_bits == 0:
            subnet_list.append(0)
    return ip_as_list(cidr_list[0]), subnet_list


def get_subnet_list(ip_list, netmask_list):
    subnet_list = []
    for i in range(len(ip_list)):
        subnet_list.append(operator.and_(ip_list[i], netmask_list[i]))
    return subnet_list


def increment_ip(ip_list, netmask_list, incr):
    x = incr
    iplist = []
    iplist.extend(ip_list)
    for i in range(len(iplist) - 1, -1, -1):
        carry, new_value = divmod((iplist[i] + x), 256)
        iplist[i] = new_value
        if carry > 0:
            x = carry
        else:
            break
    subnet = get_subnet_list(ip_list, netmask_list)
    new_subnet = get_subnet_list(iplist, netmask_list)
    if subnet != new_subnet:
        return None
    else:
        return iplist

def next_ip6(start_ip, incr):
    a = ipaddr.IPv6Address(start_ip)
    print(a + incr)
    return a + incr

def ip6_as_list(ip):
    str_list = ip.split(':', 8)
    ip_list = []
    for i in range(len(str_list)):
        ip_list.append(str_list[i])
    return ip_list

def increment_ip6(ip_list, incr):
    x = incr
    iplist = []
    iplist.extend(ip_list)
    for i in range(len(iplist) - 1, -1, -1):
        carry, new_value = divmod((iplist[i] + x), 256)
        iplist[i] = new_value
        if carry > 0:
            x = carry
        else:
            break
    return iplist

def unique_server_name_ip6(name_prefix, ip_address):
    if not ip_address:
        return None
    a = ipaddr.IPv6Address(ip_address)
    print(a)
    b = str(a)
    print(b)
    ip_octet_list = b.split(':', 8)
    print(ip_octet_list)
    for i in range(len(ip_octet_list)):
        #ip_octet_list[i] = ip_octet_list[i].zfill(7)
        suffix_list = ip_octet_list[7]
        print(suffix_list)
        unique_name = name_prefix + '_' + '_'.join(suffix_list)
    return unique_name



######


def finish_onboard(authid, novaUrl, serverid, os_distro, vm_boot_vol_ids_list, endianness):

    print("\n Entering the Utils.finish_onboard method....")
    print(" ]n os_distro is : ", os_distro)
    print(" \n vm_boot_vol_ids_list is : ", vm_boot_vol_ids_list)
    print(" \n endianness is : " , endianness)


    actionProp = { "finishOnboard": {
                                        "os_distro": os_distro,
                                        "boot_volume_ids" : vm_boot_vol_ids_list,
                                         "endianness" : endianness
                                    }
                  }



    responseTuple= novaUtils.createServerAction(novaUrl, authid,
                                                 serverid,
                                                 actionProp)
    print("response=", responseTuple[0])
    return responseTuple



def migrate_server(auth_id, novaUrl, server_dict):
    actionProp = {
                    'migrate': None
                    }
    responseTuple = novaUtils.createServerAction(novaUrl, auth_id,
                                                 server_dict['id'],
                                                 actionProp)
    print("response=", responseTuple[0])
    return responseTuple

def migrate_server_1(auth_id, novaUrl, server_dict, host):
    actionProp = {
                    'migrate': {"host": host }
                    }
    responseTuple = novaUtils.createServerAction(novaUrl, auth_id,
                                                 server_dict['id'],
                                                 actionProp)

def live_migrate(auth_id, novaUrl, server, host):
    actionProps = {
                   "os-migrateLive": {
                                      "host": host,
                                      "block_migration": False,
                                      "disk_over_commit": False
                                      }
                   }
    novaUtils.createServerAction(novaUrl, auth_id, server['id'], actionProps)


def force_delete_server(auth_id, novaUrl, server):
    actionProp = {
                  "forceDelete": None
                  }
    novaUtils.createServerAction(novaUrl, auth_id,
                                                 server['id'], actionProp)


def resize_server(auth_id, novaUrl, server, new_flavor):
    print('Resize {0} to flavor {1}'.format(server['name'], new_flavor))
    actionProps = {
                   "resize": {"flavorRef": new_flavor}
                   }
    novaUtils.createServerAction(novaUrl, auth_id,
                                                 server['id'], actionProps)

def resize_server_new(auth_id, novaUrl, name, id, vcpu, ram, proc_units, disk):

    actionProps = { "resize": {"flavor":{"vcpus": vcpu,"ram":ram,"extra_specs":{"powervm:proc_units": proc_units},"disk":disk}}}
    print("printing action props")
    print(actionProps)
    novaUtils.createServerAction(novaUrl, auth_id, id, actionProps)


def isbootvolume(cinderUrl, token, volume_id):
    responseDict={}
    responseDict = cinderUtils.showVolume(cinderUrl,token,volume_id)[1]
    print("\n response dict: ,", responseDict)
    volume_detail_dict = responseDict['volume']
    print("\n volume_detail_dict: ,", volume_detail_dict)
    if 'is_boot_volume' in volume_detail_dict['metadata']:
        print("returning True")
        return True
    else:
        print("returning False")
        return False


########################################################################################################
# Below Functions are used for report generation
########################################################################################################
def Create_Status_File(FileName):
     path = os.getcwd() + '/' + 'SVT_Reports' + '/' + FileName
     print(path)
     if not os.path.exists(path):
        path2 = os.getcwd() + '/' + 'SVT_Reports'
        print(path2)
        if not os.path.exists(path2):
            os.makedirs(path2)
        os.makedirs(path)
     filenm = path + '/' + FileName + '-' + datetime.now().strftime("day_%Y-%m-%d__time_%H-%M") + '.' + 'txt'
     print(filenm)
     open(filenm,'w')
     return filenm

def Append_File_str(pathname,Text):
    if os.path.exists(pathname):
     filepy = open(pathname, "a")
     filepy.write(Text)
     #filepy.write('\n')
     filepy.close()

def Append_File_list(pathname,list):
    if os.path.exists(pathname):
     filepy = open(pathname,"a+")
     #filepy.seek(0, 0)
     filepy.writelines(list)
     #filepy.write('\n')
     filepy.close()

def Overwrite_File(pathname,Text):
    if os.path.exists(pathname):
     filepy = open(pathname,"w")
     filepy.writelines(Text)
     #filepy.write('\n')
     filepy.close()

def Report_Update(pathName, opName, total_Sucess, total_Failure, success_VM, failed_VM):
    str1 = '*' * 20 + '\n'
    total = total_Sucess + total_Failure
    Overwrite_File(pathName, "Test_Script: ")
    Append_File_str(pathName, opName)
    Append_File_str(pathName, "\n")
    Append_File_str(pathName, str1)
    Append_File_str(pathName, "Total: ")
    Append_File_str(pathName, str(total))
    Append_File_str(pathName, "\n")
    Append_File_str(pathName, "Success: ")
    Append_File_str(pathName, str(total_Sucess))
    Append_File_str(pathName, "\n")
    Append_File_str(pathName, "Failure: ")
    Append_File_str(pathName, str(total_Failure))
    Append_File_str(pathName, "\n")
    Append_File_str(pathName, str1)
    Append_File_str(pathName, "Success VM's\n")
    Append_File_str(pathName, "-----------\n")
    Append_File_list(pathName, success_VM)
    Append_File_str(pathName, "\n")
    Append_File_str(pathName, str1)
    Append_File_str(pathName, "Failed VM's\n")
    Append_File_str(pathName, "-----------\n")
    Append_File_list(pathName, failed_VM)
    Append_File_str(pathName, "\n")
    Append_File_str(pathName, str1)

def FailedVM_update(failed_VM, server, authTokenId, novaUrl):
    try:
        server_detail = get_server(authTokenId, novaUrl,
                                             server['id'])
        servStatus = get_server_status_dict(authTokenId,
                                                      novaUrl, server)
    except HttpError as e:
            print('HTTP Error: {0}'.format(e.body))
            exit(1)
    try:
        failed_VM.append("Name:")
        failed_VM.append(str(server['name']))
        failed_VM.append("\n")
    except:
        pass

    failed_VM.append(str(datetime.now().strftime("day:%Y-%m-%d time:%H-%M-%S")))
    failed_VM.append("\n")
    try:
        failed_VM.append("vmId:")
        failed_VM.append(str(server['id']))
        failed_VM.append("\n")
    except:
        pass
    try:
        failed_VM.append("task_state:")
        failed_VM.append(str(servStatus['task_state']))
        failed_VM.append("\n")
    except:
        pass
    try:
        failed_VM.append("vm_state:")
        failed_VM.append(str(servStatus['vm_state']))
        failed_VM.append("\n")
    except:
        pass
    try:
        failed_VM.append("power_state:")
        failed_VM.append(str(servStatus['power_state']))
        failed_VM.append("\n")
    except:
        pass
    try:
        failed_VM.append("health_value:")
        failed_VM.append(str(servStatus['health_value']))
        failed_VM.append("\n")
    except:
        pass
    try:
        failed_VM.append("host:")
        failed_VM.append(str(servStatus['host']))
    except:
        pass
    failed_VM.append("\n")
    try:
        failed_VM.append("fault:")
        failed_VM.append(str(server_detail['fault']))
    except:
        pass
    failed_VM.append("\n")
    failed_VM.append(200 * '=')
    failed_VM.append("\n")
    return failed_VM

def Report_Update_volumes(pathName, opName, total_Sucess, total_Failure, success_V, failed_V):
    str1 = '*' * 20 + '\n'
    total = total_Sucess + total_Failure
    Overwrite_File(pathName, "Test_Script: ")
    Append_File_str(pathName, opName)
    Append_File_str(pathName, "\n")
    Append_File_str(pathName, str1)
    Append_File_str(pathName, "Total: ")
    Append_File_str(pathName, str(total))
    Append_File_str(pathName, "\n")
    Append_File_str(pathName, "Success: ")
    Append_File_str(pathName, str(total_Sucess))
    Append_File_str(pathName, "\n")
    Append_File_str(pathName, "Failure: ")
    Append_File_str(pathName, str(total_Failure))
    Append_File_str(pathName, "\n")
    Append_File_str(pathName, str1)
    Append_File_str(pathName, "Success Volumes\n")
    Append_File_str(pathName, "-----------\n")
    Append_File_list(pathName, success_V)
    Append_File_str(pathName, "\n")
    Append_File_str(pathName, str1)
    Append_File_str(pathName, "Failed Volumes\n")
    Append_File_str(pathName, "-----------\n")
    Append_File_list(pathName, failed_V)
    Append_File_str(pathName, "\n")
    Append_File_str(pathName, str1)

def Report_Update_image(pathName, opName, total_Sucess, total_Failure, success_C, failed_C):
    str1 = '*' * 20 + '\n'
    total = total_Sucess + total_Failure
    Overwrite_File(pathName, "Test_Script: ")
    Append_File_str(pathName, opName)
    Append_File_str(pathName, "\n")
    Append_File_str(pathName, str1)
    Append_File_str(pathName, "Total: ")
    Append_File_str(pathName, str(total))
    Append_File_str(pathName, "\n")
    Append_File_str(pathName, "Success: ")
    Append_File_str(pathName, str(total_Sucess))
    Append_File_str(pathName, "\n")
    Append_File_str(pathName, "Failure: ")
    Append_File_str(pathName, str(total_Failure))
    Append_File_str(pathName, "\n")
    Append_File_str(pathName, str1)
    Append_File_str(pathName, "Success Images\n")
    Append_File_str(pathName, "-----------\n")
    Append_File_list(pathName, success_C)
    Append_File_str(pathName, "\n")
    Append_File_str(pathName, str1)
    Append_File_str(pathName, "Failed Images\n")
    Append_File_str(pathName, "-----------\n")
    Append_File_list(pathName, failed_C)
    Append_File_str(pathName, "\n")
    Append_File_str(pathName, str1)


######################################################################################################
#End of Report generation functions
######################################################################################################



