#!/usr/bin/python
# Classification (U)

"""Program:  run_program.py

    Description:  Integration testing of run_program in elastic_db_dump.py.

    Usage:
        test/integration/elastic_db_dump/run_program.py

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
        setUp -> Unit testing initilization.
        test_initate_dump_i_option -> Test initiate dump call -i option.
        test_load_module -> Test load module call.
        test_create_repo -> Test create repo call.
        test_list_dumps -> Test list dumps call.
        test_list_repos -> Test list repos call.
        test_initate_dump -> Test initate dump call.

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

        self.func_dict = {"-C": elastic_db_dump.create_repo,
                          "-D": elastic_db_dump.initate_dump,
                          "-L": elastic_db_dump.list_dumps,
                          "-R": elastic_db_dump.list_repos}
        self.args = {"-c": "elastic", "-d": self.config_path}

        ER = elastic_class.ElasticSearchRepo(self.cfg.host, self.cfg.port)

        if ER.repo_dict:
            print("ERROR: Test environment not clean - repositories exist.")
            self.skipTest("Pre-conditions not met.")

        else:
            self.ER = None

    def test_initate_dump_i_option(self):

        """Function:  test_initate_dump_i_option

        Description:  Test initiate dump call -i option.

        Arguments:

        """

        ES = elastic_class.ElasticSearchDump(self.cfg.host, self.cfg.port)

        # Capture the first database/indice name in Elasticsearch.
        dbs = [str([x.split()
                    for x in ES.es.cat.indices().splitlines()][0][2])]

        self.args["-D"] = self.cfg.repo_name
        self.args["-i"] = dbs

        self.ER = elastic_class.ElasticSearchRepo(self.cfg.host, self.cfg.port)

        status, msg = self.ER.create_repo(self.cfg.repo_name,
                                          self.cfg.repo_dir)

        elastic_db_dump.run_program(self.args, self.func_dict)

        ES = elastic_class.ElasticSearchDump(self.cfg.host, self.cfg.port,
                                             repo=self.cfg.repo_name)

        dir_path = os.path.join(self.cfg.repo_dir, "indices")

        # Count number of databases/indices dumped to repository.
        cnt = len([name for name in os.listdir(dir_path)
                   if os.path.isdir(os.path.join(dir_path, name))])
        
        self.assertEqual(cnt, 1)

    @mock.patch("elastic_db_dump.gen_class")
    def test_load_module(self, mock_lock):

        """Function:  test_load_module

        Description:  Test load module call.

        Arguments:

        """

        mock_lock.ProgramLock.side_effect = \
            elastic_db_dump.gen_class.SingleInstanceException()

        self.assertFalse(elastic_db_dump.run_program(self.args,
                                                     self.func_dict))

    def test_create_repo(self):

        """Function:  test_create_repo

        Description:  Test create repo call.

        Arguments:

        """

        self.args["-C"] = self.cfg.repo_name
        self.args["-l"] = self.cfg.repo_dir

        elastic_db_dump.run_program(self.args, self.func_dict)

        self.ER = elastic_class.ElasticSearchRepo(self.cfg.host, self.cfg.port,
                                                  repo=self.cfg.repo_name)

        if self.cfg.repo_name in self.ER.repo_dict:
            status = True

        else:
            status = False

        self.assertTrue(status)

    def test_list_dumps(self):

        """Function:  test_list_dumps

        Description:  Test list dumps call.

        Arguments:

        """

        self.args["-L"] = self.cfg.repo_name

        self.ER = elastic_class.ElasticSearchRepo(self.cfg.host, self.cfg.port)

        status, msg = self.ER.create_repo(self.cfg.repo_name,
                                          self.cfg.repo_dir)

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.run_program(self.args,
                                                         self.func_dict))

    def test_list_repos(self):

        """Function:  test_list_repos

        Description:  Test list repos call.

        Arguments:

        """

        self.args["-R"] = True

        self.ER = elastic_class.ElasticSearchRepo(self.cfg.host, self.cfg.port)

        status, msg = self.ER.create_repo(self.cfg.repo_name,
                                          self.cfg.repo_dir)

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.run_program(self.args,
                                                         self.func_dict))

    def test_initate_dump(self):

        """Function:  test_initate_dump

        Description:  Test initiate dump call.

        Arguments:

        """

        self.args["-D"] = self.cfg.repo_name

        self.ER = elastic_class.ElasticSearchRepo(self.cfg.host, self.cfg.port)

        status, msg = self.ER.create_repo(self.cfg.repo_name,
                                          self.cfg.repo_dir)

        elastic_db_dump.run_program(self.args, self.func_dict)

        ES = elastic_class.ElasticSearchDump(self.cfg.host, self.cfg.port,
                                             repo=self.cfg.repo_name)

        if ES.dump_list:
            status = True

        else:
            status = False

        self.assertTrue(status)

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of integration testing.

        Arguments:

        """

        if "-C" in self.args or "-L" in self.args or "-R" in self.args:
            err_flag, status_msg = self.ER.delete_repo(self.cfg.repo_name)

            if err_flag:
                print("Error: Failed to remove repository '%s'"
                      % self.cfg.repo_name)
                print("Reason: '%s'" % (status_msg))

            if os.path.isdir(self.cfg.repo_dir):
                os.rmdir(self.cfg.repo_dir)

        elif "-D" in self.args:
            err_flag, status_msg = self.ER.delete_repo(self.cfg.repo_name)

            if err_flag:
                print("Error: Failed to remove repository '%s'"
                      % self.cfg.repo_name)
                print("Reason: '%s'" % (status_msg))

            if os.path.isdir(self.cfg.repo_dir):
                shutil.rmtree(self.cfg.repo_dir)


if __name__ == "__main__":
    unittest.main()
