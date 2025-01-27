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
from builtins import str
from configparser import NoOptionError
import traceback
from rest_framework import novaUtils
from rest_framework import svt_tester_base
from rest_framework.svt_tester_base import SvtTesterBase
from rest_framework.restUtils import HttpError
from rest_framework.statemachine import StateMachine
from tests import Utils
import time
import subprocess
import sys
import paramiko
import os

#variables

FLAVOR_NAME = 'flavor_name'
DESIRED_RAM = 'desired_ram'
MIN_RAM = 'min_ram'
MAX_RAM = 'max_ram'
DESIRED_CPU = 'desired_cpu'
MIN_CPU = 'min_cpu'
MAX_CPU = 'max_cpu'
DESIRED_PROC_UNITS = 'desired_proc_units'
MIN_PROC_UNITS = 'min_proc_units'
MAX_PROC_UNITS = 'max_proc_units'
DISK_SIZE = 'disk_size'
REMOTE_RESTART = 'remote_restart'

"""
#compute template sample input from config file
[test_create_compute_templates]
flavor_name = ['test23','test24']
desired_ram = ['512','1024']
min_ram = ['512','512']
max_ram = ['2048','2048']
desired_cpu = ['1','1']
min_cpu = ['1','1']
max_cpu = ['1','1']
desired_proc_units = ['.5','.5']
min_proc_units = ['.1','.1']
max_proc_units = ['.7','.7']
disk_size = ['20','20']
remote_restart = <True or False>
"""


class CreateComputeTemplate(svt_tester_base.SvtTesterBase):

     required_options = [FLAVOR_NAME, DESIRED_RAM, MIN_RAM, MAX_RAM, DESIRED_CPU, MIN_CPU, MAX_CPU, DESIRED_PROC_UNITS,
                         MIN_PROC_UNITS, MAX_PROC_UNITS, DISK_SIZE, REMOTE_RESTART]
     #config_section = 'test_create_compute_templates'  # Ensure this is the right section

     def create_Props_for_compute_template(self, flavor_name, desired_ram, desired_cpu, disk_size):
        Props = {}
        Props['name'] = flavor_name
        Props['ram'] = desired_ram
        Props['vcpus'] = desired_cpu
        Props['disk'] =  disk_size
        Props['swap'] = '0'
        Props['OS-FLV-EXT-DATA:ephemeral'] = '0'
        Props['rxtx_factor'] = '1'
        return Props

     def create_Props_for_compute_template_advance(self, min_vcpu, max_vcpu, min_mem, max_mem, proc_units, min_proc_units, max_proc_units, remote_restart):
        Props = {}
        Props['powervm:min_vcpu'] = min_vcpu
        Props['powervm:max_vcpu'] = max_vcpu
        Props['powervm:min_mem'] = min_mem
        Props['powervm:max_mem'] = max_mem
        Props['powervm:proc_units'] = proc_units
        Props['powervm:min_proc_units'] = min_proc_units
        Props['powervm:max_proc_units'] = max_proc_units
        Props['powervm:srr_capability'] = remote_restart
        Props['powervm:processor_compatibility'] = "default"
        Props['powervm:availability_priority'] = "127"
        Props['powervm:dedicated_proc'] = "false"
        Props['powervm:shared_proc_pool_name'] = "DefaultPool"
        Props['powervm:uncapped'] = "true"
        Props['powervm:shared_weight'] = "128"
        return Props

     def test_create_compute_templates(self):
        options_missing = False
        for option in self.required_options:
            if not self.config.has_option(self.config_section, option):
                print('option=', option, 'not found in configuration file')
                options_missing = True
        if options_missing:
            print(f'Provide missing options in the configuration file {self.config}, {self.config_section}.')
            os._exit(1)

        novaUrl = self.getServiceUrl('compute')
        print(f"self.config_get is {self.config_get}")
        flavor_name = self.config_get(FLAVOR_NAME)
        desired_ram = self.config_get(DESIRED_RAM)
        desired_cpu = self.config_get(DESIRED_CPU)
        disk_size = self.config_get(DISK_SIZE)
        min_vcpu = self.config_get(MIN_CPU)
        max_vcpu = self.config_get(MAX_CPU)
        min_mem = self.config_get(MIN_RAM)
        max_mem = self.config_get(MAX_RAM)
        proc_units = self.config_get(DESIRED_PROC_UNITS)
        min_proc_units = self.config_get(MIN_PROC_UNITS)
        max_proc_units = self.config_get(MAX_PROC_UNITS)
        remote_restart = self.config_get(REMOTE_RESTART)
        remote_restart = str(remote_restart)

        if remote_restart.lower() == "true":
            remote_restart = "true"
        else:
            remote_restart = "false"

        i=0

        for i in range(len(flavor_name)):
            flavor_name1 = flavor_name[i]
            desired_ram1 = desired_ram[i]
            desired_cpu1 = desired_cpu[i]
            disk_size1 = disk_size[i]
            min_vcpu1 = min_vcpu[i]
            max_vcpu1 = max_vcpu[i]
            min_mem1 = min_mem[i]
            max_mem1 = max_mem[i]
            proc_units1 = proc_units[i]
            min_proc_units1 = min_proc_units[i]
            max_proc_units1 = max_proc_units[i]
            Props = self.create_Props_for_compute_template(flavor_name1, desired_ram1, desired_cpu1, disk_size1)
            Props2 = self.create_Props_for_compute_template_advance(min_vcpu1, max_vcpu1, min_mem1, max_mem1, proc_units1, min_proc_units1, max_proc_units1, remote_restart)
            print("Create Compute Template:", str(Props))
            #time.sleep(10)

            try :
                registrnRespns, registrnRespnsBodyJSON = novaUtils.createComputeTemplate(novaUrl, self.authent_id , Props)
                print("Create Compute Template response:")
                print(str(registrnRespnsBodyJSON))
                flavor_id = str(registrnRespnsBodyJSON['flavor']['id'])
                registrnRespns, registrnRespnsBodyJSON = novaUtils.createComputeTemplateAdvance(novaUrl, self.authent_id , Props2, flavor_id)
                print("Create Advance Compute Template response:")
                print(str(registrnRespnsBodyJSON))
                time.sleep(20)

            except HttpError as e:
                print('HTTP Error: {0}'.format(e.body))
                os._exit(1)

            i += 1
       # else :
       #     print 'please check the neo Host registration parameters'


if __name__ == '__main__':
    svt_tester_base.main()
