# Classification (U)

"""Program:  create_repo.py

    Description:  Unit testing of create_repo in elastic_db_dump.py.

    Usage:
        test/unit/elastic_db_dump/create_repo.py

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

        self.hosts = "Server_Name"
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
        create_repo

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the class.

        Arguments:

        """

        self.repo_dict = ["Test_Repo_Name_1", "Test_Rep_Name_2"]
        self.repo_name = None
        self.repo_dir = None
        self.is_connected = True

    def connect(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        return True

    def create_repo(self, repo_name, repo_dir):

        """Method:  create_repo

        Description:  Mock of creating a repository.

        Arguments:

        """

        self.repo_name = repo_name
        self.repo_dir = repo_dir
        err_flag = False
        err_msg = None

        if self.repo_name == "Test_Repo_Name_False":
            err_flag = True
            err_msg = "Error_Message_Here"

        return err_flag, err_msg


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_connection_failed
        test_connection_successful
        test_reponame_in_list
        test_reponame_not_in_list
        test_err_flag_false
        test_err_flag_true

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.els = ElasticSearchDump()
        self.elr = ElasticSearchRepo()
        self.args_array = {"-C": "Test_Repo_Name_3", "-l": "Repo_Directory"}

    @mock.patch("elastic_db_dump.elastic_class.ElasticSearchRepo")
    def test_connection_failed(self, mock_er):

        """Function:  test_connection_failed

        Description:  Test with failed connection.

        Arguments:

        """

        self.elr.is_connected = False

        mock_er.return_value = self.elr

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.create_repo(
                self.els, args_array=self.args_array))

    @mock.patch("elastic_db_dump.elastic_class.ElasticSearchRepo")
    def test_connection_successful(self, mock_er):

        """Function:  test_connection_successful

        Description:  Test with successful connection.

        Arguments:

        """

        mock_er.return_value = self.elr

        self.assertFalse(elastic_db_dump.create_repo(
            self.els, args_array=self.args_array))

    @mock.patch("elastic_db_dump.elastic_class.ElasticSearchRepo")
    def test_reponame_in_list(self, mock_er):

        """Function:  test_reponame_in_list

        Description:  Test repo name is in list.

        Arguments:

        """

        mock_er.return_value = self.elr

        self.args_array["-C"] = "Test_Repo_Name_1"

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.create_repo(
                self.els, args_array=self.args_array))

    @mock.patch("elastic_db_dump.elastic_class.ElasticSearchRepo")
    def test_reponame_not_in_list(self, mock_er):

        """Function:  test_reponame_not_in_list

        Description:  Test repo name is not in list.

        Arguments:

        """

        mock_er.return_value = self.elr

        self.assertFalse(elastic_db_dump.create_repo(
            self.els, args_array=self.args_array))

    @mock.patch("elastic_db_dump.elastic_class.ElasticSearchRepo")
    def test_err_flag_false(self, mock_er):

        """Function:  test_err_flag_false

        Description:  Test err_flag is set to False.

        Arguments:

        """

        mock_er.return_value = self.elr

        self.assertFalse(elastic_db_dump.create_repo(
            self.els, args_array=self.args_array))

    @mock.patch("elastic_db_dump.elastic_class.ElasticSearchRepo")
    def test_err_flag_true(self, mock_er):

        """Function:  test_err_flag_true

        Description:  Test err_flag is set to True.

        Arguments:

        """

        mock_er.return_value = self.elr

        self.args_array["-C"] = "Test_Repo_Name_False"

        with gen_libs.no_std_out():
            self.assertFalse(elastic_db_dump.create_repo(
                self.els, args_array=self.args_array))


if __name__ == "__main__":
    unittest.main()
