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
import elastic_db_dump
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


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

                self.failed_shards = 2
                self.failures = ["Test_Shard_1", "Test_Shard_2"]

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
