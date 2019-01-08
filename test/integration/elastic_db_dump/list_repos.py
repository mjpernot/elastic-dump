#!/usr/bin/python
# Classification (U)

"""Program:  list_repos.py

    Description:  Integration testing of list_repos in elastic_db_dump.py.

    Usage:
        test/integration/elastic_db_dump/list_repos.py

    Arguments:
        None

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

# Version
__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Super-Class:  unittest.TestCase

    Sub-Classes:  None

    Methods:
        setUp -> Unit testing initilization.
        test_list_repos -> Test listing of repositories.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:
            None

        """

        self.base_dir = "test/integration/elastic_db_dump"
        self.test_path = os.path.join(os.getcwd(), self.base_dir)
        self.config_path = os.path.join(self.test_path, "config")
        self.cfg = gen_libs.load_module("elastic", self.config_path)

        self.ES = elastic_class.ElasticSearchDump(self.cfg.host, self.cfg.port)

    def test_list_repos(self):

        """Function:  test_list_repos

        Description:  Test listing of repositories.

        Arguments:
            None

        """

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.list_repos(self.ES))


if __name__ == "__main__":
    unittest.main()
