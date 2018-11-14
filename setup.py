"""
  Copyright IBM Corp. 2018.
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
      http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
"""

import os

from setuptools import setup, find_packages

setup(

    # the name of the top-level package. Must match the directory name on the
    # filesystem
    name='powerVC_Open_Source_Test_Suite',

    # ENV variables for each package will be set during the build. Work with
    # build team to ensure they are set for your package.
    version=os.environ.get('MY_PACKAGE_VERSION', '9.9.9.9'),

    # a short description - shows up as the packages "Summary"
    description='Open Source Test Suite for validate pluggable storage driver',

    author="IBM PowerVC Team",
    author_email=None,       # looking for an external email address still....

    platforms='RHEL 7.3',

    license='Apache License',

    # these packages will be bundled into the egg
    packages=find_packages(exclude=['config', 'test_suite']),

    # list of scripts to ship
    scripts=[],

    test_suite='',

    # classifiers - see list at
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Environment :: Openstack'
    ]

)
