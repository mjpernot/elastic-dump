#!/usr/bin/python
# Classification (U)

"""Program:  list_repos.py

    Description:  Unit testing of list_repos in elastic_db_dump.py.

    Usage:
        test/unit/elastic_db_dump/list_repos.py

    Arguments:

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
import mock

# Local
sys.path.append(os.getcwd())
import elastic_db_dump
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class ElasticSearchDump(object):

    """Class:  ElasticSearchDump

    Description:  Class representation of the ElasticSearchDump class.

    Methods:
        __init__

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the class.

        Arguments:

        """

        self.hosts = ["Server1"]
        self.port = 9200
        self.user = "user"
        self.japd = "japd"
        self.ca_cert = "ca_cert"
        self.scheme = "https"


class ElasticSearchRepo(object):

    """Class:  ElasticSearchRepo

    Description:  Class representation of the ElasticSearchRepo class.

    Methods:
        __init__
        connect

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the class.

        Arguments:

        """

        self.repo_dict = {}
        self.is_connected = True

    def connect(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        return True


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_connection_failed
        test_connection_successful
        test_list_repos

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.els = ElasticSearchDump()
        self.elr = ElasticSearchRepo()

    @mock.patch("elastic_db_dump.elastic_class.ElasticSearchRepo")
    def test_connection_failed(self, mock_er):

        """Function:  test_connection_failed

        Description:  Test with failed connection.

        Arguments:

        """

        self.elr.is_connected = False

        mock_er.return_value = self.elr

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.list_repos(self.els))

    @mock.patch("elastic_db_dump.elastic_libs.list_repos2")
    @mock.patch("elastic_db_dump.elastic_class.ElasticSearchRepo")
    def test_connection_successful(self, mock_er, mock_list):

        """Function:  test_connection_successful

        Description:  Test with successful connection.

        Arguments:

        """

        mock_er.return_value = self.elr
        mock_list.return_value = True

        self.assertFalse(elastic_db_dump.list_repos(self.els))

    @mock.patch("elastic_db_dump.elastic_libs.list_repos2")
    @mock.patch("elastic_db_dump.elastic_class.ElasticSearchRepo")
    def test_list_repos(self, mock_er, mock_list):

        """Function:  test_list_repos

        Description:  Test the printing of respositories.

        Arguments:

        """

        mock_er.return_value = self.elr
        mock_list.return_value = True

        self.assertFalse(elastic_db_dump.list_repos(self.els))


if __name__ == "__main__":
    unittest.main()
