# Classification (U)

"""Program:  print_failures.py

    Description:  Unit testing of initate_dump in elastic_db_dump.py.

    Usage:
        test/unit/elastic_db_dump/initate_dump.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest
import mock

# Local
sys.path.append(os.getcwd())
import elastic_db_dump
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_with_option
        test_no_i_option
        test_err_flag_true
        test_err_flag_false
        test_dump_status_success
        test_dump_status_unknown
        test_dump_status_incomp
        test_dump_status_partial
        test_dump_status_failed

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        class ElasticSearchDump(object):

            """Class:  ElasticSearchDump

            Description:  Class representation of the ElasticSearchDump class.

            Methods:
                __init__
                dump_db

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the class.

                Arguments:

                """

                self.repo_name = "Test_Repo_Name"
                self.cluster_name = "Test_Cluster_Name"
                self.dump_status = "SUCCESS"
                self.dbs = None

            def dump_db(self, **kwargs):

                """Method:  dump_db

                Description:  Simulates dumping a Elasticssearch database.

                Arguments:

                """

                err_flag = False
                status_msg = None
                self.dbs = kwargs.get("dbs")

                if not self.repo_name:
                    status_msg = "ERROR:  Repository name not set."
                    err_flag = True

                return err_flag, status_msg

        self.els = ElasticSearchDump()
        self.args_array = {}

    def test_with_option(self):

        """Function:  test_with_option

        Description:  Test with -i option in args_array.

        Arguments:

        """

        self.args_array = {"-i": ["Index1", "Index2"]}

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.initate_dump(
                self.els, args_array=self.args_array))

    def test_no_i_option(self):

        """Function:  test_no_i_option

        Description:  Test with no -i option in args_array.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.initate_dump(
                self.els, args_array=self.args_array))

    def test_err_flag_true(self):

        """Function:  test_err_flag_true

        Description:  Test error flag set to True.

        Arguments:

        """

        self.els.repo_name = None

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.initate_dump(
                self.els, args_array=self.args_array))

    def test_err_flag_false(self):

        """Function:  test_err_flag_false

        Description:  Test error flag set to False.

        Arguments:

        """

        self.assertFalse(elastic_db_dump.initate_dump(
            self.els, args_array=self.args_array))

    def test_dump_status_success(self):

        """Function:  test_dump_status_success

        Description:  Test dump status set to success.

        Arguments:

        """

        self.assertFalse(elastic_db_dump.initate_dump(
            self.els, args_array=self.args_array))

    def test_dump_status_unknown(self):

        """Function:  test_dump_status_unknown

        Description:  Test dump status set to unknown.

        Arguments:

        """

        self.els.dump_status = "unknown"

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.initate_dump(
                self.els, args_array=self.args_array))

    def test_dump_status_incomp(self):

        """Function:  test_dump_status_incomp

        Description:  Test dump status set to incompatible.

        Arguments:

        """

        self.els.dump_status = "INCOMPATIBLE"

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.initate_dump(
                self.els, args_array=self.args_array))

    @mock.patch("elastic_db_dump.print_failures")
    def test_dump_status_partial(self, mock_print):

        """Function:  test_dump_status_partial

        Description:  Test dump status set to partial.

        Arguments:

        """

        mock_print.return_value = True

        self.els.dump_status = "PARTIAL"

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.initate_dump(
                self.els, args_array=self.args_array))

    def test_dump_status_failed(self):

        """Function:  test_dump_status_failed

        Description:  Test dump status set to failed.

        Arguments:

        """

        self.els.dump_status = "FAILED"

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.initate_dump(
                self.els, args_array=self.args_array))


if __name__ == "__main__":
    unittest.main()
