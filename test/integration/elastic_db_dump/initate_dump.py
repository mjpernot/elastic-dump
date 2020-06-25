#!/usr/bin/python
# Classification (U)

"""Program:  initate_dump.py

    Description:  Integration testing of initate_dump in elastic_db_dump.py.

    Usage:
        test/integration/elastic_db_dump/initate_dump.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import shutil

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
        test_i_option_multi_db -> Test database with multiple database names.
        test_i_option_one_db -> Test database with one database name.
        test_i_option_missing_db -> Test database with incorrect database name.
        test_no_i_option -> Test database dump with no -i option.
        test_initate_dump -> Test datbase dump is created.
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
        self.args_array = {}
        self.phy_repo_dir = os.path.join(self.cfg.phy_repo_dir,
                                         self.cfg.repo_name)
        self.elr = elastic_class.ElasticSearchRepo(self.cfg.host,
                                                   self.cfg.port)

        if self.elr.repo_dict:
            print("ERROR: Test environment not clean - repositories exist.")
            self.skipTest("Pre-conditions not met.")

        else:
            _, _ = self.elr.create_repo(
                self.cfg.repo_name, os.path.join(self.cfg.repo_dir,
                                                 self.cfg.repo_name))

            self.els = elastic_class.ElasticSearchDump(
                self.cfg.host, self.cfg.port, repo=self.cfg.repo_name)

    def test_i_option_multi_db(self):

        """Function:  test_i_option_multi_db

        Description:  Test database with multiple database names.

        Arguments:

        """
        # Capture 2 databases/indices name in Elasticsearch.
        dbs = [str(y[2]) for y in [
            x.split() for x in self.els.els.cat.indices().splitlines()]][0:2]

        self.args_array = {"-i": dbs}

        elastic_db_dump.initate_dump(self.els, args_array=self.args_array)

        dir_path = os.path.join(self.cfg.phy_repo_dir, self.cfg.repo_name,
                                "indices")

        # Count number of databases/indices dumped to repository.
        cnt = len([name for name in os.listdir(dir_path)
                   if os.path.isdir(os.path.join(dir_path, name))])

        self.assertEqual(cnt, 2)

    def test_i_option_one_db(self):

        """Function:  test_i_option_one_db

        Description:  Test database with one database name.

        Arguments:

        """

        # Capture the first database/indice name in Elasticsearch.
        dbs = [str([x.split()
                    for x in self.els.els.cat.indices().splitlines()][0][2])]

        self.args_array = {"-i": dbs}

        elastic_db_dump.initate_dump(self.els, args_array=self.args_array)

        dir_path = os.path.join(self.cfg.phy_repo_dir, self.cfg.repo_name,
                                "indices")

        # Count number of databases/indices dumped to repository.
        cnt = len([name for name in os.listdir(dir_path)
                   if os.path.isdir(os.path.join(dir_path, name))])

        self.assertEqual(cnt, 1)

    def test_i_option_missing_db(self):

        """Function:  test_i_option_missing_db

        Description:  Test database with incorrect database name.

        Arguments:

        """

        self.args_array = {"-i": ["Incorrect_Database_Name"]}

        elastic_db_dump.initate_dump(self.els, args_array=self.args_array)

        # If index dump directory exists, then test is a failure.
        if os.path.isdir(os.path.join(self.cfg.repo_dir, "indices")):
            status = False

        else:
            status = True

        self.assertTrue(status)

    def test_no_i_option(self):

        """Function:  test_no_i_option

        Description:  Test database dump with no -i option.

        Arguments:

        """

        elastic_db_dump.initate_dump(self.els, args_array=self.args_array)

        if self.els.dump_list:
            status = True

        else:
            status = False

        self.assertTrue(status)

    def test_initate_dump(self):

        """Function:  test_initate_dump

        Description:  Test datbase dump is created.

        Arguments:

        """

        elastic_db_dump.initate_dump(self.els, args_array=self.args_array)

        if self.els.dump_list:
            status = True

        else:
            status = False

        self.assertTrue(status)

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
            shutil.rmtree(self.phy_repo_dir)


if __name__ == "__main__":
    unittest.main()
