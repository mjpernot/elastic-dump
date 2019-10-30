#!/usr/bin/python
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

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

# Third-party

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
        test_print_failures -> Test call to print_failures function.

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

                self.failed_shards = 2
                self.failures = ["Test_Shard_1", "Test_Shard_2"]

        self.es = ElasticSearchDump()

    def test_print_failures(self):

        """Function:  test_print_failures

        Description:  Test call to print_failures function.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.print_failures(self.es))


if __name__ == "__main__":
    unittest.main()
