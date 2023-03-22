# Classification (U)

"""Program:  run_program.py

    Description:  Integration testing of run_program in elastic_db_dump.py.

    Usage:
        test/integration/elastic_db_dump/run_program.py

    Arguments:

"""

# Libraries and Global Variables
from __future__ import print_function

# Standard
import sys
import os
import shutil
import unittest
import mock

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
        test_load_module
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
        self.func_names = {
            "-C": elastic_db_dump.create_repo,
            "-D": elastic_db_dump.initate_dump,
            "-L": elastic_db_dump.list_dumps,
            "-R": elastic_db_dump.list_repos}
        self.args = {"-c": "elastic", "-d": self.config_path}

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

        els = elastic_class.ElasticSearchDump(
            self.cfg.host, port=self.cfg.port, user=self.cfg.user,
            japd=self.cfg.japd, ca_cert=self.cfg.ssl_client_ca,
            scheme=self.cfg.scheme)
        els.connect()

        # Capture the first database/indice name in Elasticsearch.
        dbs = [str([x.split()
                    for x in els.els.cat.indices().splitlines()][0][2])]
        self.args["-D"] = self.cfg.repo_name
        self.args["-i"] = dbs
        self.elr = elastic_class.ElasticSearchRepo(
            self.cfg.host, port=self.cfg.port, user=self.cfg.user,
            japd=self.cfg.japd, ca_cert=self.cfg.ssl_client_ca,
            scheme=self.cfg.scheme)
        self.elr.connect()
        _, _ = self.elr.create_repo(
            self.cfg.repo_name, os.path.join(self.cfg.phy_repo_dir,
                                             self.cfg.repo_name))
        elastic_db_dump.run_program(self.args, self.func_names)
        dir_path = os.path.join(self.cfg.phy_repo_dir, self.cfg.repo_name,
                                "indices")

        # Count number of databases/indices dumped to repository.
        cnt = len([name for name in os.listdir(dir_path)
                   if os.path.isdir(os.path.join(dir_path, name))])

        self.assertTrue(cnt >= 1)

    @mock.patch("elastic_db_dump.gen_class")
    def test_load_module(self, mock_lock):

        """Function:  test_load_module

        Description:  Test load module call.

        Arguments:

        """

        mock_lock.ProgramLock.side_effect = \
            elastic_db_dump.gen_class.SingleInstanceException()

        self.assertFalse(elastic_db_dump.run_program(self.args,
                                                     self.func_names))

    def test_create_repo(self):

        """Function:  test_create_repo

        Description:  Test create repo call.

        Arguments:

        """

        self.args["-C"] = self.cfg.repo_name
        self.args["-l"] = self.cfg.phy_repo_dir
        elastic_db_dump.run_program(self.args, self.func_names)
        self.elr = elastic_class.ElasticSearchRepo(
            self.cfg.host, port=self.cfg.port, repo=self.cfg.repo_name,
            user=self.cfg.user, japd=self.cfg.japd,
            ca_cert=self.cfg.ssl_client_ca, scheme=self.cfg.scheme)
        self.elr.connect()

        self.assertTrue(self.cfg.repo_name in self.elr.repo_dict)

    def test_list_dumps(self):

        """Function:  test_list_dumps

        Description:  Test list dumps call.

        Arguments:

        """

        self.args["-L"] = self.cfg.repo_name
        self.elr = elastic_class.ElasticSearchRepo(
            self.cfg.host, port=self.cfg.port, user=self.cfg.user,
            japd=self.cfg.japd, ca_cert=self.cfg.ssl_client_ca,
            scheme=self.cfg.scheme)
        self.elr.connect()
        _, _ = self.elr.create_repo(
            self.cfg.repo_name, os.path.join(self.cfg.phy_repo_dir,
                                             self.cfg.repo_name))

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.run_program(self.args,
                                                         self.func_names))

    def test_list_repos(self):

        """Function:  test_list_repos

        Description:  Test list repos call.

        Arguments:

        """

        self.args["-R"] = True
        self.elr = elastic_class.ElasticSearchRepo(
            self.cfg.host, port=self.cfg.port, user=self.cfg.user,
            japd=self.cfg.japd, ca_cert=self.cfg.ssl_client_ca,
            scheme=self.cfg.scheme)
        self.elr.connect()
        _, _ = self.elr.create_repo(
            self.cfg.repo_name, os.path.join(self.cfg.phy_repo_dir,
                                             self.cfg.repo_name))

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.run_program(self.args,
                                                         self.func_names))

    def test_initate_dump(self):

        """Function:  test_initate_dump

        Description:  Test initiate dump call.

        Arguments:

        """

        self.args["-D"] = self.cfg.repo_name
        self.elr = elastic_class.ElasticSearchRepo(
            self.cfg.host, port=self.cfg.port, user=self.cfg.user,
            japd=self.cfg.japd, ca_cert=self.cfg.ssl_client_ca,
            scheme=self.cfg.scheme)
        self.elr.connect()
        _, _ = self.elr.create_repo(
            self.cfg.repo_name, os.path.join(self.cfg.phy_repo_dir,
                                             self.cfg.repo_name))
        elastic_db_dump.run_program(self.args, self.func_names)
        els = elastic_class.ElasticSearchDump(
            self.cfg.host, port=self.cfg.port, repo=self.cfg.repo_name,
            user=self.cfg.user, japd=self.cfg.japd,
            ca_cert=self.cfg.ssl_client_ca, scheme=self.cfg.scheme)
        els.connect()

        self.assertTrue(els.dump_list)

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of integration testing.

        Arguments:

        """

        if "-C" in self.args or "-L" in self.args or "-R" in self.args \
           or "-D" in self.args:
            err_flag, status_msg = self.elr.delete_repo(self.cfg.repo_name)

            if err_flag:
                print("Error: Failed to remove repository '%s'"
                      % self.cfg.repo_name)
                print("Reason: '%s'" % (status_msg))

            if os.path.isdir(self.phy_repo_dir):
                shutil.rmtree(self.phy_repo_dir)


if __name__ == "__main__":
    unittest.main()
