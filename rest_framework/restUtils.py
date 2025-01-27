#eCopyright IBM Corp. 2018.
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#http://www.apache.org/licenses/LICENSE-2.0
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

from rest_framework import log
import sys
import json
import ssl
import http.client

useHTTPS = True #change this if you want to use HTTP

class HttpError(Exception) :
    def __init__(self, code, reason, body=None) :
        self.code = code
        self.reason = reason
        self.body = body
    def __repr__(self) :
        return 'HttpError(code=%r,reason=%r,body=%r)' % (self.code, self.reason, self.body)

def request(method, address, url, headers=None, postBody=None) :
    if useHTTPS :
        protocol = 'https'
        # Create an unverified SSL context 
        ssl_context = ssl._create_unverified_context() 
        # Use the unverified SSL context with HTTPSConnection 
        conn = http.client.HTTPSConnection(address, context=ssl_context)
    else :
        protocol = 'http'
        conn = http.client.HTTPConnection(address)
    conn.timeout = 3000

    try :
        conn.request(method, url, postBody, headers)
        log.write('%s %s://%s%s headers=%s body=%s\n' % (method, protocol, address, url, headers, postBody))

        response = conn.getresponse()
        log.write('result: %s (%s)\n' % (response.status, response.reason))
        log.write('headers:\n%s\n' % (response.msg))

        if response.status == 204 :
            return None, None
        else :
            respBody = response.read()
            jsonObj = ''
            if respBody :
                try :
                    jsonObj = json.loads(respBody)
                    log.write(json.dumps(jsonObj, indent=3)+'\n')
                except ValueError :
                    log.write(respBody+'\n')
            if response.status >= 200 and response.status < 300 :
                #return jsonObj
                return response, jsonObj
            else :
                e = HttpError(response.status, response.reason)
                if jsonObj :
                    e.body = json.dumps(jsonObj, indent=3)
                print((e.body))
                raise e

    finally :
        conn.close()

def request2(method, address, url, headers=None, postBody=None) :
    if useHTTPS :
        protocol = 'https'
        # Create an unverified SSL context
        ssl_context = ssl._create_unverified_context()
        # Use the unverified SSL context with HTTPSConnection
        conn = http.client.HTTPSConnection(address, context=ssl_context)
    else :
        protocol = 'http'
        conn = http.client.HTTPConnection(address)
    conn.timeout = 3000

    try :
        conn.request(method, url, postBody, headers)
        log.write('%s %s://%s%s headers=%s body=%s\n' % (method, protocol, address, url, headers, postBody))

        response = conn.getresponse()
        log.write('result: %s (%s)\n' % (response.status, response.reason))
        log.write('headers:\n%s\n' % (response.msg))

        if response.status == 204 :
            return response.msg, None
        else :
            respBody = response.read()
            jsonObj = ''
            if respBody:
                try :
                    jsonObj = json.loads(respBody)
                    log.write(json.dumps(jsonObj, indent=3)+'\n')
                except ValueError :
                    log.write(respBody+'\n')
            if response.status >= 200 and response.status < 300:
                #return response.msg, jsonObj
                return response, jsonObj
            else :
                e = HttpError(response.status, response.reason)
                if jsonObj :
                    e.body = json.dumps(jsonObj, indent=3)
                print(e.body)
                raise e

    finally :
        conn.close()

def getJSON(address, url, headers=None) :
    if headers == None : headers = {}
    headers['Accept'] = 'application/json'
    return request('GET', address, url, headers)

def deleteJSON(address, url, headers=None) :
    if headers == None : headers = {}
    headers['Accept'] = 'application/json'
    return request('DELETE', address, url, headers)

def postJSON(address, url, body, headers=None) :
    if headers == None : headers = {}
    headers['Accept'] = 'application/json'
    if body :
        headers['Content-Type'] = 'application/json'
    return request('POST', address, url, headers, body)

def postJSON2(address, url, body, headers=None) :
    if headers == None : headers = {}
    headers['Accept'] = 'application/json'
    if body :
        headers['Content-Type'] = 'application/json'
    return request2('POST', address, url, headers, body)

def putJSON(address, url, body, headers=None) :
    if headers == None : headers = {}
    headers['Accept'] = 'application/json'
    if body :
        headers['Content-Type'] = 'application/json'
    return request('PUT', address, url, headers, body)
