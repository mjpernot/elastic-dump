# Classification (U)

"""Program:  print_failures.py

    Description:  Unit testing of print_failures in elastic_db_dump.py.

    Usage:
        test/unit/elastic_db_dump/print_failures.py

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
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class ElasticSearchDump():                              # pylint:disable=R0903

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

        self.failed_shards = 2
        self.failures = ["Test_Shard_1", "Test_Shard_2"]


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_print_failures

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.els = ElasticSearchDump()

    def test_print_failures(self):

        """Function:  test_print_failures

        Description:  Test call to print_failures function.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.print_failures(self.els))


if __name__ == "__main__":
    unittest.main()
