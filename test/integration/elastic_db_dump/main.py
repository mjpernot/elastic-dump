# Classification (U)

"""Program:  main.py

    Description:  Integration testing of main in elastic_db_dump.py.

    Usage:
        test/integration/elastic_db_dump/main.py

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
        test_initate_dump_i_option
        test_help_func
        test_arg_require
        test_arg_xor_dict
        test_arg_cond_req_or
        test_arg_dir_chk_crt
        test_create_repo
        test_list_dumps
        test_list_repos
        test_initate_dump

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
        self.phy_repo_dir = os.path.join(self.cfg.phy_repo_dir,
                                         self.cfg.repo_name)
        self.argv_list = [os.path.join(self.base_dir, "main.py"),
                          "-c", "elastic", "-d", self.config_path]
        elr = elastic_class.ElasticSearchRepo(
            self.cfg.host, port=self.cfg.port, user=self.cfg.user,
            japd=self.cfg.japd, ca_cert=self.cfg.ssl_client_ca,
            scheme=self.cfg.scheme)
        elr.connect()

        if elr.repo_dict:
            print("ERROR: Test environment not clean - repositories exist.")
            self.skipTest("Pre-conditions not met.")

        else:
            self.elr = None

    def test_initate_dump_i_option(self):

        """Function:  test_initate_dump_i_option

        Description:  Test initiate dump call -i option.

        Arguments:

        """

        cmdline = gen_libs.get_inst(sys)
        els = elastic_class.ElasticSearchDump(
            self.cfg.host, port=self.cfg.port, user=self.cfg.user,
            japd=self.cfg.japd, ca_cert=self.cfg.ssl_client_ca,
            scheme=self.cfg.scheme)
        els.connect()
        self.argv_list.append("-D")
        self.argv_list.append(self.cfg.repo_name)
        self.argv_list.append("-i")
        self.argv_list.append(
            str([x.split() for x in els.els.cat.indices().splitlines()][0][2]))
        cmdline.argv = self.argv_list
        self.elr = elastic_class.ElasticSearchRepo(
            self.cfg.host, port=self.cfg.port, user=self.cfg.user,
            japd=self.cfg.japd, ca_cert=self.cfg.ssl_client_ca,
            scheme=self.cfg.scheme)
        self.elr.connect()
        _, _ = self.elr.create_repo(
            self.cfg.repo_name, os.path.join(self.cfg.phy_repo_dir,
                                             self.cfg.repo_name))
        elastic_db_dump.main()
        dir_path = os.path.join(self.cfg.phy_repo_dir, self.cfg.repo_name,
                                "indices")

        # Count number of databases/indices dumped to repository.
        cnt = len([name for name in os.listdir(dir_path)
                   if os.path.isdir(os.path.join(dir_path, name))])

        self.assertTrue(cnt >= 1)

    def test_help_func(self):

        """Function:  test_help_func

        Description:  Test help call.

        Arguments:

        """

        cmdline = gen_libs.get_inst(sys)
        self.argv_list.append("-v")
        cmdline.argv = self.argv_list

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.main())

    def test_arg_require(self):

        """Function:  test_arg_require

        Description:  Test arg require call.

        Arguments:

        """

        cmdline = gen_libs.get_inst(sys)
        self.argv_list.remove("-c")
        self.argv_list.remove("elastic")
        cmdline.argv = self.argv_list

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.main())

    def test_arg_xor_dict(self):

        """Function:  test_arg_xor_dict

        Description:  Test arg xor dict call.

        Arguments:

        """

        cmdline = gen_libs.get_inst(sys)
        self.argv_list.append("-L")
        self.argv_list.append("-D")
        cmdline.argv = self.argv_list

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.main())

    def test_arg_cond_req_or(self):

        """Function:  test_arg_cond_req_or

        Description:  Test arg cond req or call.

        Arguments:

        """

        cmdline = gen_libs.get_inst(sys)
        self.argv_list.append("-C")
        self.argv_list.append("TEST_VALUE")
        cmdline.argv = self.argv_list

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.main())

    def test_arg_dir_chk_crt(self):

        """Function:  test_arg_dir_chk_crt

        Description:  Test arg dir chk crt call.

        Arguments:

        """

        cmdline = gen_libs.get_inst(sys)
        self.argv_list.remove(self.config_path)
        self.argv_list.append("TEST_DIR")
        cmdline.argv = self.argv_list

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.main())

    def test_create_repo(self):

        """Function:  test_create_repo

        Description:  Test create repo call.

        Arguments:

        """

        cmdline = gen_libs.get_inst(sys)
        self.argv_list.append("-C")
        self.argv_list.append(self.cfg.repo_name)
        self.argv_list.append("-l")
        self.argv_list.append(self.cfg.phy_repo_dir)
        cmdline.argv = self.argv_list

        elastic_db_dump.main()

        self.elr = elastic_class.ElasticSearchRepo(
            self.cfg.host, self.cfg.port, repo=self.cfg.repo_name,
            user=self.cfg.user, japd=self.cfg.japd,
            ca_cert=self.cfg.ssl_client_ca, scheme=self.cfg.scheme)
        self.elr.connect()

        self.assertTrue(self.cfg.repo_name in self.elr.repo_dict)

    def test_list_dumps(self):

        """Function:  test_list_dumps

        Description:  Test list dumps call.

        Arguments:

        """

        cmdline = gen_libs.get_inst(sys)
        self.argv_list.append("-L")
        self.argv_list.append(self.cfg.repo_name)
        cmdline.argv = self.argv_list
        self.elr = elastic_class.ElasticSearchRepo(
            self.cfg.host, port=self.cfg.port, user=self.cfg.user,
            japd=self.cfg.japd, ca_cert=self.cfg.ssl_client_ca,
            scheme=self.cfg.scheme)
        self.elr.connect()
        _, _ = self.elr.create_repo(
            self.cfg.repo_name, os.path.join(self.cfg.phy_repo_dir,
                                             self.cfg.repo_name))

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.main())

    def test_list_repos(self):

        """Function:  test_list_repos

        Description:  Test list repos call.

        Arguments:

        """

        cmdline = gen_libs.get_inst(sys)
        self.argv_list.append("-R")
        cmdline.argv = self.argv_list
        self.elr = elastic_class.ElasticSearchRepo(
            self.cfg.host, port=self.cfg.port, user=self.cfg.user,
            japd=self.cfg.japd, ca_cert=self.cfg.ssl_client_ca,
            scheme=self.cfg.scheme)
        self.elr.connect()
        _, _ = self.elr.create_repo(
            self.cfg.repo_name, os.path.join(self.cfg.phy_repo_dir,
                                             self.cfg.repo_name))

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.main())

    def test_initate_dump(self):

        """Function:  test_initate_dump

        Description:  Test initiate dump call.

        Arguments:

        """

        cmdline = gen_libs.get_inst(sys)
        self.argv_list.append("-D")
        self.argv_list.append(self.cfg.repo_name)
        cmdline.argv = self.argv_list
        self.elr = elastic_class.ElasticSearchRepo(
            self.cfg.host, port=self.cfg.port, user=self.cfg.user,
            japd=self.cfg.japd, ca_cert=self.cfg.ssl_client_ca,
            scheme=self.cfg.scheme)
        self.elr.connect()
        _, _ = self.elr.create_repo(
            self.cfg.repo_name, os.path.join(self.cfg.phy_repo_dir,
                                             self.cfg.repo_name))
        elastic_db_dump.main()
        els = elastic_class.ElasticSearchDump(
            self.cfg.host, self.cfg.port, repo=self.cfg.repo_name,
            user=self.cfg.user, japd=self.cfg.japd,
            ca_cert=self.cfg.ssl_client_ca, scheme=self.cfg.scheme)
        els.connect()

        self.assertTrue(els.dump_list)

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of integration testing.

        Arguments:

        """

        if self.elr and ("-C" in self.argv_list or "-L" in self.argv_list or
                         "-R" in self.argv_list or "-D" in self.argv_list):

            err_flag, status_msg = self.elr.delete_repo(self.cfg.repo_name)

            if err_flag:
                print("Error: Failed to remove repository '%s'"
                      % self.cfg.repo_name)
                print("Reason: '%s'" % (status_msg))

            if os.path.isdir(self.phy_repo_dir):
                shutil.rmtree(self.phy_repo_dir)


if __name__ == "__main__":
    unittest.main()
