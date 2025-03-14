# Classification (U)

"""Program:  list_repos.py

    Description:  Integration testing of list_repos in elastic_db_dump.py.

    Usage:
        test/integration/elastic_db_dump/list_repos.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest

# Local
sys.path.append(os.getcwd())
import elastic_db_dump                          # pylint:disable=E0401,C0413
import lib.gen_libs as gen_libs             # pylint:disable=E0401,C0413,R0402
import elastic_lib.elastic_class as ecls    # pylint:disable=E0401,C0413,R0402
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_list_repos

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
        self.els = ecls.ElasticSearchDump(
            self.cfg.host, port=self.cfg.port, user=self.cfg.user,
            japd=self.cfg.japd, ca_cert=self.cfg.ssl_client_ca,
            scheme=self.cfg.scheme)
        self.els.connect()

    def test_list_repos(self):

        """Function:  test_list_repos

        Description:  Test listing of repositories.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.list_repos(self.els))


if __name__ == "__main__":
    unittest.main()
