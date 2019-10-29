#!/usr/bin/python
# Classification (U)

"""Program:  list_dumps.py

    Description:  Integration testing of list_dumps in elastic_db_dump.py.

    Usage:
        test/integration/elastic_db_dump/list_dumps.py

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

# Local
sys.path.append(os.getcwd())
import elastic_db_dump
import lib.gen_libs as gen_libs
import elastic_lib.elastic_class as elastic_class
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Unit testing initilization.
        test_list_dumps -> Test listing of dumps.
        tearDown -> Clean up of integration testing.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.base_dir = "test/integration/elastic_db_dump"
        self.test_path = os.path.join(os.getcwd(), self.base_dir)
        self.config_path = os.path.join(self.test_path, "config")
        self.cfg = gen_libs.load_module("elastic", self.config_path)

        self.ER = elastic_class.ElasticSearchRepo(self.cfg.host, self.cfg.port)

        if self.ER.repo_dict:
            print("ERROR: Test environment not clean - repositories exist.")
            self.skipTest("Pre-conditions not met.")

        else:
            _, _ = self.ER.create_repo(self.cfg.repo_name, self.cfg.repo_dir)

            self.ES = elastic_class.ElasticSearchDump(self.cfg.host,
                                                      self.cfg.port,
                                                      repo=self.cfg.repo_name)

    def test_list_dumps(self):

        """Function:  test_list_dumps

        Description:  Test listing of dumps.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.list_dumps(self.ES))

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of integration testing.

        Arguments:

        """

        err_flag, status_msg = self.ER.delete_repo(self.cfg.repo_name)

        if err_flag:
            print("Error: Failed to remove repository '%s'"
                  % self.cfg.repo_name)
            print("Reason: '%s'" % (status_msg))

        if os.path.isdir(self.cfg.repo_dir):
            os.rmdir(self.cfg.repo_dir)


if __name__ == "__main__":
    unittest.main()
