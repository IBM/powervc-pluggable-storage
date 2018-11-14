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

import httplib
import importlib
import inspect
import traceback
import unittest
#import webob

from nose.loader import TestLoader

#from oslo_log import log as logging
#LOG = logging.getLogger(__name__)


def find_python_objects(dotted_name):
    """
    Parses 'dotted name' (string) to return tuple: (module, class, method).

    :param dotted_name: a string representing the fully qualified Python name
    of a package/module, class, or method

    :returns: 3-tuple of (module, class, method). Each may be None, and
    non-None only if its higher item (i.e., on its left) is also non-None.

    :raises: ValueError, indirectly from function 'find_class_and_method'.
    It also logs a warning if a module could not be imported or there were
    identifiable sections of the dotted_name
    """
    separ = '.'
    suffix = ""
    module = None
    first_import_warning_msg = None
    # Find the 'leaf' module of dotted_name, by parsing from right to left
    while len(dotted_name) > 0:
        try:
            module = importlib.import_module(dotted_name)
        except ImportError, e:
            if first_import_warning_msg is None:
                first_import_warning_msg = (
                    inspect.stack()[0][3] + ": '" + dotted_name
                    + "' received ImportError= " + str(e))
        if inspect.ismodule(module):
            break
        dotted_name, separ, right_substring = dotted_name.rpartition(separ)
        if len(suffix) == 0:
            suffix = right_substring
        else:
            suffix = right_substring + separ + suffix
    if not inspect.ismodule(module):
        if first_import_warning_msg is not None:
#            LOG.warn(first_import_warning_msg)
            pass
        return None, None, None
    else:
        try:
            # After module, check for class and method, then return all 3
            class_and_method = find_class_and_method(module, suffix)
            return module, class_and_method[0], class_and_method[1]
        except Exception as cm_exc:
            if first_import_warning_msg is not None:
#                LOG.warn(first_import_warning_msg)
                pass
            raise cm_exc


def find_class_and_method(module, class_method_name):
    """Returns the class/method with given name in the module; else None"""
    if len(class_method_name) == 0:
        return None, None
    error_msg_prefix = ("Module '" + module.__name__ + "' finding '"
                        + class_method_name + "': ")
    separ = '.'
    if class_method_name.count(separ) > 1:
        raise ValueError(error_msg_prefix + "Ill-formed names-string has "
                         "too many '" + separ + "' separators= "
                         + class_method_name.count(separ))
    class_name, separ, method_name = class_method_name.partition(separ)
    classes = inspect.getmembers(module, inspect.isclass)
    for cls in classes:
        if class_name == cls[0]:
            if len(method_name) == 0:
                return cls[1], None
            else:
                methods = inspect.getmembers(cls[1], inspect.ismethod)
                for mthd in methods:
                    if method_name == mthd[0]:
                        return cls[1], mthd[1]
                raise ValueError(error_msg_prefix + "Class '"
                                 + cls[1].__name__ + "' has no method '"
                                 + method_name + "'")
    raise ValueError(error_msg_prefix + "No class found "
                     "(hints: check URL for typos or logs for import errors "
                     "in modules)")


class TestRunnerUtility(object):
    """
    A PowerVC REST Controller for GET, which loads runs Python unit-tests.
    """
    _PARAM_HELP = "help"
    _PARAM_RUN = "run"

    def __init__(self):
        super(TestRunnerUtility, self).__init__()

    @property
    def pname_help(self):
        return TestRunnerUtility._PARAM_HELP

    @property
    def pname_run(self):
        return TestRunnerUtility._PARAM_RUN

    '''def index(self, req):
        """GET: Obtain TestCases and run them via a TestRunner.

        Q: Should this be done as POST instead (with params via data)?
        """
        response_type = 'text'
        response_body = ""
        try:
#            LOG.info("BEGIN " + self.__class__.__name__ + "."
#                     + inspect.stack()[0][3] + ": req.GET= " + str(req.GET))
            help_text_listed = False
            # Check parameter for: HELP
            if (len(req.GET) == 0 or
                    req.GET.get(self.pname_help, None)
                    is not None):
                response_body += self._text_for_help()
                help_text_listed = True
            if req.GET.get(self.pname_run, None) is not None:
                dotted_name_of_tests = req.GET.get(self.pname_run)
                testsuite = self.load_tests(dotted_name_of_tests)
                if help_text_listed:
                    response_body += "\n====[ Test Runs ]============\n"
                response_body += self._text_for_testsuite(testsuite)
                # Use standard test-runner to run the test-suite
                test_results = unittest.TextTestRunner(
                    verbosity=int(req.GET.get('verbosity', 2))).run(testsuite)
                response_body += self._text_for_results(test_results)
            else:
                response_body += ("----------------\n"
                                  + "UNRECOGNIZED PARAMETER(S):\n"
                                  + str(req.GET) + "\n--------\n")
                if not help_text_listed:
                    response_body += self._text_for_help()
        except:
            err_trace = traceback.format_exc()
#            LOG.warn(err_trace)
            response_body += err_trace
            response_body += "\n"
            response_body += ("For help, add request-parameter: &"
                              + self.pname_help)
        finally:
            pass
            return webob.Response(request=req,
                                  status=httplib.OK,
                                  content_type=response_type,
                                  body=response_body)'''

    def verify_python_objects(self, module, clazz, method, test_method_prefix,
                              error_msg_prefix):
        """Raise error if module/class/method are not plausible for tests."""
        if module is None:
            raise TypeError(error_msg_prefix + "Found no module.")
        if clazz is None:
            if method is not None:
                raise TypeError(error_msg_prefix + "Missing a class for "
                                "method= '" + str(method.__name__) + "'")
        else:
            test_superclass = unittest.TestCase
            if not issubclass(clazz, test_superclass):
                raise TypeError(error_msg_prefix + "Not a subclass of "
                                + test_superclass.__name__)
            if (method is not None and
                    not method.__name__.startswith(test_method_prefix)):
                raise TypeError(error_msg_prefix + "Method lacks "
                                "test prefix '" + test_method_prefix + "'")

    def load_tests(self, dotted_name_of_tests):
        """Returns a TestSuite of all tests in the named scope.

        The dotted name may specify a package, module, class, or method.
        All tests within the named scope will be recursively collected into
        a single TestSuite, which is returned.
        """
        module, clazz, method = find_python_objects(dotted_name_of_tests)
        error_msg_prefix = ("Parameter '" + self.pname_run
                            + "=" + dotted_name_of_tests + "': ")
        self._verify_python_objects(
            module, clazz, method, unittest.defaultTestLoader.testMethodPrefix,
            error_msg_prefix)
        '''LOG.info(inspect.stack()[0][3] + ": module= " + module.__name__
                 + ", class= "
                 + ("None" if clazz is None else clazz.__name__)
                 + ", method= "
                 + ("None" if method is None else method.__name__))'''
        testsuite = None
        if clazz is None:
            # Use nose TestLoader b/c unittest.loadTestsFromModule didn't work
            testsuite = TestLoader().loadTestsFromModule(module)
            #testsuite = unittest.defaultTestLoader.loadTestsFromModule(module)
            if testsuite.countTestCases() < 1:
                raise ValueError(error_msg_prefix + "No tests in module")
        else:
            if method is None:
                testsuite = unittest.defaultTestLoader.loadTestsFromTestCase(
                    clazz)
                '''LOG.info("Loaded from class '" + clazz.__name__ + "'= "
                         + str(testsuite.countTestCases()))
                if testsuite.countTestCases() < 1:
                    raise ValueError(error_msg_prefix + "No tests in class")'''
            else:
                testsuite = unittest.TestSuite(tests=[clazz(method.__name__)])
        return testsuite

    def _text_for_testsuite(self, testsuite, max_testsuite_listings=7):
        testsuite_text = ("TestSuite, total tests= "
                          + str(testsuite.countTestCases()) + "\n")
        listed_count = 0
        indent_str = "    "
        for test in testsuite:
            if listed_count >= max_testsuite_listings:
                testsuite_text += indent_str + "...etc.\n"
                break
            testsuite_text += indent_str + self._testsuite_to_str(test) + "\n"
            listed_count += 1
        return testsuite_text

    def _testsuite_to_str(self, test, max_tests=5):
        """Return a 1-line (string) representation of a TestSuite's content."""
        if not isinstance(test, unittest.TestSuite):
            return str(test.id().rpartition('.')[2])
        tests_str = ""
        ts_label = "TSuite"
        ts_classname = ts_label
        test_count = 0
        for tst in test:
            if isinstance(tst, unittest.TestCase):
                if ts_classname == ts_label:
                    ts_classname = str(tst.id().rpartition('.')[0])
                elif ts_classname != str(tst.id().rpartition('.')[0]):
                    ts_classname += " <various>"
            test_count += 1
            if test_count <= max_tests:
                tests_str += self._testsuite_to_str(tst)
            else:
                tests_str += "..."
                break
            if test_count < test.countTestCases():
                tests_str += ", "
        return (" (" + ts_classname + "= " + str(test.countTestCases())
                + ": " + tests_str + ")")

    def _text_for_results(self, test_results):
        """Return the result message (string) from running a TestSuite."""
        result_text = "\nRESULTS: " + str(test_results) + "\n"
        result_text += self._text_for_result_problems(
            test_results.errors, "ERROR")
        result_text += self._text_for_result_problems(
            test_results.failures, "Failure")
        return result_text

    def _text_for_result_problems(self, problems, label):
        """Return an error message (string) for problems from one test-run.
        :param problems: String for the problem details, usually a stacktrace
        :param label: String indicating whether the problem is an "error" or
        a "failure"
        """
        problem_text = ""
        num = 0
        for bad in problems:
            num += 1
            problem_text += ("\n----" + label + " " + str(num) + ": "
                             + str(bad[0]) + "----\n" + str(bad[1]) + "\n")
        return problem_text

    def _text_for_help(self):
        """Return the 'help' information as a string."""
        return ("URL: https://<SERVER>/powervc/openstack/compute/v2/"
                "<TENANT-ID>/test_runner?<PARM1>[=VAL1][&<P2>[=V2]]\n"
                "Parameters:\n"
                "  " + self.pname_help + " or <no parameters> - "
                "Show this listing\n"
                "\n"
                "  " + self.pname_run + "=<DOTTED-NAME OF: "
                "PACKAGE or MODULE or TestCase or test_method>\n"
                "    Recursively load and run all tests from all sources "
                "in the named scope.\n"
                "    A test is defined by a method beginning with 'test' "
                "on a subclass of 'unittest.TestCase'.\n"
                "\n"
                "    (cf. http://nose.readthedocs.org/en/latest/api/"
                "loader.html#unittest.TestLoader\n"
                "     and http://docs.python.org/2/library/unittest.html"
                "#unittest.TestLoader)\n"
                "\n"
                "Examples:\n"
                ".../test_runner?" + self.pname_run + "="
                "mytest.pkg - "
                "Run all tests recursively loaded from all packages/modules "
                "under package: 'mytest.pkg'\n"
                ".../test_runner?" + self.pname_run + "="
                "mytest.pkg&help - "
                "Same as above, but also show this help listing\n"
                ".../test_runner?" + self.pname_run + "="
                "mytest.pkg.mytest_module - "
                "Run all tests from all TestCase subclasses in module: "
                "'mytest_module.py'\n"
                ".../test_runner?" + self.pname_run + "="
                "mytest.pkg.mytest_module.MyTests - "
                "Run all tests from TestCase subclass: 'MyTests'\n"
                ".../test_runner?" + self.pname_run + "="
                "mytest.pkg.mytest_module.MyTests.test_001_foo - "
                "Run the single test: 'test_001_foo'\n"
                )
