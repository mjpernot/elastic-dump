#!/usr/bin/python
# Classification (U)

"""Program:  list_dumps.py

    Description:  Unit testing of list_dumps in elastic_db_dump.py.

    Usage:
        test/unit/elastic_db_dump/list_dumps.py

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


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Unit testing initilization.
        test_repo_name_true -> Test repo name set to a name.
        test_repo_name_false -> Test repo name set to None.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        class ElasticSearchDump(object):

            """Class:  ElasticSearchDump

            Description:  Class representation of the ElasticSearchDump class.

            Methods:
                __init__ -> Initialize configuration environment.

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the class.

                Arguments:

                """

                self.repo_name = "Test_Repo_Name"
                self.dump_list = []

        self.es = ElasticSearchDump()

    @mock.patch("elastic_db_dump.elastic_libs.list_dumps")
    def test_repo_name_true(self, mock_list):

        """Function:  test_repo_name_true

        Description:  Test repo name set to a name.

        Arguments:

        """

        mock_list.return_value = True

        self.assertFalse(elastic_db_dump.list_dumps(self.es))

    def test_repo_name_false(self):

        """Function:  test_repo_name_false

        Description:  Test repo name set to None.

        Arguments:

        """

        self.es.repo_name = None

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.list_dumps(self.es))


if __name__ == "__main__":
    unittest.main()
