#!/usr/bin/python
# Classification (U)

"""Program:  elastic_db_dump.py

    Description:  Execute a dump of an Elasticsearch database.

    Usage:
        elastic_db_dump.py -c file -d path
            {-C repo_name -l base_path |
            -D [repo_name] [-i index1 {index2 ...}] |
            -L [repo_name] | -R}
            [-v | -h]

    Arguments:
        -c file => Elasticsearch configuration file.  Required argument.
        -d dir path => Directory path for option '-c'.  Required argument.
        -C repo_name => Create new repository name.  Requires -l option.
        -l base_path => Base directory path name for repository.
            Used with the -C option.
        -D [repo_name] => Dump an Elasticsearch database.  repo_name is name
            of repository to dump.  repo_name is required if multiple
            repositories exist or if used in conjunction with -i option.
        -i index1 {index2 ...} => One or more indices to dump.
            Used with the -D option.
            Can use wildcard searches in the index name.
        -L [repo_name] => List of database dumps for an Elasticsearch
            repository.
            NOTE: repo_name is required if multiple repositories exist.
        -R => List of repositories in the Elasticsearch database.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1:  -v or -h overrides all other options.
        NOTE 2:  -C, -D, -L, and -R are XOR options.

    Notes:
        Elasticsearch configuration file format (elastic.py).  The
        configuration file format for the Elasticsearch connection to a
        database.

            # Elasticsearch configuration file.
            name = ["HOSTNAME1", "HOSTNAME2"]
            # Default port for ElasticSearch is 9200.
            port = 9200

        Configuration modules -> Name is runtime dependent as it can be used to
        connect to different databases with different names.

    Example:
        elastic_db_dump.py -c elastic -d config -D backup

"""

# Libraries and Global Variables

# Standard
import sys
import os

# Local
import lib.arg_parser as arg_parser
import lib.gen_libs as gen_libs
import lib.gen_class as gen_class
import elastic_lib.elastic_class as elastic_class
import elastic_lib.elastic_libs as elastic_libs
import version

__version__ = version.__version__


def help_message(**kwargs):

    """Function:  help_message

    Description:  Displays the program's docstring which is the help and usage
        message when -h option is selected.

    Arguments:

    """

    print(__doc__)


def create_repo(els, **kwargs):

    """Function:  create_repo

    Description:  Create a repository for Elasticsearch database dumps.

    Arguments:
        (input) els -> ElasticSearch class instance.
        (input) **kwargs:
            args_array -> Dict of command line options and values.

    """

    args_array = dict(kwargs.get("args_array"))
    repo_name = args_array.get("-C")
    repo_dir = args_array.get("-l")
    elr = elastic_class.ElasticSearchRepo(els.hosts, els.port)

    if repo_name in elr.repo_dict:
        print("ERROR:  '%s' repository already exists at: '%s'"
              % (repo_name, repo_dir))

    else:
        err_flag, msg = elr.create_repo(repo_name,
                                        os.path.join(repo_dir, repo_name))

        if err_flag:
            print("Error detected for Repository: '%s' at '%s'"
                  % (repo_name, repo_dir))
            print("Reason: '%s'" % (msg))


def print_failures(els, **kwargs):

    """Function:  print_failures

    Description:  Prints out failures detected within the class.

    Arguments:
        (input) els -> Elasticsearch class instance.

    """

    print("Failed to dump on %s shards" % (els.failed_shards))
    print("Detected failures: %s" % (els.failures))


def initate_dump(els, dbs_list=None, **kwargs):

    """Function:  initate_dump

    Description:  Execute a dump of the Elasticsearch database and check on
        the return status of the database dump.

    Arguments:
        (input) els -> Elasticsearch class instance.
        (input) dbs_list -> String of comma-delimited indice names to dump.
        (input) **kwargs:
            args_array -> Dict of command line options and values.

    """

    prt_template = "Message:  %s"

    if "-i" in kwargs.get("args_array"):
        dbs_list = ','.join(kwargs.get("args_array").get("-i"))

    err_flag, status_msg = els.dump_db(dbs=dbs_list)

    # Failed to execute dump
    if err_flag:
        print("Failed to execute dump on Cluster: %s" % (els.cluster_name))
        print(prt_template % (status_msg))

    # Check dump if anything other than success
    elif els.dump_status != "SUCCESS":

        if els.dump_status == "FAILED":
            print("Dump failed to finish on %s" % (els.cluster_name))
            print(prt_template % (status_msg))

        elif els.dump_status == "PARTIAL":
            print("Partial dump completed on %s" % (els.cluster_name))
            print_failures(els)

        elif els.dump_status == "INCOMPATIBLE":
            print("Older version of Elasticsearch in repo detected %s"
                  % (els.cluster_name))

        else:
            print("Unknown error detected on %s" % (els.cluster_name))
            print(prt_template % (status_msg))


def list_dumps(els, **kwargs):

    """Function:  list_dumps

    Description:  Lists the dumps in a repository.

    Arguments:
        (input) els -> Elasticsearch class instance.

    """

    if els.repo_name:
        elastic_libs.list_dumps(els.dump_list, **kwargs)

    else:
        print("WARNING:  Repository name not found or not passed.")


def list_repos(els, **kwargs):

    """Function:  list_repos

    Description:  Lists the repositories present.

    Arguments:
        (input) els -> Elasticsearch class instance.

    """

    elr = elastic_class.ElasticSearchRepo(els.hosts, els.port)
    elastic_libs.list_repos2(elr.repo_dict)


def run_program(args_array, func_dict, **kwargs):

    """Function:  run_program

    Description:  Creates class instance and controls flow of the program.
        Create a program lock to prevent other instantiations from running.

    Arguments:
        (input) args_array -> Dict of command line options and values.
        (input) func_dict -> Dictionary list of functions and options.

    """

    cmdline = gen_libs.get_inst(sys)
    args_array = dict(args_array)
    func_dict = dict(func_dict)
    cfg = gen_libs.load_module(args_array["-c"], args_array["-d"])

    try:
        prog_lock = gen_class.ProgramLock(cmdline.argv, cfg.host)

        # Find which functions to call.
        for opt in set(args_array.keys()) & set(func_dict.keys()):
            els = elastic_class.ElasticSearchDump(
                cfg.host, cfg.port, args_array.get(opt, None), **kwargs)
            func_dict[opt](els, args_array=args_array, **kwargs)

        del prog_lock

    except gen_class.SingleInstanceException:
        print("WARNING:  elastic_db_dump lock in place for: %s" % (cfg.host))


def main():

    """Function:  main

    Description:  Initializes program-wide used variables and processes command
        line arguments and values.

    Variables:
        dir_chk_list -> contains options which will be directories.
        func_dict -> dictionary list for the function calls or other options.
        opt_con_req_dict -> contains options requiring other options.
        opt_multi_list -> contains the options that will have multiple values.
        opt_req_list -> contains options that are required for the program.
        opt_val -> List of options that allow 0 or 1 value for option.
        opt_val_list -> contains options which require values.
        opt_xor_dict -> contains dict with key that is xor with it's values.

    Arguments:
        (input) argv -> Arguments from the command line.

    """

    cmdline = gen_libs.get_inst(sys)
    dir_chk_list = ["-d"]
    func_dict = {"-C": create_repo, "-D": initate_dump, "-L": list_dumps,
                 "-R": list_repos}
    opt_con_req_dict = {"-C": ["-l"], "-i": ["-D"]}
    opt_multi_list = ["-i"]
    opt_req_list = ["-c", "-d"]
    opt_val = ["-D", "-L"]
    opt_val_list = ["-c", "-d", "-i", "-l", "-C"]
    opt_xor_dict = {"-C": ["-D", "-L", "-R"], "-D": ["-C", "-L", "-R"],
                    "-L": ["-C", "-D", "-R"], "-R": ["-C", "-D", "-L"]}

    # Process argument list from command line.
    args_array = arg_parser.arg_parse2(
        cmdline.argv, opt_val_list, opt_val=opt_val, multi_val=opt_multi_list)

    if not gen_libs.help_func(args_array, __version__, help_message) \
       and not arg_parser.arg_require(args_array, opt_req_list) \
       and arg_parser.arg_xor_dict(args_array, opt_xor_dict) \
       and arg_parser.arg_cond_req_or(args_array, opt_con_req_dict) \
       and not arg_parser.arg_dir_chk_crt(args_array, dir_chk_list):
        run_program(args_array, func_dict)


if __name__ == "__main__":
    sys.exit(main())
