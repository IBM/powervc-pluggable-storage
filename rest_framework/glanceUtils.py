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

def listImages(glanceUrl, token) :
    #print 'ENTER listImages'
    address = openstackUtils.parseAddress(glanceUrl)
    url = openstackUtils.parseBaseURL(glanceUrl, address) + '/v2.0/images?limit=400'
    headers = {'X-Auth-Token' : token}
    return restUtils.getJSON(address, url, headers)

def showImage(glanceUrl, token, image_id) :
    #print 'ENTER showImage'
    address = openstackUtils.parseAddress(glanceUrl)
    url = openstackUtils.parseBaseURL(glanceUrl, address) + '/v2.0/images/' + image_id
    headers = {'X-Auth-Token' : token}
#    return restUtils.getJSON(address, url, headers)
    return restUtils.getJSON(address, url, headers)

def deleteImage(glanceUrl, token, image_id) :
    #print 'ENTER deleteImage'
    address = openstackUtils.parseAddress(glanceUrl)
    url = openstackUtils.parseBaseURL(glanceUrl, address) + '/v2.0/images/' + image_id
    headers = {'X-Auth-Token' : token}
    return restUtils.request('DELETE', address, url, headers)

def exportImage(cinderUrl, token, image_id, image_name) :
    address = openstackUtils.parseAddress(cinderUrl)
    url = openstackUtils.parseBaseURL(cinderUrl, address) + '/image-backups/export_image'
    headers = {'X-Auth-Token' : token}
    print ({'image-backup':{'src_image_id': image_id,'name': 'export_svt_' + image_name,'description': 'SVT image export'}})
    postBody = json.dumps({'image-backup':{'src_image_id': image_id,'name': 'export_svt_' + image_name,'description': 'SVT image export'}})
    restUtils.postJSON(address, url, postBody, headers)
