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
from rest_framework import validatorUtils
from rest_framework import novaUtils
import os
import time



class SVTTTVValidator(svt_tester_base.SvtTesterBase):

    def test_1501_pvc_validate_env(self):

        count = 0
        check_status = 'fail'
        time_out_value = 90

        validatorUrl = self.getServiceUrl('ttv')
        novaUrl = self.getServiceUrl('compute')
        auth_token = self.authent_id
        ttv_error_flag = False

        list_host_output=novaUtils.listHosts(novaUrl,self.authent_id)[1]
        all_hosts = list_host_output['hosts']
        print(all_hosts)
        for host_record in all_hosts:
            if host_record['service'] == 'compute':
                count = count +1
        print(" Total Number of Hosts =", count)
        total_time_out = time_out_value * count

        """ run TTV or verify environment and display results"""

        ttv_run_op =validatorUtils.initValidationRun(validatorUrl,auth_token)
        print(" ----------waiting for TTV to complete---------")
        time.sleep(total_time_out)
        ttv_results = validatorUtils.getValidationResult(validatorUrl,auth_token)

        output= ttv_results[1]['prior-results'][0]['check-groups']

        print("\n")
        for item in output:
            validations = output[item]['checks']
            for validation in validations:
                if check_status in validation['status']:
                    ttv_error_flag = True
                    print(output[item]['group-description']+" ----- "+validation['ip'] +" ----- " +validation['status'] + " ----- " + validation['msg'])

        if ttv_error_flag:
            print("FAIL: TTV reported errors. Please check your environment")
            os._exit(1)
        else:
            print("SUCCESS: TTV run is successful without any errors")
            os._exit(0)

if __name__ == '__main__':
    svt_tester_base.main()
