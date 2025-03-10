# Classification (U)

"""Program:  create_repo.py

    Description:  Integration testing of create_repo in elastic_db_dump.py.

    Usage:
        test/integration/elastic_db_dump/create_repo.py

    Arguments:

"""

# Libraries and Global Variables

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


class ArgParser():                                      # pylint:disable=R0903

    """Class:  ArgParser

    Description:  Class stub holder for gen_class.ArgParser class.

    Methods:
        __init__
        get_val

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.args_array = {}

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
        test_repo_init
        test_repo_create
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
        self.args.args_array = {
            "-C": self.cfg.repo_name, "-l": self.cfg.phy_repo_dir}
        self.phy_repo_dir = os.path.join(
            self.cfg.phy_repo_dir, self.cfg.repo_name)
        self.els = ecls.ElasticSearchDump(
            self.cfg.host, port=self.cfg.port, user=self.cfg.user,
            japd=self.cfg.japd, ca_cert=self.cfg.ssl_client_ca,
            scheme=self.cfg.scheme)
        self.els.connect()

        elr = ecls.ElasticSearchRepo(
            self.cfg.host, port=self.cfg.port, user=self.cfg.user,
            japd=self.cfg.japd, ca_cert=self.cfg.ssl_client_ca,
            scheme=self.cfg.scheme)
        elr.connect()

        if elr.repo_dict:
            print("ERROR: Test environment not clean - repositories exist.")
            self.skipTest("Pre-conditions not met.")

        else:
            self.elr = None

    def test_repo_init(self):

        """Function:  test_repo_init

        Description:  Test initialization of Elasticsearch class.

        Arguments:

        """

        self.elr = ecls.ElasticSearchRepo(
            self.cfg.host, port=self.cfg.port, user=self.cfg.user,
            japd=self.cfg.japd, ca_cert=self.cfg.ssl_client_ca,
            scheme=self.cfg.scheme)
        self.elr.connect()
        self.elr.create_repo(
            self.cfg.repo_name, os.path.join(
                self.cfg.phy_repo_dir, self.cfg.repo_name))

        with gen_libs.no_std_out():
            self.assertFalse(
                elastic_db_dump.create_repo(self.els, args=self.args))

    def test_repo_create(self):

        """Function:  test_repo_create

        Description:  Test repository is created.

        Arguments:

        """

        elastic_db_dump.create_repo(self.els, args=self.args)
        self.elr = ecls.ElasticSearchRepo(
            self.cfg.host, port=self.cfg.port, user=self.cfg.user,
            japd=self.cfg.japd, ca_cert=self.cfg.ssl_client_ca,
            scheme=self.cfg.scheme)
        self.elr.connect()

        self.assertIn(self.cfg.repo_name, self.elr.repo_dict)

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
