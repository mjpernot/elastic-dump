# Classification (U)

"""Program:  list_dumps.py

    Description:  Integration testing of list_dumps in elastic_db_dump.py.

    Usage:
        test/integration/elastic_db_dump/list_dumps.py

    Arguments:

"""

# Libraries and Global Variables
from __future__ import print_function

# Standard
import sys
import os
import unittest

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
        setUp
        test_list_dumps
        tearDown

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
        self.phy_repo_dir = os.path.join(
            self.cfg.phy_repo_dir, self.cfg.repo_name)
        self.elr = elastic_class.ElasticSearchRepo(
            self.cfg.host, port=self.cfg.port, user=self.cfg.user,
            japd=self.cfg.japd, ca_cert=self.cfg.ssl_client_ca,
            scheme=self.cfg.scheme)
        self.elr.connect()

        if self.elr.repo_dict:
            print("ERROR: Test environment not clean - repositories exist.")
            self.skipTest("Pre-conditions not met.")

        else:
            _, _ = self.elr.create_repo(
                self.cfg.repo_name, os.path.join(
                    self.cfg.phy_repo_dir, self.cfg.repo_name))

            self.els = elastic_class.ElasticSearchDump(
                self.cfg.host, port=self.cfg.port, repo=self.cfg.repo_name,
                user=self.cfg.user, japd=self.cfg.japd,
                ca_cert=self.cfg.ssl_client_ca, scheme=self.cfg.scheme)
            self.els.connect()

    def test_list_dumps(self):

        """Function:  test_list_dumps

        Description:  Test listing of dumps.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.list_dumps(self.els))

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of integration testing.

        Arguments:

        """

        err_flag, status_msg = self.elr.delete_repo(self.cfg.repo_name)

        if err_flag:
            print("Error: Failed to remove repository '%s'"
                  % self.cfg.repo_name)
            print("Reason: '%s'" % (status_msg))

        if os.path.isdir(self.phy_repo_dir):
            os.rmdir(self.phy_repo_dir)


if __name__ == "__main__":
    unittest.main()
