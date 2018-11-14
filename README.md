PowerVC Test Suite For Pluggable Storage Driver Validation
---------------
This test suite provides the REST testing support to validate the pluggable storage driver on PowerVC.
The tests validate to see if the storage driver is compatible with PowerVC VM life-cycle functions.


Getting Started
---------------
Download **powervc-pluggable-storage** into any Linux or Windows systems which supports Python 2.7.
If you downloaded the zip file then extract the contents to a folder.
Verify if your folder has these files:

**config**: This folder is used for storing all configuration files. A sample configuration file
         'Storage_driver_test.conf' is available for reference.

**powerVC_rest_tools.egg-info**: This folder has different files which has information related
                              to the test framework.

**rest_framework**: This folder contains all base framework related Utils files.

**setup.py**: This Python script will do the base installation of framework.

**tests**: All test scripts are available in this folder.

**test_suite**: Test suite files should be stored into this path. A sample test suite file
                'Storage_driver_test.testSuite' and clean_up test suite file 'clean_up.testSuite'
                are available for running pre-defined lists of reference test cases.


Prerequisites
-------------
Prerequisites to run the framework:

1. Python 2.7 is required on the system where you planning to run tests.
2. PowerVC should be installed.
3. All the resources like HMC, Hosts, Storages and Switches should already be registered into PowerVC.
   Refer below PowerVC KC links for more information:
   https://www.ibm.com/support/knowledgecenter/en/SSXK2N_1.4.1/com.ibm.powervc.standard.help.doc/kc_welcome-standard-supermap.html
   https://www.ibm.com/support/knowledgecenter/en/SSXK2N_1.4.1/com.ibm.powervc.standard.help.doc/powervc_pluggable_v_integrated.html
   https://www.ibm.com/support/knowledgecenter/en/SSXK2N_1.4.1/com.ibm.powervc.standard.help.doc/powervc_pluggable_storage.html
4. Images and Network should already be created. More information:
   https://www.ibm.com/support/knowledgecenter/en/SSXK2N_1.4.1/com.ibm.powervc.standard.help.doc/PowerVC_creating_initial_vm.html


Installation
-------------
To install the framework on your system, go to the framework folder **powervc-pluggable-storage**
and run setup.py like below:


`python setup.py install`


Running the tests
-----------------

We have two reference test suites

Basic
------
Config: Basic_storage_driver_test.conf

Test Suite: Basic_storage_driver_test.testSuite

Advanced
---------
Config: Storage_driver_test.conf

Test Suite: Storage_driver_test.testSuite

Go to the framework folder **powervc-pluggable-storage** and run test suite like below:

` nohup python -u tests/smart_script.py <test suite file path> <configuration file path> & `

eg:

`nohup python -u tests/smart_script.py test_suite/Basic_storage_driver_test.testSuite config/Basic_storage_driver_test.conf & `

or

` nohup python -u tests/smart_script.py test_suite/Storage_driver_test.testSuite config/Storage_driver_test.conf & `

When you run the script using nohup there will be a output file generated like `nohup.out`.

You can see the test execution progress using `nohup.out` file as follows:

`tail -f nohup.out`


Test configuration file
-----------------------
Each test script expects required inputs from configuration file so please make sure you update the
configuration file for each script which you plan to run.

You can refer to the sample configuration file provided in the below path:

powerVC_Open_Source_Test_Suite/config/Storage_driver_test.conf


Test Suite file
---------------
The test suite file defines the list of tests that will be run. Each test has its own python module.
The sample reference test suites provided can be found in the following directory:

PowerVC_Open_Source_Test_Suite/test_suite/

You can edit the sample files as described in each or create your own additional test suites.


Validation
----------
Manual validation is required to certify that all tests work fine. Use PowerVC messages to track failures and errors happening during test suite execution.


Test coverage as part of Basic Storage Driver Test Suite
------------------------------------------------------
The test execution will follow the following flow. To see or edit the default values of parameters used by each test case, refer to the test case module.

1. Compute template creation for Deploy and Resize using different size disks: test_create_compute_template.py<br>
2. Concurrent Scale run using multiple images and multiple SCGs: test_complex2_deploy_resize_delete_simple_SCG.py<br>
3. Create volumes one by one: pvc_create_volumes.py<br>
4. Concurrent attach of volumes to VMs: pvc_host_based_conn_attach_volume.py<br>
5. Active concurrent capture of VMs: pvc_host_based_Active_capture_off_servers.py<br>
6. Active resize of VMs: pvc_host_based_conn_Active_resize_new2.py<br>

Test coverage as part of Advanced Storage Driver Test Suite
--------------------------------------------------------
The test execution will follow the following flow. To see or edit the default values of parameters used by each test case, refer to the test case module.

1. Compute template creation for Deploy and Resize using different size disks: test_create_compute_template.py<br>
2. Concurrent Scale run using multiple images and multiple SCGs: test_complex2_deploy_resize_delete_simple_SCG.py<br>
3. Bulk volumes creation: pvc_create_Bulkvolumes.py<br>
4. Bulk volume attach: pvc_host_based_bulk_volume_attach.py<br>
5. Concurrent detach of volumes: pvc_host_based_conn_detach_volume.py<br>
6. Unmanage volumes from PowerVC: pvc_UnmanageVolumes.py<br>
7. Active concurrent capture of VMs: pvc_host_based_Active_capture_off_servers.py<br>
8. Active resize of VMs: pvc_host_based_conn_Active_resize_new2.py<br>
9. Concurrent migration of VMs: test_selective_migration.py<br>
11. Onboard volumes from storage, by default PowerVC not support manage volumes for pluggable storage driver: pvc_OnboardVolumes.py<br>

Clean_up
--------
Go to the framework folder **powervc-pluggable-storage** and run test suite like below:

`nohup python -u tests/smart_script.py <test suite file path> <configuration file path> &`

eg:

`nohup python -u tests/smart_script.py test_suite/clean_up.testSuite config/Storage_driver_test.conf &`


When you run the script using nohup there will be a output file generated like `nohup.out`

You can see the test execution progress using `nohup.out` file as follows:

`tail -f nohup.out`

The clean_up suite will cover below scenarios

1. Concurrent delete of VMs: 'pvc_conn_delete_all_vms.py'

2. Concurrent delete of images: 'delete_all_images.py'

3. concurrent delete of volumes: 'pvc_delete_volumes_except_volume_name_startwith_DND.py'

Useful Information
--------------------
1. If deploys are failing with error saying volume name length exceeds supported length by storage, then you
   can reduce volume length using PowerVC CLI command 'powervc-config storage vol-name-format -h'.

2. For some reason if you want to stop test suite execution, please find the process and kill it

eg:
`ps -aux | grep smart`

`kill -9 <process ID>`
