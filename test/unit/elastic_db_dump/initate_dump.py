#!/usr/bin/python
# Classification (U)

"""Program:  print_failures.py

    Description:  Unit testing of initate_dump in elastic_db_dump.py.

    Usage:
        test/unit/elastic_db_dump/initate_dump.py

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


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Super-Class:  unittest.TestCase

    Sub-Classes:  None

    Methods:
        setUp -> Unit testing initilization.
        test_with_option -> Test with -i option in args_array.
        test_no_i_option -> Test with no -i option in args_array.
        test_err_flag_true -> Test error flag set to True.
        test_err_flag_false -> Test error flag set to False.
        test_dump_status_success -> Test dump status set to success.
        test_dump_status_unknown -> Test dump status set to unknown.
        test_dump_status_incomp -> Test dump status set to incompatible.
        test_dump_status_partial -> Test dump status set to partial.
        test_dump_status_failed -> Test dump status set to failed.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:
            None

        """

        class ElasticSearchDump(object):

            """Class:  ElasticSearchDump

            Description:  Class representation of the ElasticSearchDump class.

            Super-Class:  object

            Sub-Classes:  None

            Methods:
                __init__ -> Initialize configuration environment.
                dump_db -> Simulates dumping a Elasticssearch database.

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the class.

                Arguments:
                        None

                """

                self.repo_name = "Test_Repo_Name"
                self.cluster_name = "Test_Cluster_Name"
                self.dump_status = "SUCCESS"

            def dump_db(self, **kwargs):

                """Method:  dump_db

                Description:  Simulates dumping a Elasticssearch database.

                Arguments:
                    (input)  **kwargs:
                        None
                    (output) err_flag True|False -> Has errors been detected.
                    (output) status_msg -> Return dump status or error message.

                """

                err_flag = False
                status_msg = None

                if not self.repo_name:
                    status_msg = "ERROR:  Repository name not set."
                    err_flag = True

                return err_flag, status_msg

        self.ES = ElasticSearchDump()
        self.args_array = {}

    def test_with_option(self):

        """Function:  test_with_option

        Description:  Test with -i option in args_array.

        Arguments:
            None

        """

        self.args_array = {"-i": ["Index1", "Index2"]}

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.initate_dump(self.ES,
                args_array=self.args_array))

    def test_no_i_option(self):

        """Function:  test_no_i_option

        Description:  Test with no -i option in args_array.

        Arguments:
            None

        """

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.initate_dump(self.ES,
                args_array=self.args_array))

    def test_err_flag_true(self):

        """Function:  test_err_flag_true

        Description:  Test error flag set to True.

        Arguments:
            None

        """

        self.ES.repo_name = None

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.initate_dump(self.ES,
                args_array=self.args_array))

    def test_err_flag_false(self):

        """Function:  test_err_flag_false

        Description:  Test error flag set to False.

        Arguments:
            None

        """

        self.assertFalse(elastic_db_dump.initate_dump(self.ES,
                args_array=self.args_array))

    def test_dump_status_success(self):

        """Function:  test_dump_status_success

        Description:  Test dump status set to success.

        Arguments:
            None

        """

        self.assertFalse(elastic_db_dump.initate_dump(self.ES,
                args_array=self.args_array))

    def test_dump_status_unknown(self):

        """Function:  test_dump_status_unknown

        Description:  Test dump status set to unknown.

        Arguments:
            None

        """

        self.ES.dump_status = "unknown"

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.initate_dump(self.ES,
                args_array=self.args_array))

    def test_dump_status_incomp(self):

        """Function:  test_dump_status_incomp

        Description:  Test dump status set to incompatible.

        Arguments:
            None

        """

        self.ES.dump_status = "INCOMPATIBLE"

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.initate_dump(self.ES,
                args_array=self.args_array))

    @mock.patch("elastic_db_dump.print_failures")
    def test_dump_status_partial(self, mock_print):

        """Function:  test_dump_status_partial

        Description:  Test dump status set to partial.

        Arguments:
            mock_print -> Mock Ref:  elastic_db_dump.print_failures

        """

        mock_print.return_value = True

        self.ES.dump_status = "PARTIAL"

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.initate_dump(self.ES,
                args_array=self.args_array))

    def test_dump_status_failed(self):

        """Function:  test_dump_status_failed

        Description:  Test dump status set to failed.

        Arguments:
            None

        """

        self.ES.dump_status = "FAILED"

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.initate_dump(self.ES,
                args_array=self.args_array))


if __name__ == "__main__":
    unittest.main()
