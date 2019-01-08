#!/usr/bin/python
# Classification (U)

"""Program:  run_program.py

    Description:  Unit testing of run_program in elastic_db_dump.py.

    Usage:
        test/unit/elastic_db_dump/run_program.py

    Arguments:
        None

"""

# Libraries and Global Variables

# Standard
import sys
import os

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

# Third-party
import mock

# Local
sys.path.append(os.getcwd())
import elastic_db_dump
import lib.gen_libs as gen_libs
import version

# Version
__version__ = version.__version__


def list_dumps(ES, **kwargs):

    """Function:  list_dumps

    Description:  This is a function stub for elastic_db_dump.list_dumps.

    Arguments:
        ES -> Stub argument holder.

    """

    pass


def disk_usage(ES, **kwargs):

    """Function:  disk_usage

    Description:  This is a function stub for elastic_db_dump.disk_usage.

    Arguments:
        ES -> Stub argument holder.

    """

    pass


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Super-Class:  unittest.TestCase

    Sub-Classes:  None

    Methods:
        setUp -> Unit testing initilization.
        test_func_call_multi -> Test run_program with multiple calls.
        test_func_call_one -> Test run_program with one call to function.
        test_func_call_zero -> Test run_program with zero calls to function.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:
            None

        """

        class CfgTest(object):

            """Class:  CfgTest

            Description:  Class which is a representation of a cfg module.

            Super-Class:  object

            Sub-Classes:  None

            Methods:
                __init__ -> Initialize configuration environment.

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the CfgTest class.

                Arguments:
                        None

                """

                self.host = "SERVER_NAME"
                self.port = 9200

        self.CT = CfgTest()

        self.args = {"-c": "config_file", "-d": "config_dir"}
        self.func_dict = {"-L": list_dumps, "-U": disk_usage}

    @mock.patch("elastic_db_dump.gen_libs.load_module")
    @mock.patch("elastic_db_dump.elastic_class.ElasticSearchDump")
    @mock.patch("elastic_db_dump.gen_class")
    def test_func_call_multi(self, mock_lock, mock_class, mock_load):

        """Function:  test_func_call_multi

        Description:  Test run_program function with multiple calls to
            function.

        Arguments:
            mock_lock -> Mock Ref:  elastic_db_dump.gen_class
            mock_class -> Mock Ref:
                elastic_db_dump.elastic_class.ElasticSearchDump
            mock_load -> Mock Ref:  elastic_db_dump.gen_libs.load_module

        """

        self.args["-U"] = True
        self.args["-L"] = True

        mock_lock.ProgramLock = elastic_db_dump.gen_class.ProgramLock
        mock_class.return_value = "Elastic_Class"
        mock_load = self.CT

        self.assertFalse(elastic_db_dump.run_program(self.args,
                                                     self.func_dict))

    @mock.patch("elastic_db_dump.gen_libs.load_module")
    @mock.patch("elastic_db_dump.elastic_class.ElasticSearchDump")
    @mock.patch("elastic_db_dump.gen_class")
    def test_func_call_one(self, mock_lock, mock_class, mock_load):

        """Function:  test_func_call_one

        Description:  Test run_program function with one call to function.

        Arguments:
            mock_lock -> Mock Ref:  elastic_db_dump.gen_class
            mock_class -> Mock Ref:
                elastic_db_dump.elastic_class.ElasticSearchDump
            mock_load -> Mock Ref:  elastic_db_dump.gen_libs.load_module

        """

        self.args["-L"] = True

        mock_lock.ProgramLock = elastic_db_dump.gen_class.ProgramLock
        mock_class.return_value = "Elastic_Class"
        mock_load = self.CT

        self.assertFalse(elastic_db_dump.run_program(self.args,
                                                     self.func_dict))

    @mock.patch("elastic_db_dump.gen_libs.load_module")
    @mock.patch("elastic_db_dump.elastic_class.ElasticSearchDump")
    @mock.patch("elastic_db_dump.gen_class")
    def test_func_call_zero(self, mock_lock, mock_class, mock_load):

        """Function:  test_func_call_zero

        Description:  Test run_program function with zero calls to function.

        Arguments:
            mock_lock -> Mock Ref:  elastic_db_dump.gen_class
            mock_class -> Mock Ref:
                elastic_db_dump.elastic_class.ElasticSearchDump
            mock_load -> Mock Ref:  elastic_db_dump.gen_libs.load_module

        """

        mock_lock.ProgramLock = elastic_db_dump.gen_class.ProgramLock
        mock_class.return_value = "Elastic_Class"
        mock_load = self.CT

        self.assertFalse(elastic_db_dump.run_program(self.args,
                                                     self.func_dict))


if __name__ == "__main__":
    unittest.main()
