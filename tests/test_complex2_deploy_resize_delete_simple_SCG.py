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
from rest_framework.statemachine import StateMachine
from rest_framework.restUtils import HttpError
from rest_framework import novaUtils
from rest_framework import Utils
import os
import time
import copy
from datetime import datetime
from datetime import timedelta

START = "START"
DEPLOYING = "DEPLOYING"
DEPLOY_COMPLETE = 'DEPLOY_COMPLETE'
DEPLOY_ADD = 'DEPLOY_ADD'
RESIZING = 'RESIZING'
START_DELETE = 'START_DELETE'
TIMED_OUT = 'TIMED_OUT'
RESIZE_COMPLETE = 'RESIZE_COMPLETE'
DELETING = 'DELETING'
DELETE_COMPLETE = 'DELETE_COMPLETE'
DELETE_START = 'DELETE_START'
ERROR = 'ERROR'
END = "END"
NUM_DEPLOYS = 'number_of_deploys'
DEPLOYS_BEFORE_SCENARIO_START = 'deploys_before_scenario_start'
SCG_FLAVOR_NAMES = 'scg_flavor_names'
START_IP = 'start_ip_address'
IMAGE_NAME_LIST = 'image_name_list'
SRV_NAME_PREFIX = 'server_name_prefix'
NET_NAME = 'network_name'
DEPLOY_FLAV = 'deploy_flavor'
RESIZE_FLAV = 'resize_flavor'
SLEEP_INT = 'sleep_interval'
WAIT_TO = 'wait_timeout'
NUM_CONCUR_DEPLOYS = 'number_of_concurrent_deploys'
OPT_TIMED_STATS = 'timed_stats'
DEPLOY_SUM = 'deploy_sum'
DELETE_SUM = 'delete_sum'
RESIZE_SUM = 'resize_sum'
DEPLOY_COUNT = 'deploy_count'
DELETE_COUNT = 'delete_count'
RESIZE_COUNT = 'resize_count'
SERVER_DICT = 'server'
VMS_LIST = 'vms'
STATS_DICT = 'stats'
STATE_START_TIME = 'state_start'
IP_ADDR = 'ip_addr'
DEPLOY_FLAVID = 'deploy_flavorId'
IMAGE_ID = 'imageRef'
NET_ID = 'networkId'
RESIZE_FLAVID = 'resize_flavorId'
POST_DEPLOY_STATE = 'post_deploy_state'
SM_STATE = 'state'
SM_CARGO = 'cargo'
NAME_KEY = 'name'
ID_KEY = 'id'
TASK_STATE_KEY = 'task_state'
VM_STATE_KEY = 'vm_state'
POWER_STATE_KEY = 'power_state'
HEALTH_VAL_KEY = 'health_value'
TIME_OUT_STATE_KEY = 'timeout_state'
#Sample Config Parameters
"""
[test_1013_complex2_deploy]
number_of_deploys = 100
deploys_before_scenario_start = 100
start_ip_address =172.26.17.1
image_name_list = ['rhel72_1','rhel73LE_1','rhel73LE_2']
server_name_prefix = rojv_
network_name = private
deploy_flavor = roj1
resize_flavor = roj2
sleep_interval = 8
wait_timeout = 300
number_of_concurrent_deploys = 10
timed_stats = True
scg_flavor_names = ['vSCSI']
"""

class SvtDeployTester(svt_tester_base.SvtTesterBase):
    """Testcase to do sequential deploys and sequential resize on stop.
    Requires a number of config options to be set in the configuration file
    which is passed as an argument:
    number_of_deploys = <number of deploys to perform>
    server_name_prefix = <prefix of the server name>
    start_ip_address = <starting ip address>
    image_name = <name of image to use for deploy>
    network_name = <name of the network to use>
    wait_timeout
    flavor_for_deploy = <flavor used for deploys>
    concurrent_count = <number of concurrent deploys>
    Optional configuration:
    timed_stats = <True or False depending if you want to see average timings>
    """

    required_options = [NUM_DEPLOYS, START_IP, IMAGE_NAME_LIST,
                        SRV_NAME_PREFIX, NET_NAME, DEPLOY_FLAV, RESIZE_FLAV,
                        SLEEP_INT, WAIT_TO, NUM_CONCUR_DEPLOYS,
                        DEPLOYS_BEFORE_SCENARIO_START, SCG_FLAVOR_NAMES
                        ]

    def cmp(a, b):
        return (a > b) - (a < b) 

    def test_1013_complex2_deploy(self):
        options_missing = False
        for option in self.required_options:
            if not self.config_has_option(option):
                print(('option=', option, 'not found in configuration file'))
                options_missing = True
        if options_missing:
            print('Provide missing options to the configuration file.')
            os._exit(1)

        number_of_deploys = int(self.config_get(NUM_DEPLOYS))
        server_name_prefix = self.config_get(SRV_NAME_PREFIX)
        start_ip_address = self.config_get(START_IP)
        image_name_list = self.config_get(IMAGE_NAME_LIST)
        network_name = self.config_get(NET_NAME)
        deploy_flavor = self.config_get(DEPLOY_FLAV)
        resize_flavor = self.config_get(RESIZE_FLAV)

        number_of_concurrent_deploys = \
            self.config_get(NUM_CONCUR_DEPLOYS)
        post_states = [END, DELETING, RESIZING, DELETING]
        deploys_before_scenario_starts = \
            self.config_get(DEPLOYS_BEFORE_SCENARIO_START)
        wait_timeout = self.config_get(WAIT_TO)
        sleep_interval = self.config_get(SLEEP_INT)
        if self.config_has_option(OPT_TIMED_STATS):
            timed_stats = self.config_get(OPT_TIMED_STATS)
        else:
            timed_stats = False

        deploy_flavorId = None
        resize_flavorId = None
        try:
            flavor_list = Utils.get_flavor_list(self.authent_id, self.novaUrl)
        except HttpError as e:
            print(('HTTP Error: {0}'.format(e.body)))
            os._exit(1)
        for flavor in flavor_list:
            if flavor[NAME_KEY] == deploy_flavor:
                deploy_flavorId = flavor[ID_KEY]
            if flavor[NAME_KEY] == resize_flavor:
                resize_flavorId = flavor[ID_KEY]
            if deploy_flavorId and resize_flavorId:
                break
        if not deploy_flavorId:
            print(("Deploy Flavor, {0} not found".format(deploy_flavor)))
            exit(1)
        if not resize_flavorId:
            print(("Resize Flavor, {0} not found".format(resize_flavor)))
            os._exit(1)

        image_ref_list = []

        for image_name in image_name_list:
            imageRef = Utils.get_named_image(self.authent_id, self.glanceUrl,
                                             image_name)
            image_ref_list.append(imageRef)

        if not image_ref_list:
            print(('Named images {0} not found,'\
                'provide a valid image names.'.format(image_name_list)))
            os._exit(1)

        networkId = Utils.get_named_network_id(self.authent_id,
                                               self.quantumUrl,
                                               network_name)
        if not networkId:
            print(('Named Network {0} not found,'\
                ' provide a valid image name.'.format(network_name)))
            os._exit(1)
        netmask = Utils.get_netmask(self.authent_id, self.quantumUrl,
                                    networkId, start_ip_address)

        # define state machine
        sm = StateMachine()
        sm.add_state(START, self.start)
        sm.add_state(DEPLOYING, self.deploying)
        sm.add_state(DEPLOY_COMPLETE, self.deploy_complete)
        sm.add_state(DEPLOY_ADD, self.deploy_add)
        sm.add_state(RESIZING, self.resizing)
        sm.add_state(START_DELETE, self.start_delete)
        sm.add_state(DELETING, self.deleting)
        sm.add_state(DELETE_COMPLETE, self.delete_complete)
        sm.add_state(RESIZE_COMPLETE, self.resize_complete)
        sm.add_state(TIMED_OUT, self.timed_out)
        sm.add_state(END, self.end_transition, end_state=1)
        sm.add_state(ERROR, self.error_transition, end_state=1)
        sm.set_start(START)
        if timed_stats:
            stats = {DEPLOY_SUM: timedelta(0),
                     DEPLOY_COUNT: 0,
                     DELETE_SUM: timedelta(0),
                     DELETE_COUNT: 0,
                     RESIZE_SUM: timedelta(0),
                     RESIZE_COUNT: 0
                     }
        else:
            stats = None
        req_deploy_count = 0
        num_deployed = 0
        num_deleted = 0
        num_resized = 0
        work_item_list = []
        servers_timed_out = []
        servers_errored = []
        server_list = Utils.get_server_details(self.authent_id, self.novaUrl,
                                               fields=['name',
                                                       'id',
                                                       'created',
                                                       'addresses'])
        if number_of_deploys <= len(server_list):
            print(('Requested {0} Virtual Servers, but {1} already exist'.\
                format(number_of_deploys, len(server_list))))
            os._exit(1)
        ip_pool = []
        for i in range(number_of_deploys + number_of_concurrent_deploys):
            ip = Utils.next_ip(start_ip_address, netmask, i)
            if not ip:
                break
            ip_pool.append(ip)
        for server in server_list:
            for network in server['addresses']:
                for addr_dict in server['addresses'][network]:
                    if addr_dict['addr'] in ip_pool:
                        ip_pool.remove(addr_dict['addr'])

        print(('ip_pool[{0}]={1}'.format(len(ip_pool), ip_pool)))
        print("preeti server_list=",server_list)
        #server_list.sort()
        #server_list.sort(cmp, self.key_created, False)
        projected_deploy_count = len(server_list)
        # SCG section.
        # We first get the list of SCG flavor names.
        try:
            scg_flavor_list = self.config_get(SCG_FLAVOR_NAMES)
        except HttpError as e:
            print(('HTTP Error: {0}'.format(e.body)))
            os._exit(1)
            # Query for all the SCGs
        try:

            scg_response, scg_dict = novaUtils.getSCGs(self.novaUrl, self.authent_id)
        except HttpError as e:
            print(('HTTP Error: {0}'.format(e.body)))
            os._exit(1)

        # Scan the usable SCGs
        scgs_to_use = []
        for scg in scg_dict['storage_connectivity_groups']:
            for scg_flavor in scg_flavor_list:
                if scg['display_name'] == scg_flavor:
                    scgs_to_use.append(scg['id'])
        scgs_copy = copy.copy(scgs_to_use)
        while work_item_list[:] or projected_deploy_count < number_of_deploys:
            # Count the number of severs that are currently deploying
            concurrent_deploy_count = 0
            for work_item in work_item_list:
                if work_item[SM_STATE] == DEPLOYING or\
                    work_item[SM_STATE] == START:
                    concurrent_deploy_count += 1
            # request as many deploys as possible to meet the concurrent value
            while concurrent_deploy_count < number_of_concurrent_deploys and \
                projected_deploy_count < number_of_deploys:
                if len(server_list) > 5:
                    display_count = 5
                else:
                    display_count = len(server_list)
                if display_count > 0:
                    print(('deployed servers={0}'.\
                        format(server_list[0:display_count])))
                print(('ip_pool={0}'.format(ip_pool[0:5])))
                imageId = \
                    image_ref_list[req_deploy_count % len(image_ref_list)]
                ip = ip_pool.pop(0)
                if len(scgs_copy) != 0:
                    scg_id = scgs_copy[0]
                    if scg_id in scgs_copy:
                        scgs_copy.remove(scg_id)
                else:
                    scgs_copy = copy.copy(scgs_to_use)
                    scg_id = scgs_copy[0]
                    if scg_id in scgs_copy:
                        scgs_copy.remove(scg_id)
                try:
                    scg_prop = {"powervm:storage_connectivity_group":scg_id}
                    novaUtils.addSCGtoFlavor(self.novaUrl, self.authent_id,
                                             deploy_flavorId, scg_prop)
                except Exception as e:
                    print("Encoutered an exception in adding scg")
                server = self.deploy_server(imageId, server_name_prefix,
                                            ip, networkId,
                                            deploy_flavorId)
                cargo = {}
                index = 0
                index = req_deploy_count % len(post_states)
                if req_deploy_count < deploys_before_scenario_starts:
                    cargo[POST_DEPLOY_STATE] = END
                    projected_deploy_count += 1
                elif index == 0:
                    cargo[POST_DEPLOY_STATE] = END
                    projected_deploy_count += 1
                elif index == 1 or index == 3:
                    cargo[POST_DEPLOY_STATE] = DELETING
                elif index == 2:
                    cargo[POST_DEPLOY_STATE] = RESIZING
                    cargo[RESIZE_FLAVID] = resize_flavorId
                    projected_deploy_count += 1
                cargo[SERVER_DICT] = server
                cargo[STATE_START_TIME] = datetime.now()
                cargo[STATS_DICT] = stats
                cargo[WAIT_TO] = wait_timeout
                work_item_list.append({SM_STATE: START,
                                       SM_CARGO: cargo})
                concurrent_deploy_count += 1
                req_deploy_count += 1

            for work_item in work_item_list[:]:
                currentState = work_item[SM_STATE]
                currentCargo = work_item[SM_CARGO]
                if sm.is_end_state(currentState):
                    work_item_list.remove(work_item)
                    print(('work_item finished:', str(work_item)))
                    continue
                # get updated state and cargo
                (newState, newCargo) = sm.step(currentState, currentCargo)
                if newState != currentState:
                    print(('{0} -> {1} for Server {2}'.\
                        format(currentState, newState,
                               newCargo[SERVER_DICT][NAME_KEY])))

                    if newState == DELETE_COMPLETE:
                        # recycle IP
                        server = newCargo['server']
                        for network in newCargo['server']['addresses']:
                            for addr_dict in \
                                newCargo['server']['addresses'][network]:
                                if not addr_dict in ip_pool:
                                    ip_pool.insert(0, addr_dict['addr'])
                                    print(('+++ip_pool after insert{0}'.\
                                        format(ip_pool[0:3])))
                                    print(('**ip addr of deleted vm={0}'.\
                                        format(ip_pool[0])))
                        num_deleted += 1
                    elif newState == TIMED_OUT:
                        servers_timed_out.append(newCargo[SERVER_DICT]
                                                 [NAME_KEY])
                    elif newState == DEPLOY_ADD:
                        server_id = None
                        server_id = newCargo[SERVER_DICT]['id']
                        server = {}
                        fields = ['name', 'id', 'created', 'addresses']
                        try:
                            server = Utils.get_server(self.authent_id,
                                                      self.novaUrl,
                                                      server_id, fields=fields)
                        except HttpError as e:
                            print(('HTTP Error: {0}'.format(e.body)))
                            os._exit(1)
                        if not server in server_list:
                            server_list.append(server)
                            print(('Adding Server {0} to list of servers'.\
                                format(server)))
                        num_deployed += 1
                    elif newState == RESIZE_COMPLETE:
                        num_resized += 1
                    elif newState == START_DELETE:
                        deleteCargo = {}
                        deleteCargo[SERVER_DICT] = server_list.pop(0)
                        print(('Request Delete Server {0}'.\
                            format(deleteCargo[SERVER_DICT]['name'])))
                        try:
                            Utils.delete_server(self.authent_id, self.novaUrl,
                                                deleteCargo[SERVER_DICT])
                        except HttpError as e:
                            print(('HTTP Error: {0}'.format(e.body)))
                            os._exit(1)

                        deleteCargo[STATE_START_TIME] = datetime.now()
                        deleteCargo[STATS_DICT] = stats
                        deleteCargo[WAIT_TO] = wait_timeout
                        work_item_list.append({SM_STATE: DELETING,
                                               SM_CARGO: deleteCargo})

                # update work_item
                work_item[SM_STATE] = newState
                work_item[SM_CARGO] = newCargo
            time.sleep(sleep_interval)
        print(('number of requested deploys=', req_deploy_count))
        print('-------SUMMARTY-------')
        print(('Number of deploys = {0}'.format(num_deployed)))
        print(('Number of deletions = {0}'.format(num_deleted)))
        print(('Number of resizes = {0}'.format(num_resized)))
        print(('Number of servers in Error State ='.format(len(servers_errored))))
        print(('Number of servers that timed out {0}'.\
            format(len(servers_timed_out))))
        if timed_stats:
            if stats[DEPLOY_COUNT] > 0:
                print(('deployed count:{0}, total time:{1}, average time{2}'.\
                    format(stats[DEPLOY_COUNT], stats[DEPLOY_SUM],
                           stats[DEPLOY_SUM] / stats[DEPLOY_COUNT])))
            if stats[DELETE_COUNT] > 0:
                print(('deleted count:{0}, total time:{1}, average time{2}'.\
                    format(stats[DELETE_COUNT], stats[DELETE_SUM],
                           stats[DELETE_SUM] / stats[DELETE_COUNT])))
            if stats[RESIZE_COUNT] > 0:
                print(('resize count:{0}, total time:{1}, average time{2}'.\
                    format(stats[RESIZE_COUNT], stats[RESIZE_SUM],
                           stats[RESIZE_SUM] / stats[RESIZE_COUNT])))

    def deploy_server(self, imageId, server_name_prefix, ip_addr, networkId,
                      deploy_flavor):
        myState = START
        server_name = \
            Utils.unique_server_name(server_name_prefix, ip_addr)
        for i in range(5):
            if deploy_flavor:
                server = Utils.create_server(self.authent_id, self.novaUrl,
                                         imageId, server_name,
                                         ip_addr,
                                         networkId,
                                         flavor_id=deploy_flavor)
            else:
                server = Utils.create_server(self.authent_id, self.novaUrl,
                                         imageId, server_name,
                                         ip_addr,
                                         networkId)
            if server:
                break
        if not server:
            print(('Error: No server instance for {0}, after {1} tries.'.\
                format(server_name, i)))
            return None
        print(('-{0}-Deploy Request for new Server named {1} with ip={2}'.\
            format(myState, server_name, ip_addr)))
        return server

    def start(self, cargo):
        return (DEPLOYING, cargo)

    def deploying(self, cargo):
        myState = DEPLOYING
        server = cargo[SERVER_DICT]
        # check to see if we have timed out
        delta = datetime.now() - cargo[STATE_START_TIME]
        if (delta > timedelta(seconds=cargo[WAIT_TO])):
            print(('-{0}-Forcing Server {1} to Error State for timeout'.\
                format(myState, server[NAME_KEY])))
            cargo[TIME_OUT_STATE_KEY] = myState
            return (ERROR, cargo)
        try:
            servStatus = Utils.get_server_status_dict(self.authent_id,
                                                      self.novaUrl,
                                                      server)
        except HttpError as e:
            print(('HTTP Error: {0}'.format(e.body)))
            os._exit(1)

        if not servStatus:
            print(('-{0}-Server {1} Error: Could not get Server Status'.\
                format(myState, server[NAME_KEY])))
            return (myState, cargo)

        status_changed = self.hasStatusChanged(cargo, servStatus)
        if status_changed:
            print(('-{0}-Server {1}: {2}'.format(myState, server[NAME_KEY],
                                                servStatus)))

        if not servStatus[TASK_STATE_KEY] and\
            servStatus[VM_STATE_KEY] == 'active' and\
            servStatus[HEALTH_VAL_KEY] == 'OK':
            print(('Deploy complete for Server:{0}'.format(server[NAME_KEY])))
            if cargo[STATS_DICT]:
                cargo[STATS_DICT][DEPLOY_SUM] += delta
                cargo[STATS_DICT][DEPLOY_COUNT] += 1
            cargo[STATE_START_TIME] = datetime.now()
            return (DEPLOY_COMPLETE, cargo)
        elif servStatus[VM_STATE_KEY] == 'error':
            print(('-{0}-Server {1} went to Error State during deploying'.\
                format(myState, server[NAME_KEY])))
            cargo['error_state'] = myState
            return (ERROR, cargo)
        else:
            return (myState, cargo)

    def deploy_complete(self, cargo):
        myState = DEPLOY_COMPLETE
        server = cargo[SERVER_DICT]
        # check to see if we have timed out
        delta = datetime.now() - cargo[STATE_START_TIME]
        if (delta > timedelta(seconds=cargo[WAIT_TO])):
            print(('-{0}-Forcing Server {1} to Error State for timeout'.\
                format(myState, server[NAME_KEY])))
            cargo[TIME_OUT_STATE_KEY] = myState
            return (ERROR, cargo)
        try:
            servStatus = Utils.get_server_status_dict(self.authent_id,
                                                      self.novaUrl, server)
        except HttpError as e:
            print(('HTTP Error: {0}'.format(e.body)))
            os._exit(1)
        if not servStatus:
            print(('-{0}-Server {1} Error: Could not get Server Status'.\
                format(myState, server[NAME_KEY])))
            return (myState, cargo)

        status_changed = self.hasStatusChanged(cargo, servStatus)
        if status_changed:
            print(('-{0}-Server {1}: {2}'.format(myState, server[NAME_KEY],
                                                servStatus)))

        if not servStatus[TASK_STATE_KEY] and\
            servStatus[VM_STATE_KEY] == 'active':
            print(('PowerUp complete for Server:{0}'.format(server[NAME_KEY])))
            next_state = cargo[POST_DEPLOY_STATE]

            if next_state == RESIZING:
                # call resize and return state RESIZING state
                Utils.resize_server(self.authent_id, self.novaUrl, server,
                                    cargo[RESIZE_FLAVID])
                print(('Request Resizing for Server:{0}'.\
                    format(server[NAME_KEY])))
                cargo[STATE_START_TIME] = datetime.now()
                return (RESIZING, cargo)
            elif next_state == DELETING:
                return (START_DELETE, cargo)
            else:
                print(('Request END for Server:{0}'.\
                    format(server[NAME_KEY])))
                return (DEPLOY_ADD, cargo)
        elif servStatus[VM_STATE_KEY] == 'error':
            print(('-{0}-Server {1} went to Error State during {2}'.\
                format(myState, server[NAME_KEY], myState)))
            return (ERROR, cargo)
        else:
            return (myState, cargo)

    def start_delete(self, cargo):
        return (DEPLOY_ADD, cargo)

    def deploy_add(self, cargo):
        return (END, cargo)

    def resizing(self, cargo):
        myState = RESIZING
        server = cargo[SERVER_DICT]
        # check to see if we have timed out
        delta = datetime.now() - cargo[STATE_START_TIME]
        if (delta > timedelta(seconds=cargo[WAIT_TO])):
            print(('-{0}-Forcing Server {1} to Error State for timeout'.\
                format(myState, server[NAME_KEY])))
            cargo[TIME_OUT_STATE_KEY] = myState
            return (ERROR, cargo)
        try:
            servStatus = Utils.get_server_status_dict(self.authent_id,
                                                      self.novaUrl,
                                                      server)
        except HttpError as e:
            print(('HTTP Error: {0}'.format(e.body)))
            os._exit(1)
        if not servStatus:
            print(('-{0}-Server {1} Error: Could not get Server Status'.\
                format(myState, server[NAME_KEY])))
            return (myState, cargo)

        status_changed = self.hasStatusChanged(cargo, servStatus)
        if status_changed:
            print(('-{0}-Server {1}: {2}'.format(myState, server[NAME_KEY],
                                                servStatus)))

        if not servStatus[TASK_STATE_KEY] and\
            servStatus[VM_STATE_KEY] == 'active' and\
            servStatus[HEALTH_VAL_KEY] == 'OK':
            print(('Resize complete for Server:{0}'.format(server[NAME_KEY])))
            if cargo[STATS_DICT]:
                cargo[STATS_DICT][RESIZE_SUM] += delta
                cargo[STATS_DICT][RESIZE_COUNT] += 1
            return (RESIZE_COMPLETE, cargo)
        elif servStatus[VM_STATE_KEY] == 'error':
            print(('-{0}-Server {1} went to Error State during Resize'.\
                format(myState, server[NAME_KEY])))
            return (ERROR, cargo)
        else:
            return (myState, cargo)

    def deleting(self, cargo):
        myState = DELETING
        server = cargo[SERVER_DICT]
        wait_timeout = cargo[WAIT_TO]
        delta = datetime.now() - cargo[STATE_START_TIME]
        if (delta > timedelta(seconds=wait_timeout)):
            print(('-{0}-Forcing Server {1} to Error State for timeout'.\
                format(myState, server[NAME_KEY])))
            return (ERROR, cargo)

        try:
            servStatus = Utils.get_server_status_dict(self.authent_id,
                                                      self.novaUrl,
                                                      server)
        except HttpError as e:
            if e.code == 404:
                print(('Deletion complete for Server:{0}'.\
                    format(server[NAME_KEY])))
                if cargo[STATS_DICT]:
                    cargo[STATS_DICT][DELETE_SUM] += delta
                    cargo[STATS_DICT][DELETE_COUNT] += 1
                return (DELETE_COMPLETE, cargo)
            else:
                print(('code={0} reason={1} body={2}'.format(e.code, e.reason,
                                                            e.body)))
                raise e
        if delta > (timedelta(seconds=wait_timeout) / 2):
            print(('Re-request Delete after {0}'.\
                format(delta)))
            try:
                Utils.delete_server(self.authent_id, self.novaUrl, server)
            except HttpError as e:
                print(('HTTP Error: {0}'.format(e.body)))
                os._exit(1)
        if not servStatus:
            print(('-{0}-Server {1} Error: Could not get Server Status'.\
                format(myState, server[NAME_KEY])))
            return (myState, cargo)

        status_changed = self.hasStatusChanged(cargo, servStatus)
        if status_changed:
            print(('-{0}-Server {1}: {2}'.format(myState, server[NAME_KEY],
                                                servStatus)))

        if servStatus[VM_STATE_KEY] == 'error':
            print(('-{0}-Server {1} went to Error State during Power Up'.\
                format(myState, server[NAME_KEY])))
            self.delete_errors.append(server[NAME_KEY])
            return (ERROR, cargo)
        else:
            return (myState, cargo)

    def delete_complete(self, cargo):
        return (END, cargo)

    def timed_out(self, cargo):
        return (END, cargo)

    def resize_complete(self, cargo):
        return (DEPLOY_ADD, cargo)

    def end_transition(self, cargo):
        print('Reached the End')
        return (END, cargo)

    def error_transition(self, cargo):
        print('Error transition')
        return (ERROR, cargo)

    def isStatusChanged(self, key_list, prev, current):
        for key in key_list:
            if key in prev and key in current:
                if prev[key] != current[key]:
                    return True
            elif key in prev or key in current:
                return True
        return False

    def hasStatusChanged(self, cargo, servStatus):
        return False
        if not 'servStatus' in cargo[SERVER_DICT]:
            cargo[SERVER_DICT]['servStatus'] = servStatus
            return True
        else:
            prevServStatus = cargo[SERVER_DICT]['servStatus']
            key_list = [TASK_STATE_KEY, VM_STATE_KEY, POWER_STATE_KEY,
                        HEALTH_VAL_KEY]
            status_changed = self.isStatusChanged(key_list, prevServStatus,
                                             servStatus)
            if status_changed:
                cargo[SERVER_DICT]['servStatus'] = servStatus
            return status_changed

    def cmpServers(self, value1, value2):
        if value1 < value2:
            return -1
        elif value1 > value2:
            return 1
        else:
            return 0

    def key_created(self, server):
        created_str = server['created']
        utc_str = created_str.replace('Z', 'UTC')
        key = datetime.strptime(utc_str, '%Y-%m-%dT%H:%M:%S%Z')
        return key

if __name__ == '__main__':
    svt_tester_base.main()
