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

from rest_framework import novaUtils
from rest_framework import svt_tester_base
from rest_framework.svt_tester_base import SvtTesterBase, VmTuple


class TbdTester(SvtTesterBase):
    """
    """

    def test_1000_TBD(self):
        '''BEGIN
        novaUrl = self.getServiceUrl('compute')
        hmcProps = {'access_ip': self.config_get('access_ip'),
                    'user_id': self.config_get('userid'),
                    'password': self.config_get('password'),
                    'hmc_display_name': self.config_get(
                        'hmc_display_name_list')
                    }
        print "Registering HMC... ", str(hmcProps)
        registrationResponse, registrationResponseBodyJSON = \
            novaUtils.registerHmc(novaUrl, self.authent_id, hmcProps)
        print "Registration of HMC response:"
        print str(registrationResponseBodyJSON)
        END'''


if __name__ == '__main__':
    svt_tester_base.main()
