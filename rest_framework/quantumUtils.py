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

from rest_framework import restUtils
from rest_framework import openstackUtils
import json

def listNetworks(quantumUrl, token) :
        #print 'ENTER listNetworks'
        address = openstackUtils.parseAddress(quantumUrl)
        url = openstackUtils.parseBaseURL(quantumUrl, address) + '/v2.0/networks'
        headers = {'X-Auth-Token' : token}
        return restUtils.getJSON(address, url, headers)

def showNetwork(quantumUrl, token, network_id) :
        #print 'ENTER showNetwork'
        address = openstackUtils.parseAddress(quantumUrl)
        url = openstackUtils.parseBaseURL(quantumUrl, address) + '/v2.0/networks/' + network_id
        headers = {'X-Auth-Token' : token}
        return restUtils.getJSON(address, url, headers)

def createNetwork(quantumUrl, token, networkProps) :
        #print 'ENTER createNetwork'
        address = openstackUtils.parseAddress(quantumUrl)
        url = openstackUtils.parseBaseURL(quantumUrl, address) + '/v2.0/networks'
        postBody = json.dumps({'network' : networkProps})
        headers = {'X-Auth-Token' : token}
        return restUtils.postJSON(address, url, postBody, headers)

def updateNetwork(quantumUrl, token, network_id, networkProps) :
        #print 'ENTER updateNetwork'
        address = openstackUtils.parseAddress(quantumUrl)
        url = openstackUtils.parseBaseURL(quantumUrl, address) + '/v2.0/networks/' + network_id
        putBody = json.dumps({'network' : networkProps})
        headers = {'X-Auth-Token' : token}
        return restUtils.putJSON(address, url, putBody, headers)

def deleteNetwork(quantumUrl, token, network_id) :
        #print 'ENTER deleteNetwork'
        address = openstackUtils.parseAddress(quantumUrl)
        url = openstackUtils.parseBaseURL(quantumUrl, address) + '/v2.0/networks/' + network_id
        headers = {'X-Auth-Token' : token}
        return restUtils.request('DELETE', address, url, headers)

def listSubnets(quantumUrl, token) :
        #print 'ENTER listSubnets'
        address = openstackUtils.parseAddress(quantumUrl)
        url = openstackUtils.parseBaseURL(quantumUrl, address) + '/v2.0/subnets'
        headers = {'X-Auth-Token' : token}
        return restUtils.getJSON(address, url, headers)

def transferIP(quantumUrl, token, portProps) :
    #print 'ENTER transferIP'
    address = openstackUtils.parseAddress(quantumUrl)
    url = openstackUtils.parseBaseURL(quantumUrl, address) + '/v2.0/ip-transfer'
    postBody = json.dumps(portProps)
    headers = {'X-Auth-Token' : token}
    return restUtils.postJSON(address, url, postBody, headers)

def showSubnet(quantumUrl, token, subnet_id) :
        #print 'ENTER showSubnet'
        address = openstackUtils.parseAddress(quantumUrl)
        url = openstackUtils.parseBaseURL(quantumUrl, address) + '/v2.0/subnets/' + subnet_id
        headers = {'X-Auth-Token' : token}
        return restUtils.getJSON(address, url, headers)

def createSubnet(quantumUrl, token, subnetProps) :
        #print 'ENTER createSubnet'
        address = openstackUtils.parseAddress(quantumUrl)
        url = openstackUtils.parseBaseURL(quantumUrl, address) + '/v2.0/subnets'
        postBody = json.dumps({'subnet' : subnetProps})
        headers = {'X-Auth-Token' : token}
        return restUtils.postJSON(address, url, postBody, headers)

def updateSubnet(quantumUrl, token, subnet_id, subnetProps) :
        #print 'ENTER updateSubnet'
        address = openstackUtils.parseAddress(quantumUrl)
        url = openstackUtils.parseBaseURL(quantumUrl, address) + '/v2.0/subnets/' + subnet_id
        putBody = json.dumps({'subnet' : subnetProps})
        headers = {'X-Auth-Token' : token}
        return restUtils.putJSON(address, url, putBody, headers)

def deleteSubnet(quantumUrl, token, subnet_id) :
        #print 'ENTER deleteSubnet'
        address = openstackUtils.parseAddress(quantumUrl)
        url = openstackUtils.parseBaseURL(quantumUrl, address) + '/v2.0/subnets/' + subnet_id
        headers = {'X-Auth-Token' : token}
        return restUtils.request('DELETE', address, url, headers)

## SRIOV port
def createSriovPorts(quantumUrl, token, sriovPortProps) :
        #print 'ENTER createSubnet'
        address = openstackUtils.parseAddress(quantumUrl)
        url = openstackUtils.parseBaseURL(quantumUrl, address) + '/v2.0//ports'
        postBody = json.dumps({'port' : sriovPortProps})
        headers = {'X-Auth-Token' : token}
        print(url)
        print(postBody)
        return restUtils.postJSON(address, url, postBody, headers)

## Network Node host registration
def registerNetNodes(quantumUrl, token, netnodeProps):
    address = openstackUtils.parseAddress(quantumUrl)
    url = openstackUtils.parseBaseURL(quantumUrl, address) + '/v2.0/network-nodes'
    putBody = json.dumps({'network_node': {'registration': netnodeProps}})
    headers = {'X-Auth-Token': token}
    return restUtils.postJSON(address, url, putBody, headers)

## Network Node host De-Registration
def deregisterNetNodes(quantumUrl, token, netnode_hname):
    address = openstackUtils.parseAddress(quantumUrl)
    url = openstackUtils.parseBaseURL(quantumUrl, address) + '/v2.0/network-nodes/' + netnode_hname + '/uninstall'
    headers = {'X-Auth-Token': token}
    return restUtils.deleteJSON(address, url, headers)
