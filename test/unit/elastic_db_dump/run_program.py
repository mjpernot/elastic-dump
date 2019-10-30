#!/usr/bin/python
# Classification (U)

"""Program:  run_program.py

    Description:  Unit testing of run_program in elastic_db_dump.py.

    Usage:
        test/unit/elastic_db_dump/run_program.py

    Arguments:

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

__version__ = version.__version__


def list_dumps(es, **kwargs):

    """Function:  list_dumps

    Description:  This is a function stub for elastic_db_dump.list_dumps.

    Arguments:
        es -> Stub argument holder.

    """

    pass


def disk_usage(es, **kwargs):

    """Function:  disk_usage

    Description:  This is a function stub for elastic_db_dump.disk_usage.

    Arguments:
        es -> Stub argument holder.

    """

    pass


class ProgramLock(object):

    """Class:  ProgramLock

    Description:  Mock of the gen_class.ProgramLock class.

    Methods:
        __init__ -> Class instance initilization.
        __del__ -> Deletion of the ProgramLock instance.

    """

    def __init__(self, argv, flavor_id=""):

        """Method:  __init__

        Description:  Initialization of an instance of the ProgramLock class.

        Arguments:
            (input) argv -> Arguments from the command line.
            (input) flavor_id -> Unique identifier for an instance.

        """

        self.lock_created = True

    def __del__(self):

        """Method:  __del__

        Description:  Deletion of the ProgramLock instance.

        Arguments:

        """

        return True


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Unit testing initilization.
        test_exception_handler -> Test with exception handler.
        test_func_call_multi -> Test run_program with multiple calls.
        test_func_call_one -> Test run_program with one call to function.
        test_func_call_zero -> Test run_program with zero calls to function.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        class CfgTest(object):

            """Class:  CfgTest

            Description:  Class which is a representation of a cfg module.

            Methods:
                __init__ -> Initialize configuration environment.

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the CfgTest class.

                Arguments:

                """

                self.host = "SERVER_NAME"
                self.port = 9200

        self.ct = CfgTest()

        self.args = {"-c": "config_file", "-d": "config_dir"}
        self.func_dict = {"-L": list_dumps, "-U": disk_usage}

    @mock.patch("elastic_db_dump.gen_libs.load_module")
    @mock.patch("elastic_db_dump.elastic_class.ElasticSearchDump")
    @mock.patch("elastic_db_dump.gen_class.ProgramLock")
    def test_exception_handler(self, mock_lock, mock_class, mock_load):

        """Function:  test_exception_handler

        Description:  Test with exception handler.

        Arguments:

        """

        self.args["-U"] = True
        self.args["-L"] = True

        mock_lock.side_effect = \
            elastic_db_dump.gen_class.SingleInstanceException
        mock_class.return_value = "Elastic_Class"
        mock_load.return_value = self.ct

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.run_program(self.args,
                                                         self.func_dict))

    @mock.patch("elastic_db_dump.gen_libs.load_module")
    @mock.patch("elastic_db_dump.elastic_class.ElasticSearchDump")
    @mock.patch("elastic_db_dump.gen_class")
    def test_func_call_multi(self, mock_lock, mock_class, mock_load):

        """Function:  test_func_call_multi

        Description:  Test run_program function with multiple calls to
            function.

        Arguments:

        """

        self.args["-U"] = True
        self.args["-L"] = True

        mock_lock.ProgramLock.return_value = ProgramLock([], "FlavorID")
        mock_class.return_value = "Elastic_Class"
        mock_load.return_value = self.ct

        self.assertFalse(elastic_db_dump.run_program(self.args,
                                                     self.func_dict))

    @mock.patch("elastic_db_dump.gen_libs.load_module")
    @mock.patch("elastic_db_dump.elastic_class.ElasticSearchDump")
    @mock.patch("elastic_db_dump.gen_class")
    def test_func_call_one(self, mock_lock, mock_class, mock_load):

        """Function:  test_func_call_one

        Description:  Test run_program function with one call to function.

        Arguments:

        """

        self.args["-L"] = True

        mock_lock.ProgramLock.return_value = ProgramLock([], "FlavorID")
        mock_class.return_value = "Elastic_Class"
        mock_load.return_value = self.ct

        self.assertFalse(elastic_db_dump.run_program(self.args,
                                                     self.func_dict))

    @mock.patch("elastic_db_dump.gen_libs.load_module")
    @mock.patch("elastic_db_dump.elastic_class.ElasticSearchDump")
    @mock.patch("elastic_db_dump.gen_class")
    def test_func_call_zero(self, mock_lock, mock_class, mock_load):

        """Function:  test_func_call_zero

        Description:  Test run_program function with zero calls to function.

        Arguments:

        """

        mock_lock.ProgramLock.return_value = ProgramLock([], "FlavorID")
        mock_class.return_value = "Elastic_Class"
        mock_load.return_value = self.ct

        self.assertFalse(elastic_db_dump.run_program(self.args,
                                                     self.func_dict))


if __name__ == "__main__":
    unittest.main()
