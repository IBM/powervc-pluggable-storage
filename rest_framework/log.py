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

import datetime

logFile = None

class LogError :
    def __init__(self, msg) :
        self.msg = msg
    def __repr__(self) :
        return 'LogError(msg=%r)' % (self.msg)

def init() :
    global logFile
    if not logFile :
        logFile = open('log.txt', 'a+')
        logFile.write('\n---------------------------------\n')
        logFile.write('-----  ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '  -----')
        logFile.write('\n---------------------------------\n')

def write(msg) :
    if logFile :
        logFile.write(msg)
    else :
        raise LogError(msg)

def done() :
    global logFile
    if logFile :
        logFile.close()
        logFile = None
