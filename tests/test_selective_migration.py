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
from rest_framework.restUtils import HttpError
from rest_framework.statemachine import StateMachine
from tests import Utils
import time
import os
#Variables for report generation
success_VM = []
failed_VM = []
total_Success = 0
total_failure = 0

BEGIN_STATE = 'START'
MIGRATING_STATE = 'MIGRATING'
MIGRATION_COMPLETE_STATE = 'MIGRATION_COMPLETE'
MIGRATING_BACK_STATE = 'MIGRATING_BACK'
END_STATE = 'END'
ERROR_STATE = 'ERROR'
MAX_MIGRATIONS = 'max_migrations'
SRV_NAME_PREFIX = 'server_name_prefix'
START_IP = 'starting_ip_address'
NET_NAME = 'network_name'
SRC_HOST = 'source_host'
DEST_HOST = 'destination_host'
CONCURRENT_MIGRATIONS = 'concurrent_migrations'

class SvtMobilityTester(svt_tester_base.SvtTesterBase):
    """
    Tester for performing a migrations using configured lists of servers
    and a list of hosts to migrate to. The lists should be in 1 to 1
    correspondence and of the same length. The test will attempt to migrate
    each server to its associated destination host. If it encounters a
    destination host that is already a source host, or a source host that is
    a destination, then that migration will be postponed until the other
    migration has finished.

    Test case included:
    test_1005_live_mobility
    test_live_mobility.py --test=test_1005_live_mobility <path to config file>

    Currently number_of_cycles is not used, but it is still required to be in
    the config file.

    if its not executable, use chmod +x pvc_show_servers.py

    options needed in config file
    [DEFAULT]
    host_type = powervm
    install_type = [standard|express]
    access_ip = <ip addresss or hostname of PowerVC server>
    userid = <userid with admin group access in PowerVC>
    password = <password for the userid>
    project = ibm-default
    auth_version = 3

    [TestCase]
    [test_1005_concurrent_deploy_resize]
    migrating_vm_list = <list of servers in python list syntax>
    destination_hosts = <list of MTMS host names in python list syntax>
    max_concurrent_migrations = <maximum migrations at one time>
    """
    required_options = [MAX_MIGRATIONS, SRV_NAME_PREFIX, SRC_HOST, DEST_HOST,
                        CONCURRENT_MIGRATIONS
                        ]
    dest_hosts = []
    src_hosts = []

    def test_1006_selective_migration(self):
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print('option=', option, 'not found in configuration file')
                options_missing = True
        if options_missing:
            print('Provide missing options to the configuration file.')
            os._exit(1)

        max_migrations = self.config_get(MAX_MIGRATIONS)
        print(MAX_MIGRATIONS, max_migrations)
        server_name_prefix = self.config_get(SRV_NAME_PREFIX)
        print(SRV_NAME_PREFIX, server_name_prefix)
        src_host = self.config_get(SRC_HOST)
        print(SRC_HOST, src_host)
        dest_host = self.config_get(DEST_HOST)
        print(DEST_HOST, dest_host)
        concurrent_migrations = \
            self.config_get(CONCURRENT_MIGRATIONS)
        print(CONCURRENT_MIGRATIONS, concurrent_migrations)

        sm = StateMachine()
        sm.add_state(BEGIN_STATE, self.migrate_server)
        sm.add_state(MIGRATING_STATE, self.migrating)
        sm.add_state(MIGRATION_COMPLETE_STATE, self.migrated)
        sm.add_state(END_STATE, self.end_transition, end_state=1)
        sm.add_state(ERROR_STATE, self.error_transition, end_state=1)
        sm.set_start(BEGIN_STATE)

        vm_list = Utils.get_server_list(self.authent_id, self.novaUrl)
        to_be_migrated = []
        error_servers = []
        success_servers = []
        server_list = []
        count = 0

        for vm in vm_list:
            if vm['name'].startswith(server_name_prefix):
                try:
                    servStatus = Utils.get_server_status_dict(self.authent_id,
                                                              self.novaUrl, vm)
                except HttpError as e:
                    print('HTTP Error: {0}'.format(e.body))
                    os._exit(1)
                if servStatus and 'host' in servStatus and\
                    servStatus['host'] == src_host and\
                    servStatus['vm_state'] == 'active' and\
                    servStatus['health_value'] == 'OK':
                    to_be_migrated.append(vm)
                    if len(to_be_migrated) == max_migrations:
                        break
            print('.', end=' ')
            count += 1
            if count == 80:
                print('')
                count = 0

        if not to_be_migrated:
            print('')
            print('No Servers found starting with {0} for host {1}:', \
                   server_name_prefix, src_host)
        else:
            print('')
            print('to_be_migrated=', str(to_be_migrated))
        try:
            error_servers, success_servers =\
                self.execute_migrations(to_be_migrated,
                                    concurrent_migrations,
                                    max_migrations, src_host, dest_host, sm)
        except HttpError as e:
            print('HTTP Error: {0}'.format(e.body))
            os._exit(1)

        print('error_servers=', str(error_servers))
        print('success_servers=', str(success_servers))

    def execute_migrations(self, to_be_migrated, concurrent_migrations,
                           max_migrations, src_host, dest_host, sm):
        work_item_list = []
        error_servers = []
        success_servers = []
        migrations_requested = 0
        while work_item_list[:] or to_be_migrated[:]:
            # Count the number of severs that are deploying
            concurrent_running = 0
            for work_item in work_item_list:
                if work_item['state'] == MIGRATING_STATE or\
                    work_item['state'] == BEGIN_STATE:
                    concurrent_running += 1
            # request as many deploys as possible to meet the concurrent value
            while concurrent_running < concurrent_migrations and \
                to_be_migrated[:]:
                print('concurrent_running', concurrent_running)
                newCargo = {}
                newCargo['server'] = to_be_migrated.pop(0)
                newCargo['dest_host'] = dest_host
                newCargo['src_host'] = src_host
                work_item_list.append({'state': BEGIN_STATE,
                                       'cargo': newCargo})
                concurrent_running += 1
                migrations_requested += 1
                print('***Migrating:{0}'.\
                    format(newCargo['server']['name']))

            for work_item in work_item_list:
                currentState = work_item['state']
                currentCargo = work_item['cargo']
                if sm.is_end_state(currentState):
                    work_item_list.pop(0)
                    print('work_item finished', str(work_item))
                    if currentState == ERROR_STATE:
                        error_servers.append(currentCargo['server'])
                    elif work_item['state'] == END_STATE:
                        success_servers.append(currentCargo['server'])
                    continue
                # get updated state and cargo
                (nextState, nextCargo) = sm.step(currentState, currentCargo)
                if nextState != currentState:
                    print('{0} -> {1}'.format(currentState, nextState))
                # update work_item
                work_item['state'] = nextState
                work_item['cargo'] = nextCargo
            time.sleep(30)
        return (error_servers, success_servers)

    def migrate_server(self, cargo):
        myState = BEGIN_STATE
        token = self.authent_id
        novaUrl = self.novaUrl
        server = cargo['server']
        to_host = cargo['dest_host']
        for i in range(5):
            try:
                Utils.live_migrate(token, novaUrl, server, to_host)
                print('-{0}-Migrate Request for Server named {1}'.\
                    format(myState, server['name']))
                break
            except HttpError as e:
                if i == 4:
                    raise e
        return (MIGRATING_STATE, cargo)

    def migrating(self, cargo):
        myState = MIGRATING_STATE
        server = cargo['server']
        try:
            servStatus = Utils.get_server_status_dict(self.authent_id,
                                                  self.novaUrl,
                                                  server)
        except HttpError as e:
            print('HTTP Error: {0}'.format(e.body))
            os._exit(1)

        if not servStatus:
            print('-{0}-Server {1} Error: Could not get Server Status'.\
                format(myState, server['name']))
            return (ERROR_STATE, cargo)

        if not 'servStatus' in server:
            print('-{0}-Server {1}: {2}'.format(myState, server['name'],
                                                servStatus))
            server['servStatus'] = servStatus
            cargo['server'] = server
        else:
            prevServStatus = server['servStatus']
            key_list = ['task_state', 'vm_state', 'power_state',
                        'health_value']
            status_changed = self.isStatusChanged(key_list, prevServStatus,
                                             servStatus)
            if status_changed:
                print('-{0}-Server {1}: {2}'.format(myState, server['name'],
                                                    servStatus))
                server['servStatus'] = servStatus
                cargo['server'] = server

        if not servStatus['task_state'] and\
            servStatus['vm_state'] == 'active' and\
            servStatus['health_value'] == 'OK' and\
            servStatus['power_state'] == 1:
            if servStatus['host'] != cargo['src_host']:
                print('Migration complete for Server:{0}'.format(server['name']))
                return (MIGRATION_COMPLETE_STATE, cargo)
            else:
                # migration actually failed but state is set back to original
                print('-{0}-Server {1} s not migrated'.\
                        format(myState, server['name']))
                return (ERROR_STATE, cargo)
        elif servStatus and servStatus['vm_state'] == 'error':
            print('-{0}-Server {1} went to Error State while migrating'.\
                format(myState, server['name']))
            return (ERROR_STATE, cargo)
        else:
            return (myState, cargo)

    def migrated(self, cargo):
        return (END_STATE, cargo)

    def end_transition(self, cargo):
        print('Reached the End')
        return (END_STATE, cargo)

    def error_transition(self, cargo):
        print('Error transition')
        return (ERROR_STATE, cargo)

    def isStatusChanged(self, key_list, prev, current):
        for key in key_list:
            if key in prev and key in current:
                if prev[key] != current[key]:
                    return True
            elif key in prev or key in current:
                return True
        return False

if __name__ == '__main__':
    svt_tester_base.main()
