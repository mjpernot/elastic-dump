#!/usr/bin/python
# Classification (U)

"""Program:  blackbox_test.py

    Description:  Blackbox testing of elastic_db_dump.py program.

    Usage:
        test/blackbox/elastic_db_dump/blackbox_test.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import shutil

# Third-party

# Local
sys.path.append(os.getcwd())
import lib.gen_libs as gen_libs
import lib.arg_parser as arg_parser
import elastic_lib.elastic_class as elastic_class
import version

__version__ = version.__version__


def load_cfg(args_array, **kwargs):

    """Function:  load_cfg

    Description:  Read and load configuration into cfg.

    Arguments:
        (input) args_array -> Dict of command line options and values.
        (output) -> Server configuration settings.

    """

    return gen_libs.load_module(args_array["-c"], args_array["-d"])


def chk_create_repo(ER, repo_name, **kwargs):

    """Function:  chk_create_repo

    Description:  Check for the existence of a repository.

    Arguments:
        (input) ES -> Elasticsearch class instance.
        (input) repo_name -> Name of repository.
        (output) status -> True|False - Status of check.

    """

    status = True

    if repo_name not in ER.repo_dict:
        status = False

    return status


def create_es_instance(cfg, instance, repo_name=None, **kwargs):

    """Function:  create_es_instance

    Description:  Create instance of Elasticsearch database.

    Arguments:
        (input) cfg -> Server configuration settings.
        (input) instance -> ElasticSearch instance name.
        (input) repo_name -> Name of repository.
        (output) -> ElasticSearch instance.

    """

    return instance(cfg.host, cfg.port, repo=repo_name)


def remove_repo(ER, repo_name, dump_loc, **kwargs):

    """Function:  remove_repo

    Description:  Remove repository and cleanup directory.

    Arguments:
        (input) ER -> ElasticSearchRepo class instance.
        (input) repo_name -> Name of repository being removed.
        (input) dump_loc -> Location of repository.
        (output) status -> True|False - Status of repository removal.

    """

    status = True

    err_flag, msg = ER.delete_repo(repo_name=repo_name)

    if err_flag:
        status = False

        print("Error: Failed to remove repo '%s'" % repo_name)
        print("Reason: '%s'" % (msg))

    if os.path.isdir(dump_loc):
        shutil.rmtree(dump_loc)

    return status


def main():

    """Function:  main

    Description:  Control the blackbox testing of elastic_db_dump.py program.

    Variables:
        opt_val_list -> contains options which require values.

    Arguments:

    """

    opt_val_list = ["-c", "-d", "-C", "-R", "-D"]
    args_array = arg_parser.arg_parse2(sys.argv, opt_val_list)
    cfg = load_cfg(args_array)

    if "-C" in args_array:
        ES = create_es_instance(cfg, elastic_class.ElasticSearchDump,
                                args_array["-C"])
        ER = create_es_instance(cfg, elastic_class.ElasticSearchRepo,
                                args_array["-C"])

        if chk_create_repo(ER, args_array["-C"]):
            print("\n\tTest Successful")

        else:
            print("\n\tTest Failure")

        _ = remove_repo(ER, args_array["-C"], ES.dump_loc)

    elif "-R" in args_array:
        ES = create_es_instance(cfg, elastic_class.ElasticSearchDump,
                                args_array["-R"])
        ER = create_es_instance(cfg, elastic_class.ElasticSearchRepo,
                                args_array["-R"])
        _ = remove_repo(ER, args_array["-R"], ES.dump_loc)

    elif "-i" in args_array and "-D" in args_array:
        ES = create_es_instance(cfg, elastic_class.ElasticSearchDump,
                                args_array["-D"])
        ER = create_es_instance(cfg, elastic_class.ElasticSearchRepo,
                                args_array["-D"])
        dir_path = os.path.join(ES.dump_loc, "indices")

        # Count number of databases/indices dumped to repository.
        if len([name for name in os.listdir(dir_path)
                if os.path.isdir(os.path.join(dir_path, name))]) == 1:

            print("\n\tTest Successful")

        else:
            print("\n\tTest Failure")

        _ = remove_repo(ER, args_array["-D"], ES.dump_loc)

    elif "-D" in args_array:
        ES = create_es_instance(cfg, elastic_class.ElasticSearchDump,
                                args_array["-D"])
        ER = create_es_instance(cfg, elastic_class.ElasticSearchRepo,
                                args_array["-D"])

        if ES.dump_list:
            print("\n\tTest Successful")

        else:
            print("\n\tTest Failure")

        _ = remove_repo(ER, args_array["-D"], ES.dump_loc)

    elif "-I" in args_array:
        ES = create_es_instance(cfg, elastic_class.ElasticSearchDump)

        print(str([x.split() for x in ES.es.cat.indices().splitlines()][0][2]))


if __name__ == "__main__":
    sys.exit(main())
