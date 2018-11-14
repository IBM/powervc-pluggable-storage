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

from ConfigParser import NoOptionError
import traceback

from rest_framework import novaUtils
from rest_framework import quantumUtils
from rest_framework import cinderUtils
from rest_framework import svt_tester_base
from rest_framework import svt_tester_base
from rest_framework import restUtils, openstackUtils
import json
import pexpect
import subprocess
import paramiko
import re
import time
import os
import sys

hmc_h = 'hmc_h'
hmc_disp_name = 'hmc_disp_name'
Network_name = 'network_name'
vlan_id = 'vlan_id'

def test_reg(self):
        token = self.authent_id
        neutronUrl = self.getServiceUrl('network')

        HMC_Id = test_register_hmc(self)
        print "Hello"
        print "HMC Registration"

        Net_Cr = test_create_network(self)
        print Net_Cr

        print HMC_Id
        Host_Reg = test_host_reg(self)
        print "Host Regsitration"
        print Host_Reg
        Net_Cr = test_create_network(self)
        print Net_Cr
        SVC_reg = test_svc_reg(self)
        print "SVC Regsitration"


def register_hmc(novaUrl, token, hmc_ip_list, hmc_userid_list, hmc_password_list, hmc_disp_name):

        hmcProps = {'access_ip': hmc_ip_list,
                    'user_id': hmc_userid_list,
                    'password': hmc_password_list,
                    'hmc_display_name': hmc_disp_name
                    }
        print "Registering HMC:", str(hmcProps)
        print token

        address = openstackUtils.parseAddress(novaUrl)
        url = openstackUtils.parseBaseURL(novaUrl, address) + '/ibm-hmcs'
        putBody = json.dumps({'hmc': {'registration': hmcProps}})
        print putBody
        headers = {'X-Auth-Token': token}
        registrnRespns, registrnRespnsBodyJSON = restUtils.postJSON(address, url, putBody, headers)

        print "Registration of HMC response:"


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
            print hostProps
            registrnRespns, registrnRespnsBodyJSON = createHost(novaUrl, token, hostProps)
            print "Registration of Host response:"
            print str(registrnRespnsBodyJSON)

        return registrnRespns

def register_kvmhost(novaUrl, token, host_ip, host_display_name, userid, password):

        address = openstackUtils.parseAddress(novaUrl)
        host_display_name = host_display_name
        hostProps = {'host_type': "kvm",
                     'host_display_name': host_display_name,
                     'access_ip' : host_ip,
                     'user_id': userid,
                     'password': password,
                     'ephemeral_disk_path': "/var/lib/libvirt/images",
                     'force_unmanage':  "false"
                      }

        registrnRespns, registrnRespnsBodyJSON = createHost(novaUrl, token, hostProps)
        print "Registration of Host response:"
        print str(registrnRespnsBodyJSON)

        return registrnRespns


def create_network(neutronUrl, token, network_name, vlan_id, cidr_ip, ip_version, gateway_ip):

        vlan_id = vlan_id
        networkProps = {"name":network_name,
                        "provider:network_type":"vlan",
                        "provider:physical_network":"default",

                        "provider:segmentation_id": vlan_id
                        }
        registrnRespns, registrnRespnsBodyJSON = quantumUtils.createNetwork(neutronUrl, token, networkProps)

        dict = registrnRespnsBodyJSON
        net = dict['network']
        net_id = net['id']

        cidr = cidr_ip
        ipversion = ip_version
        gateway_ip = gateway_ip

        subnetProps = {"network_id": net_id,
                       "cidr": cidr,
                       "ip_version": ipversion,
                       "gateway_ip": gateway_ip,
                       "enable_dhcp": "false"
                        }


        registrnRespns, registrnRespnsBodyJSON = quantumUtils.createSubnet(neutronUrl, token, subnetProps)
        print str(registrnRespnsBodyJSON)
        return registrnRespns

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

        return str(registrnRespnsBodyJSON)


def fab_reg(cinderUrl, token, fab_access_ip, fabric_disp_name, fabric_type, fab_userid, fab_passwd):
        if fabric_type is "brocade":
            fabProps = { "access_ip": fab_access_ip,
                        "auto_add_host_key": "true",
                        "fabric_display_name": fabric_disp_name,
                        "fabric_type": fabric_type,
                        "password": fab_passwd,
                        "user_id": fab_userid,
                        "zoning_policy": "initiator"
                        }
        else:
            fabProps = { "access_ip": fab_access_ip,
                        "auto_add_host_key": "true",
                        "fabric_display_name": fabric_disp_name,
                        "fabric_type": fabric_type,
                        "password": fab_passwd,
                        "user_id": fab_userid,
                        "zoning_policy": "initiator",
                        "vsan": 1,
                        "port": 22
                      }
        address = openstackUtils.parseAddress(cinderUrl)
        url = openstackUtils.parseBaseURL(cinderUrl, address) + '/san-fabrics'
        postbody = json.dumps({'fabric' : { 'registration' : fabProps}})
        headers = {'X-Auth-Token': token}
        registrnRespns, registrnRespnsBodyJSON = restUtils.postJSON(address, url, postbody, headers)

def liststorage(cinderUrl, token):
    address = openstackUtils.parseAddress(cinderUrl)
    url = openstackUtils.parseBaseURL(cinderUrl, address) + '/storage-providers'
    headers = {'X-Auth-Token': token}
    return restUtils.getJSON(address, url, headers)

def onboard_vol(cinderUrl, token, volume_id, host_name):
    address = openstackUtils.parseAddress(cinderUrl)
    url = openstackUtils.parseBaseURL(cinderUrl, address) + '/os-hosts/' + host_name + '/onboard'
    print url
    headers = {'X-Auth-Token': token}
    volProps = {"volumes": [volume_id]}
    postbody = json.dumps(volProps)
    print postbody
    registrnRespns, registrnRespnsBodyJSON = restUtils.postJSON(address, url, postbody, headers)

def unmanage_vol(cinderUrl, token, volume_id, host_name):
    address = openstackUtils.parseAddress(cinderUrl)
    url = openstackUtils.parseBaseURL(cinderUrl, address) + '/os-hosts/' + host_name + '/unmanage'
    print url
    headers = {'X-Auth-Token': token}
    volProps = {"volumes": [volume_id]}
    postbody = json.dumps(volProps)
    print postbody
    registrnRespns, registrnRespnsBodyJSON = restUtils.postJSON(address, url, postbody, headers)



def getHMC_uuid(hmc_name, novaUrl, address, token):

        show_hmc_url = openstackUtils.parseBaseURL(novaUrl, address) + '/ibm-hmcs'
        headers = {'X-Auth-Token': token}
        resp_body2 = restUtils.getJSON(address, show_hmc_url, headers)
        dict = resp_body2[1]

        for i in dict['hmcs']:

            print i['hmc_display_name']
            print hmc_name
            if i['hmc_display_name'] == hmc_name:
                return i['hmc_uuid']
        return 0

def createHost(novaUrl, token, hostProps):

    reg_key = 'registration'
    print reg_key

    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + '/os-hosts'
    postBody = json.dumps({'host': { 'registration': hostProps}})
    headers = {'X-Auth-Token': token }
    print "post body", postBody
    print url
    print headers
    return restUtils.postJSON(address, url, postBody, headers)

def cre_flavor(token, novaUrl, fla_name, mem, vcpu, proc_unit, min_vcpu, max_vcpu, min_mem, max_mem, min_proc, max_proc, SPP):
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + '/flavors'
    flavor_props =  {"name": fla_name,
                               "ram": mem,
                               "vcpus":  vcpu,
                               "disk": 0,
                               "swap":0,
                               "OS-FLV-EXT-DATA:ephemeral":0,
                               "rxtx_factor":1,
                               "extra_specs":{"powervm:srr_capability":"false",
                                              "powervm:min_vcpu": min_vcpu,
                                              "powervm:max_vcpu": max_vcpu,
                                              "powervm:min_mem": min_mem,
                                              "powervm:max_mem": max_mem,
                                              "powervm:availability_priority":"127",
                                              "powervm:proc_units":proc_unit,
                                              "powervm:min_proc_units": min_proc,
                                              "powervm:max_proc_units": max_proc,
                                              "powervm:dedicated_proc":"false",
                                              "powervm:shared_proc_pool_name": SPP,
                                              "powervm:uncapped":"true",
                                              "powervm:shared_weight":"128"}
                               }


    postBody = json.dumps({'flavor': flavor_props })
    print postBody
    headers =  {'X-Auth-Token': token }
    return restUtils.postJSON(address, url, postBody, headers)

def create_scg(token, novaUrl, scg_name, vios1_id, vios2_id):
    address = openstackUtils.parseAddress(novaUrl)
    url = openstackUtils.parseBaseURL(novaUrl, address) + '/storage-connectivity-groups'
    scg_props = { "display_name": scg_name,
                   "fc_storage_access":'true',
                   "auto_add_vios":'false',
                   "include_untagged": 'false',
                   "enabled": 'true',
                   "vios_ids": [vios1_id, vios2_id],
                   "exact_redundancy": 'false',
                   "vios_redundancy":"1",
                   "fabric_set_req":"per_vios",
                   "fabric_set_npiv":["*"],
                   "ports_per_fabric_npiv":"1",
                   "boot_connectivity":["npiv"],
                   "data_connectivity":["npiv"],
                   }


    postBody = json.dumps({'storage_connectivity_group': scg_props })
    print postBody
    headers =  {'X-Auth-Token': token }
    return restUtils.postJSON(address, url, postBody, headers)


def virt_fab_reg(cinderUrl, token, fab_access_ip, fabric_disp_name, fabric_type, zoning_policy, fab_userid, fab_passwd, virtual_fabric_id):
        fabProps = { "access_ip": fab_access_ip,
                      "auto_add_host_key": "true",
                      "fabric_display_name": fabric_disp_name,
                      "fabric_type": fabric_type,
                      "zoning_policy": zoning_policy,
                      "auto_add_certificate":"false",
                      "password": fab_passwd,
                      "user_id": fab_userid,
                      "port": "22",
                      "virtual_fabric_id": virtual_fabric_id,
                      "vsan": virtual_fabric_id
                      }
        address = openstackUtils.parseAddress(cinderUrl)
        url = openstackUtils.parseBaseURL(cinderUrl, address) + '/san-fabrics'
        postbody = json.dumps({'fabric' : { 'registration' : fabProps}})
        headers = {'X-Auth-Token': token}
        registrnRespns, registrnRespnsBodyJSON = restUtils.postJSON(address, url, postbody, headers)

# Email configuration
def registerEmail(notificationurl, token, smtp_server, smtp_port, from_name, from_address, add_receipt_emails, authorize_user_id, authorize_passwd, use_tls, retry_on_failure, retry_frequency, retry_number):
    address = openstackUtils.parseAddress(notificationurl)
    url = openstackUtils.parseBaseURL(notificationurl, address) + "/v1/email/server"
    ssk_email_props = {"from_name": from_name, "from_address": from_address, "additional_addresses": [add_receipt_emails], "smtp_port": smtp_port, "enabled": "true", "smtp_server": smtp_server, "retry_on_failure": retry_on_failure, "retry_frequency": retry_frequency, "retry_number": retry_number, "user_id": authorize_user_id, "password": authorize_passwd, "use_tls": use_tls}
    putBody = json.dumps({"email_server" : ssk_email_props})
    headers = {'X-Auth-Token': token}
    return restUtils.putJSON(address, url, putBody, headers)

if __name__ == '__main__':
    svt_tester_base.main()
