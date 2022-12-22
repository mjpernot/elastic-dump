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
import unittest
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
        setUp
        test_repo_name_true
        test_repo_name_false

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
                __init__

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the class.

                Arguments:

                """

                self.repo_name = "Test_Repo_Name"
                self.dump_list = []

        self.els = ElasticSearchDump()

    @mock.patch("elastic_db_dump.elastic_libs.list_dumps")
    def test_repo_name_true(self, mock_list):

        """Function:  test_repo_name_true

        Description:  Test repo name set to a name.

        Arguments:

        """

        mock_list.return_value = True

        self.assertFalse(elastic_db_dump.list_dumps(self.els))

    def test_repo_name_false(self):

        """Function:  test_repo_name_false

        Description:  Test repo name set to None.

        Arguments:

        """

        self.els.repo_name = None

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.list_dumps(self.els))


if __name__ == "__main__":
    unittest.main()
