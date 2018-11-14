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

def createv2Token(address, authProps) :
	#print 'ENTER createv2Token'
#	address = address + ':5000'
#	url = '/v2.0/tokens'
	url = '/powervc/openstack/admin/v2.0/tokens'
	postBody = json.dumps({'auth' : authProps})
	return restUtils.postJSON(address, url, postBody)

def createv3Token(address, authProps) :
	#print 'ENTER createv2Token'
#	address = address + ':5000'
#	url = '/v2.0/tokens'
	url = '/powervc/openstack/admin/v3.0/tokens'
	postBody = json.dumps({'auth' : authProps})
	return restUtils.postJSON(address, url, postBody)

def showv2Tenants(address, token) :
	#print 'ENTER showv2Tenants'
#	address = address + ':5000'
#	url = '/v2.0/tenants'
	url = '/powervc/openstack/identity/v2.0/tenants'
	headers = {'X-Auth-Token' : token}
	return restUtils.getJSON(address, url, headers)

def showv3Tenants(address, token) :
	#print 'ENTER showv2Tenants'
#	address = address + ':5000'
#	url = '/v2.0/tenants'
	url = '/powervc/openstack/identity/v3.0/tenants'
	headers = {'X-Auth-Token' : token}
	return restUtils.getJSON(address, url, headers)

def authv2(keystoneAddress, user, passwd, tenantName):
	pwdCredProps = {'username' : user,
		'password' : passwd,
	}
	#authProps = {'passwordCredentials' : pwdCredProps}
	try :
		#token = createv2Token(keystoneAddress, authProps)
		#if not token : return None

		#tokenId = token['access']['token']['id']

		#tenants = getv2Tenants(keystoneAddress, tokenId)['tenants']
		#tenant = None
		#for t in tenants :
		#	if t['name'] == tenantName :
		#		tenant = t
		#if not tenant : return None

		authProps = {'passwordCredentials' : pwdCredProps,
		#	'tenantId' : tenant['id']
			'tenantName' : tenantName
			}
		return createv2Token(keystoneAddress, authProps)
	except restUtils.HttpError :
		return None

def authv3(keystoneAddress, domain, user, passwd, project):
	authProps = {
		'identity' : {
			'methods' : ['password'],
			'password' : {
				'user' : {
					'domain' : {'name' : domain},
					'name' : user,
					'password' : passwd
				}
			}
		},
		'scope' : {
			'project' : {
				'domain' : {'name' : domain},
				'name' : project
			}
		}
	}
	try :
		return createToken(keystoneAddress, authProps)
	except restUtils.HttpError :
		return None

def createToken(address, authProps) :
	#print 'ENTER createToken'
#	address = address + ':5000'
#	url = '/v3/auth/tokens'
	url = '/powervc/openstack/admin/v3/auth/tokens'
	postBody = json.dumps({'auth' : authProps})
	headers = {'Vary' : 'X-Auth-Token, X-Subject-Token'}
	respHeaders, resp = restUtils.postJSON2(address, url, postBody, headers)
	tok = ''
	if respHeaders :
		tok = respHeaders.getheader('X-Subject-Token')
	return tok, resp

def showToken(keystoneUrl, token, token_id) :
	#print 'ENTER showToken'
	address = openstackUtils.parseAddress(keystoneUrl)
	url = openstackUtils.parseBaseURL(keystoneUrl, address) + '/auth/tokens'
	headers = {
		'X-Auth-Token' : token,
		'X-Subject-Token' : token_id,
	}
	return restUtils.getJSON(address, url, headers)

def checkToken(keystoneUrl, token, token_id) :
	#print 'ENTER checkToken'
	address = openstackUtils.parseAddress(keystoneUrl)
	url = openstackUtils.parseBaseURL(keystoneUrl, address) + '/auth/tokens'
	headers = {
		'X-Auth-Token' : token,
		'X-Subject-Token' : token_id,
	}
	return restUtils.request('HEAD', address, url, headers)

def deleteToken(keystoneUrl, token, token_id) :
	#print 'ENTER deleteToken'
	address = openstackUtils.parseAddress(keystoneUrl)
	url = openstackUtils.parseBaseURL(keystoneUrl, address) + '/auth/tokens'
	headers = {
		'X-Auth-Token' : token,
		'X-Subject-Token' : token_id,
	}
	return restUtils.request('DELETE', address, url, headers)

def listDomains(keystoneUrl, token) :
	#print 'ENTER listDomains'
	address = openstackUtils.parseAddress(keystoneUrl)
	url = openstackUtils.parseBaseURL(keystoneUrl, address) + '/domains'
	headers = {'X-Auth-Token' : token}
	return restUtils.getJSON(address, url, headers)['domains']

def listUsers(keystoneUrl, token) :
	#print 'ENTER listUsers'
	address = openstackUtils.parseAddress(keystoneUrl)
	url = openstackUtils.parseBaseURL(keystoneUrl, address) + '/users'
	headers = {'X-Auth-Token' : token}
	return restUtils.getJSON(address, url, headers)['users']

def listUsers2(keystoneUrl, token) :
	#print 'ENTER listUsers'
	address = openstackUtils.parseAddress(keystoneUrl)
	url = openstackUtils.parseBaseURL(keystoneUrl, address) + '/users'
	headers = {'X-Auth-Token' : token}
	#return restUtils.getJSON(address, url, headers)['users']
	return restUtils.getJSON(address, url, headers)

def showUser(keystoneUrl, token, user_id) :
	#print 'ENTER showUser'
	address = openstackUtils.parseAddress(keystoneUrl)
	url = openstackUtils.parseBaseURL(keystoneUrl, address) + '/users/' + user_id
	headers = {'X-Auth-Token' : token}
	return restUtils.getJSON(address, url, headers)['user']

def listGroupsForUser(keystoneUrl, token, user_id) :
	#print 'ENTER listGroupsForUser'
	address = openstackUtils.parseAddress(keystoneUrl)
	url = openstackUtils.parseBaseURL(keystoneUrl, address) + '/users/' + user_id + '/groups'
	headers = {'X-Auth-Token' : token}
	return restUtils.getJSON(address, url, headers)['groups']

def listGroups(keystoneUrl, token) :
	#print 'ENTER listGroups'
	address = openstackUtils.parseAddress(keystoneUrl)
	url = openstackUtils.parseBaseURL(keystoneUrl, address) + '/groups'
	headers = {'X-Auth-Token' : token}
	return restUtils.getJSON(address, url, headers)['groups']

def listGroups2(keystoneUrl, token) :
	#print 'ENTER listGroups'
	address = openstackUtils.parseAddress(keystoneUrl)
	url = openstackUtils.parseBaseURL(keystoneUrl, address) + '/groups'
	headers = {'X-Auth-Token' : token}
	return restUtils.getJSON(address, url, headers)

def showGroup(keystoneUrl, token, group_id) :
	#print 'ENTER showGroup'
	address = openstackUtils.parseAddress(keystoneUrl)
	url = openstackUtils.parseBaseURL(keystoneUrl, address) + '/groups/' + group_id
	headers = {'X-Auth-Token' : token}
	return restUtils.getJSON(address, url, headers)['group']

def listUsersForGroup(keystoneUrl, token, group_id) :
	#print 'ENTER listUsersForGroup'
	address = openstackUtils.parseAddress(keystoneUrl)
	url = openstackUtils.parseBaseURL(keystoneUrl, address) + '/groups/' + group_id + '/users'
	headers = {'X-Auth-Token' : token}
	return restUtils.getJSON(address, url, headers)['users']

def listCredentials(keystoneUrl, token) :
	#print 'ENTER listCredentials'
	address = openstackUtils.parseAddress(keystoneUrl)
	url = openstackUtils.parseBaseURL(keystoneUrl, address) + '/credentials'
	headers = {'X-Auth-Token' : token}
	return restUtils.getJSON(address, url, headers)['credentials']

def listProjects(keystoneUrl, token) :
	#print 'ENTER listProjects'
	address = openstackUtils.parseAddress(keystoneUrl)
	url = openstackUtils.parseBaseURL(keystoneUrl, address) + '/projects'
	headers = {'X-Auth-Token' : token}
	return restUtils.getJSON(address, url, headers)['projects']

def listProjects2(keystoneUrl, token) :
	#print 'ENTER listProjects'
	address = openstackUtils.parseAddress(keystoneUrl)
	url = openstackUtils.parseBaseURL(keystoneUrl, address) + '/projects'
	headers = {'X-Auth-Token' : token}
	return restUtils.getJSON(address, url, headers)

def listRoles(keystoneUrl, token) :
	#print 'ENTER listRoles'
	address = openstackUtils.parseAddress(keystoneUrl)
	url = openstackUtils.parseBaseURL(keystoneUrl, address) + '/roles'
	headers = {'X-Auth-Token' : token}
	return restUtils.getJSON(address, url, headers)['roles']

def listServices(keystoneUrl, token) :
	#print 'ENTER listServices'
	address = openstackUtils.parseAddress(keystoneUrl)
	url = openstackUtils.parseBaseURL(keystoneUrl, address) + '/services'
	headers = {'X-Auth-Token' : token}
	return restUtils.getJSON(address, url, headers)['services']

def listEndpoints(keystoneUrl, token) :
	#print 'ENTER listEndpoints'
	address = openstackUtils.parseAddress(keystoneUrl)
	url = openstackUtils.parseBaseURL(keystoneUrl, address) + '/endpoints'
	headers = {'X-Auth-Token' : token}
	return restUtils.getJSON(address, url, headers)['endpoints']


