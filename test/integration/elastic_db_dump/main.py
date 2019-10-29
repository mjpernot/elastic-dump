#!/usr/bin/python
# Classification (U)

"""Program:  main.py

    Description:  Integration testing of main in elastic_db_dump.py.

    Usage:
        test/integration/elastic_db_dump/main.py

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
        test_initate_dump_i_option -> Test initiate dump call -i option.
        test_help_func -> Test help call.
        test_arg_require -> Test arg require call.
        test_arg_xor_dict -> Test arg xor dict call.
        test_arg_cond_req_or -> Test arg cond req or call.
        test_arg_dir_chk_crt -> Test arg dir chk crt call.
        test_create_repo -> Test create repo call.
        test_list_dumps -> Test list dumps call.
        test_list_repos -> Test list repos call.
        test_initate_dump -> Test initiate dump call.

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

        self.argv_list = [os.path.join(self.base_dir, "main.py"),
                          "-c", "elastic", "-d", self.config_path]

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

        self.argv_list.append("-D")
        self.argv_list.append(self.cfg.repo_name)
        self.argv_list.append("-i")
        self.argv_list.append(str([x.split()
            for x in ES.es.cat.indices().splitlines()][0][2]))
        sys.argv = self.argv_list

        self.ER = elastic_class.ElasticSearchRepo(self.cfg.host, self.cfg.port)

        status, msg = self.ER.create_repo(self.cfg.repo_name,
                                          self.cfg.repo_dir)

        elastic_db_dump.main()

        ES = elastic_class.ElasticSearchDump(self.cfg.host, self.cfg.port,
                                             repo=self.cfg.repo_name)

        dir_path = os.path.join(self.cfg.repo_dir, "indices")

        # Count number of databases/indices dumped to repository.
        cnt = len([name for name in os.listdir(dir_path)
                   if os.path.isdir(os.path.join(dir_path, name))])
        
        self.assertEqual(cnt, 1)

    def test_help_func(self):

        """Function:  test_help_func

        Description:  Test help call.

        Arguments:

        """

        self.argv_list.append("-v")
        sys.argv = self.argv_list

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.main())

    def test_arg_require(self):

        """Function:  test_arg_require

        Description:  Test arg require call.

        Arguments:

        """

        self.argv_list.remove("-c")
        self.argv_list.remove("elastic")
        sys.argv = self.argv_list

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.main())

    def test_arg_xor_dict(self):

        """Function:  test_arg_xor_dict

        Description:  Test arg xor dict call.

        Arguments:

        """

        self.argv_list.append("-L")
        self.argv_list.append("-D")
        sys.argv = self.argv_list

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.main())

    def test_arg_cond_req_or(self):

        """Function:  test_arg_cond_req_or

        Description:  Test arg cond req or call.

        Arguments:

        """

        self.argv_list.append("-C")
        self.argv_list.append("TEST_VALUE")
        sys.argv = self.argv_list

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.main())

    def test_arg_dir_chk_crt(self):

        """Function:  test_arg_dir_chk_crt

        Description:  Test arg dir chk crt call.

        Arguments:

        """
        self.argv_list.remove(self.config_path)
        self.argv_list.append("TEST_DIR")
        sys.argv = self.argv_list

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.main())

    def test_create_repo(self):

        """Function:  test_create_repo

        Description:  Test create repo call.

        Arguments:

        """

        self.argv_list.append("-C")
        self.argv_list.append(self.cfg.repo_name)
        self.argv_list.append("-l")
        self.argv_list.append(self.cfg.repo_dir)
        sys.argv = self.argv_list

        elastic_db_dump.main()

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

        self.argv_list.append("-L")
        self.argv_list.append(self.cfg.repo_name)
        sys.argv = self.argv_list

        self.ER = elastic_class.ElasticSearchRepo(self.cfg.host, self.cfg.port)

        status, msg = self.ER.create_repo(self.cfg.repo_name,
                                          self.cfg.repo_dir)

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.main())

    def test_list_repos(self):

        """Function:  test_list_repos

        Description:  Test list repos call.

        Arguments:

        """

        self.argv_list.append("-R")
        sys.argv = self.argv_list

        self.ER = elastic_class.ElasticSearchRepo(self.cfg.host, self.cfg.port)

        status, msg = self.ER.create_repo(self.cfg.repo_name,
                                          self.cfg.repo_dir)

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.main())

    def test_initate_dump(self):

        """Function:  test_initate_dump

        Description:  Test initiate dump call.

        Arguments:

        """

        self.argv_list.append("-D")
        self.argv_list.append(self.cfg.repo_name)
        sys.argv = self.argv_list

        self.ER = elastic_class.ElasticSearchRepo(self.cfg.host, self.cfg.port)

        status, msg = self.ER.create_repo(self.cfg.repo_name,
                                          self.cfg.repo_dir)

        elastic_db_dump.main()

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

        if self.ER and ("-C" in self.argv_list or "-L" in self.argv_list or
                        "-R" in self.argv_list):

            err_flag, status_msg = self.ER.delete_repo(self.cfg.repo_name)

            if err_flag:
                print("Error: Failed to remove repository '%s'"
                      % self.cfg.repo_name)
                print("Reason: '%s'" % (status_msg))

            if os.path.isdir(self.cfg.repo_dir):
                os.rmdir(self.cfg.repo_dir)

        elif self.ER and "-D" in self.argv_list:

            err_flag, status_msg = self.ER.delete_repo(self.cfg.repo_name)

            if err_flag:
                print("Error: Failed to remove repository '%s'"
                      % self.cfg.repo_name)
                print("Reason: '%s'" % (status_msg))

            if os.path.isdir(self.cfg.repo_dir):
                shutil.rmtree(self.cfg.repo_dir)


if __name__ == "__main__":
    unittest.main()
