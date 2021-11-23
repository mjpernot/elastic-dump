#!/usr/bin/python
# Classification (U)

"""Program:  run_program.py

    Description:  Unit testing of run_program in elastic_db_dump.py.

    Usage:
        test/unit/elastic_db_dump/run_program.py

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


def list_dumps(els, **kwargs):

    """Function:  list_dumps

    Description:  This is a function stub for elastic_db_dump.list_dumps.

    Arguments:

    """

    status = True

    if els and dict(kwargs.get("args_array")):
        status = True

    return status


def disk_usage(els, **kwargs):

    """Function:  disk_usage

    Description:  This is a function stub for elastic_db_dump.disk_usage.

    Arguments:

    """

    status = True

    if els and dict(kwargs.get("args_array")):
        status = True

    return status


class ProgramLock(object):

    """Class:  ProgramLock

    Description:  Class stub holder for gen_class.ProgramLock class.

    Methods:
        __init__

    """

    def __init__(self, cmdline, flavor):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.cmdline = cmdline
        self.flavor = flavor


class CfgTest(object):

    """Class:  CfgTest

    Description:  Class which is a representation of a cfg module.

    Methods:
        __init__

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the CfgTest class.

        Arguments:

        """

        self.host = "SERVER_NAME"
        self.port = 9200
        self.user = None
        self.japd = None
        self.ssl_client_ca = None
        self.scheme = "https"


class ElasticSearchDump(object):

    """Class:  ElasticSearchDump

    Description:  Class stub holder for elastic_class.ElasticSearchDump class.

    Methods:
        __init__
        connect

    """

    def __init__(self, host, port, repo, user, japd, ca_cert, scheme):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.host = host
        self.port = port
        self.repo = repo
        self.user = user
        self.japd = japd
        self.ca_cert = ca_cert
        self.scheme = scheme
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
        test_failed_connection
        test_success_connection
        test_exception_handler
        test_func_call_multi
        test_func_call_one
        test_func_call_zero

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.cfg = CfgTest()
        self.args = {"-c": "config_file", "-d": "config_dir"}
        self.func_dict = {"-L": list_dumps, "-U": disk_usage}
        self.proglock = ProgramLock(["cmdline"], "FlavorID")

    @mock.patch("elastic_db_dump.gen_libs.load_module")
    @mock.patch("elastic_db_dump.elastic_class.ElasticSearchDump")
    @mock.patch("elastic_db_dump.gen_class")
    def test_failed_connection(self, mock_lock, mock_class, mock_load):

        """Function:  test_failed_connection

        Description:  Test with failed connection.

        Arguments:

        """

        self.args["-L"] = True

        els = ElasticSearchDump(
            "host", port=9200, repo="repo", user="user", japd="japd",
            ca_cert="ca_cert", scheme="https")
        els.is_connected = False

        mock_lock.return_value = self.proglock
        mock_class.return_value = els
        mock_load.return_value = self.cfg

        with gen_libs.no_std_out():
            self.assertFalse(
                elastic_db_dump.run_program(self.args, self.func_dict))

    @mock.patch("elastic_db_dump.gen_libs.load_module")
    @mock.patch("elastic_db_dump.elastic_class.ElasticSearchDump")
    @mock.patch("elastic_db_dump.gen_class")
    def test_success_connection(self, mock_lock, mock_class, mock_load):

        """Function:  test_success_connection

        Description:  Test with successful connection.

        Arguments:

        """

        els = ElasticSearchDump(
            self.cfg.host, self.cfg.port, None, self.cfg.user,
            self.cfg.japd, self.cfg.ssl_client_ca, self.cfg.scheme)

        self.args["-L"] = True

        mock_lock.return_value = self.proglock
        mock_class.return_value = els
        mock_load.return_value = self.cfg

        self.assertFalse(
            elastic_db_dump.run_program(self.args, self.func_dict))

    @mock.patch("elastic_db_dump.gen_libs.load_module")
    @mock.patch("elastic_db_dump.elastic_class.ElasticSearchDump")
    @mock.patch("elastic_db_dump.gen_class.ProgramLock")
    def test_exception_handler(self, mock_lock, mock_class, mock_load):

        """Function:  test_exception_handler

        Description:  Test with exception handler.

        Arguments:

        """

        els = ElasticSearchDump(
            self.cfg.host, self.cfg.port, None, self.cfg.user,
            self.cfg.japd, self.cfg.ssl_client_ca, self.cfg.scheme)

        self.args["-U"] = True
        self.args["-L"] = True

        mock_lock.side_effect = \
            elastic_db_dump.gen_class.SingleInstanceException
        mock_class.return_value = els
        mock_load.return_value = self.cfg

        with gen_libs.no_std_out():
            self.assertFalse(
                elastic_db_dump.run_program(self.args, self.func_dict))

    @mock.patch("elastic_db_dump.gen_libs.load_module")
    @mock.patch("elastic_db_dump.elastic_class.ElasticSearchDump")
    @mock.patch("elastic_db_dump.gen_class")
    def test_func_call_multi(self, mock_lock, mock_class, mock_load):

        """Function:  test_func_call_multi

        Description:  Test run_program function with multiple calls to
            function.

        Arguments:

        """

        els = ElasticSearchDump(
            self.cfg.host, self.cfg.port, None, self.cfg.user,
            self.cfg.japd, self.cfg.ssl_client_ca, self.cfg.scheme)

        self.args["-U"] = True
        self.args["-L"] = True

        mock_lock.return_value = self.proglock
        mock_class.return_value = els
        mock_load.return_value = self.cfg

        self.assertFalse(
            elastic_db_dump.run_program(self.args, self.func_dict))

    @mock.patch("elastic_db_dump.gen_libs.load_module")
    @mock.patch("elastic_db_dump.elastic_class.ElasticSearchDump")
    @mock.patch("elastic_db_dump.gen_class")
    def test_func_call_one(self, mock_lock, mock_class, mock_load):

        """Function:  test_func_call_one

        Description:  Test run_program function with one call to function.

        Arguments:

        """

        els = ElasticSearchDump(
            self.cfg.host, self.cfg.port, None, self.cfg.user,
            self.cfg.japd, self.cfg.ssl_client_ca, self.cfg.scheme)

        self.args["-L"] = True

        mock_lock.return_value = self.proglock
        mock_class.return_value = els
        mock_load.return_value = self.cfg

        self.assertFalse(
            elastic_db_dump.run_program(self.args, self.func_dict))

    @mock.patch("elastic_db_dump.gen_libs.load_module")
    @mock.patch("elastic_db_dump.elastic_class.ElasticSearchDump")
    @mock.patch("elastic_db_dump.gen_class")
    def test_func_call_zero(self, mock_lock, mock_class, mock_load):

        """Function:  test_func_call_zero

        Description:  Test run_program function with zero calls to function.

        Arguments:

        """

        els = ElasticSearchDump(
            self.cfg.host, self.cfg.port, None, self.cfg.user,
            self.cfg.japd, self.cfg.ssl_client_ca, self.cfg.scheme)

        mock_lock.return_value = self.proglock
        mock_class.return_value = els
        mock_load.return_value = self.cfg

        self.assertFalse(
            elastic_db_dump.run_program(self.args, self.func_dict))


if __name__ == "__main__":
    unittest.main()
