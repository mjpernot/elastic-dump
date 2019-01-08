#!/usr/bin/python
# Classification (U)

"""Program:  list_repos.py

    Description:  Unit testing of list_repos in elastic_db_dump.py.

    Usage:
        test/unit/elastic_db_dump/list_repos.py

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
import mock

# Local
sys.path.append(os.getcwd())
import elastic_db_dump
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
        test_list_repos -> Test the printing of respositories.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:
            None

        """

        class ElasticSearchDump(object):

            """Class:  ElasticSearchDump

            Description:  Class representation of the ElasticSearchDump class.

            Super-Class:  object

            Sub-Classes:  None

            Methods:
                __init__ -> Initialize configuration environment.

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the class.

                Arguments:
                        None

                """

                self.hosts = ["Server1"]
                self.port = 9000

        self.ES = ElasticSearchDump()

        class ElasticSearchRepo(object):

            """Class:  ElasticSearchRepo

            Description:  Class representation of the ElasticSearchRepo class.

            Super-Class:  object

            Sub-Classes:  None

            Methods:
                __init__ -> Initialize configuration environment.

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the class.

                Arguments:
                        None

                """

                self.repo_dict = {}

        self.ER = ElasticSearchRepo()

    @mock.patch("elastic_db_dump.elastic_libs.list_repos2")
    @mock.patch("elastic_db_dump.elastic_class.ElasticSearchRepo")
    def test_list_repos(self, mock_er, mock_list):

        """Function:  test_list_repos

        Description:  Test the printing of respositories.

        Arguments:
            mock_er -> Mock Ref:
                elastic_db_dump.elastic_class.ElasticSearchRepo
            mock_list -> Mock Ref:  elastic_db_dump.elastic_libs.list_repos2

        """

        mock_er.return_value = self.ER
        mock_list.return_value = True

        self.assertFalse(elastic_db_dump.list_repos(self.ES))


if __name__ == "__main__":
    unittest.main()
