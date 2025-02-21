# Classification (U)

"""Program:  initate_dump.py

    Description:  Integration testing of initate_dump in elastic_db_dump.py.

    Usage:
        test/integration/elastic_db_dump/initate_dump.py

    Arguments:

"""

# Libraries and Global Variables
from __future__ import print_function

# Standard
import sys
import os
import shutil
import unittest

# Local
sys.path.append(os.getcwd())
import elastic_db_dump                          # pylint:disable=E0401,C0413
import lib.gen_libs as gen_libs             # pylint:disable=E0401,C0413,R0402
import elastic_lib.elastic_class as ecls    # pylint:disable=E0401,C0413,R0402
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class ArgParser():

    """Class:  ArgParser

    Description:  Class stub holder for gen_class.ArgParser class.

    Methods:
        __init__
        arg_exist
        get_val

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.args_array = {}

    def arg_exist(self, arg):

        """Method:  arg_exist

        Description:  Method stub holder for gen_class.ArgParser.arg_exist.

        Arguments:

        """

        return arg in self.args_array

    def get_val(self, skey, def_val=None):

        """Method:  get_val

        Description:  Method stub holder for gen_class.ArgParser.get_val.

        Arguments:

        """

        return self.args_array.get(skey, def_val)


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_i_option_multi_db
        test_i_option_one_db
        test_i_option_missing_db
        test_no_i_option
        test_initate_dump
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
        self.args = ArgParser()
        self.phy_repo_dir = os.path.join(self.cfg.phy_repo_dir,
                                         self.cfg.repo_name)
        self.elr = ecls.ElasticSearchRepo(
            self.cfg.host, port=self.cfg.port, user=self.cfg.user,
            japd=self.cfg.japd, ca_cert=self.cfg.ssl_client_ca,
            scheme=self.cfg.scheme)
        self.elr.connect()

        if self.elr.repo_dict:
            print("ERROR: Test environment not clean - repositories exist.")
            self.skipTest("Pre-conditions not met.")

        else:
            _, _ = self.elr.create_repo(
                self.cfg.repo_name, os.path.join(self.cfg.phy_repo_dir,
                                                 self.cfg.repo_name))

            self.els = ecls.ElasticSearchDump(
                self.cfg.host, port=self.cfg.port, repo=self.cfg.repo_name,
                user=self.cfg.user, japd=self.cfg.japd,
                ca_cert=self.cfg.ssl_client_ca, scheme=self.cfg.scheme)
            self.els.connect()

    def test_i_option_multi_db(self):

        """Function:  test_i_option_multi_db

        Description:  Test database with multiple database names.

        Arguments:

        """
        # Capture 2 databases/indices name in Elasticsearch.
        dbs = [str(y[2]) for y in [
            x.split() for x in self.els.els.cat.indices().splitlines()]][0:2]

        self.args.args_array = {"-i": dbs}

        elastic_db_dump.initate_dump(self.els, args=self.args)

        dir_path = os.path.join(
            self.cfg.phy_repo_dir, self.cfg.repo_name, "indices")

        # Count number of databases/indices dumped to repository.
        cnt = len([name for name in os.listdir(dir_path)
                   if os.path.isdir(os.path.join(dir_path, name))])

        self.assertTrue(cnt >= 2)

    def test_i_option_one_db(self):

        """Function:  test_i_option_one_db

        Description:  Test database with one database name.

        Arguments:

        """

        # Capture the first database/indice name in Elasticsearch.
        dbs = [str([x.split()
                    for x in self.els.els.cat.indices().splitlines()][0][2])]

        self.args.args_array = {"-i": dbs}

        elastic_db_dump.initate_dump(self.els, args=self.args)

        dir_path = os.path.join(
            self.cfg.phy_repo_dir, self.cfg.repo_name, "indices")

        # Count number of databases/indices dumped to repository.
        cnt = len([name for name in os.listdir(dir_path)
                   if os.path.isdir(os.path.join(dir_path, name))])

        self.assertTrue(cnt >= 1)

    def test_i_option_missing_db(self):

        """Function:  test_i_option_missing_db

        Description:  Test database with incorrect database name.

        Arguments:

        """

        self.args.args_array = {"-i": ["Incorrect_Database_Name"]}

        elastic_db_dump.initate_dump(self.els, args=self.args)

        # If index dump directory exists, then test is a failure.
        self.assertFalse(
            os.path.isdir(os.path.join(self.cfg.phy_repo_dir, "indices")))

    def test_no_i_option(self):

        """Function:  test_no_i_option

        Description:  Test database dump with no -i option.

        Arguments:

        """

        elastic_db_dump.initate_dump(self.els, args=self.args)

        self.assertTrue(self.els.dump_list)

    def test_initate_dump(self):

        """Function:  test_initate_dump

        Description:  Test datbase dump is created.

        Arguments:

        """

        elastic_db_dump.initate_dump(self.els, args=self.args)

        self.assertTrue(self.els.dump_list)

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of integration testing.

        Arguments:

        """

        err_flag, status_msg = self.elr.delete_repo(self.cfg.repo_name)

        if err_flag:
            print(f"Error: Failed to remove repository {self.cfg.repo_name}")
            print(f"Reason: {status_msg}")

        if os.path.isdir(self.phy_repo_dir):
            shutil.rmtree(self.phy_repo_dir)


if __name__ == "__main__":
    unittest.main()
