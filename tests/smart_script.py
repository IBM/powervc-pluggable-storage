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

import traceback
import time
import subprocess
import os
import datetime
import sys

#Adding this comment just for Review

class SmartScript():
    """
    Smart script use to run any number of scripts in sequential order. User have to provide
    test suite file (svt_test_suite/test.suite) and configuration file (svt_config/svt.conf)
svt.conf Input format
[DEFAULT]
access_ip = <powerVC IP>
userid = <User Name>
password = <Password>
project = ibm-default
auth_version = 3

[TestCase]

#You have to provide all the scripts parameters which you planning to run as part of smart script
[test1]
:
:
[test2]
:
:
etc

test.suite Input format
<script1_name> : <test case name >
<script2 name> : <test case name >
<wait> : <wait time in seconds, minutes and hours)>
<script3 name> : <test case name > : <skip>
eg:
test_complex2_deploy_resize_delete_simple_SCG.py : test_1013_complex2_deploy
wait : 1h
pvc_host_based_conn_capture_off_servers.py : test_1001_capture_off_servers
wait : 10m
pvc_host_based_conn_stop_servers.py : test_1001_host_Based_stop_servers : skip
wait : 30s
pvc_host_based_conn_start_servers.py : test_1001_host_Based_start_servers

    """

    def test_smart(self):

        scripts=[]
        test_cases=[]
        skip_cases=[]
        config_file = str(sys.argv[2])
        print "="*50
        print "Reading Test Suite/n"
        suite_file = str(sys.argv[1])
        for line in open(suite_file):
            a = line
            try:
                a, b, c = line.split(':')
            except:
                c = "NONE"
                try:
                    a, b = line.split(':')
                except:
                    b = "NONE"

            a = a.strip()
            b = b.strip()
            c = c.strip()
            if c == "":
                c = "NONE"
            if b == "":
                b = "NONE"
            if b.lower() == "SKIP".lower():
                b = "NONE"
                c = "skip"
            if a != "":
                if a[0] != "#":
                    scripts.append(a)
                    test_cases.append(b)
                    skip_cases.append(c)
        if len(scripts) == 0:
            print "You not provided any inputs, nothing to do"
            os._exit(1)
        print "="*50
        if (len(scripts) == len(test_cases)):
            scripts_status = "<>"*60+"\n"
            scripts_status = scripts_status+" You can find scripts execution status below"+"\n"
            flag = 0
            for i in range(len(scripts)):
                #print scripts_status
                #print "<>"*60
                now = str(datetime.datetime.now())
                return_value = self.python_script_runner(scripts[i], test_cases[i], config_file)
                if return_value == 0:
                    print "\n Execution Success: "+scripts[i]+"  "+test_cases[i]+"\n"
                    script_name = scripts[i]
                    test_case = test_cases[i]
                    if script_name.lower() == 'WAIT'.lower() and test_case.lower() != 'NONE'.lower():
                        scripts_status = scripts_status+"\n Waiting : "+test_cases[i]+"\n"
                    else:
                        scripts_status = scripts_status+"\n Date & Time: "+now+"\n"
                        scripts_status = scripts_status+"\n Execution Success: "+scripts[i]+"\n"
                else:
                    temp_skip = str(skip_cases[i])
                    if temp_skip.lower() == "SKIP".lower():
                        flag = 2
                        print scripts[i]+" Script Failed, please check \n Proceeding with next Script since you choose SKIP"
                        scripts_status = scripts_status+"\n Date & Time: "+now+"\n"
                        scripts_status = scripts_status+"\n Script Failed: "+scripts[i]+"\n"+"Skipping Above Failure and Proceeding with Next Script Since You Chosen SKIP Failure \n "
                    else:
                        flag = 1
                        print scripts[i]+" Script Failed, please check \n"
                        scripts_status = scripts_status+"\n Date & Time: "+now+"\n"
                        scripts_status = scripts_status+"\n Script Failed: "+scripts[i]+"\n"
                        scripts_status = scripts_status+"\n Smart script stops running, you can fix the issue and retry remaining scripts\n"
                        break
            if flag == 0:
                scripts_status = scripts_status+"\n Smart Script: Scripts Execution is Success\n"
                scripts_status = scripts_status+"<>"*60
                print scripts_status
                os._exit(0)
            elif flag == 2:
                scripts_status = scripts_status+"\n Smart Script: Scripts Execution is Partially Success\n Please Rerun failed script after fixing issues \n"
                scripts_status = scripts_status+"<>"*60
                print scripts_status
                os._exit(0)
            else:
                scripts_status = scripts_status+"<>"*60
                print scripts_status
                os._exit(1)
        else:
            print '\n please check each script have corresponding test cases in the config file'


    #Python script runner
    def python_script_runner(self, script_name, test_case, config_file):
        if script_name.lower() == 'WAIT'.lower() and test_case.lower() != 'NONE'.lower():
            print "\n"+":"*130
            print "\n Waiting "+test_case
            wait_return= self.wait_time(test_case)
            if wait_return == 1:
                print "\nWrong Input given for wait time, ignoring wait and proceeding script execution"
            else:
                print "\nWait is over, proceeding script execution"
            return 0

        else:
            print "\n"+":"*130
            print "\n"*1+"Running python script: "+script_name+"\n"*1
            if test_case.lower() == 'NONE'.lower():
                cmd = 'python'+" -u"+" "+"tests_svt/"+script_name+" "+config_file
            else:
                cmd = 'python'+" -u"+" "+"tests_svt/"+script_name+" "+"--test="+test_case+" "+config_file
            print "\n"*1
            print cmd
            try:
                return_value = subprocess.call(cmd, shell=True)
                return return_value
            except:
                print "\nThere is some problem with running the script > "+cmd
                return 1

    # Adding Waiting time
    def wait_time(self, wait_t):
        try:
            time_type=wait_t[-1:]
            time_value=wait_t[:-1]
            if time_type.lower() == "h":
                print "Waiting "+time_value+" hour"
                float_time_value=float(time_value)
                i=0
                while i < float_time_value:
                    j=0
                    while j < 60:
                        time.sleep(60)
                        j=j+1
                    i=i+1
                    rem_time= float_time_value - i
                    if rem_time != 0:
                        print "Waiting another "+str(rem_time)+" hour"
                    else:
                        print "Waiting over, continuing with script execution"
                return 0

            elif time_type.lower() == "m":
                print time_value+" minutes"
                float_time_value=float(time_value)
                i=0
                while i < float_time_value:
                    time.sleep(60)
                    i=i+1
                return 0

            elif time_type.lower() == "s":
                print time_value+" seconds"
                float_time_value=float(time_value)
                time.sleep(float_time_value)
                return 0

            else:
                return 1
        except:
            return1
if __name__ == '__main__':
    inst = SmartScript()
    inst.test_smart()
