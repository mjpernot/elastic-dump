#!/usr/bin/python
# Classification (U)

"""Program:  elastic_db_dump.py

    Description:  Execute a dump of an Elasticsearch database.

    Usage:
        elastic_db_dump.py -c file -d path
            {-C repo_name -l base_path | -L [repo_name] | -R |
             -D [repo_name] [-i index1 {index2 ...}] [-o]}
            [-v | -h]

    Arguments:
        -c file => Elasticsearch configuration file.
        -d dir path => Directory path for option '-c'.

        -C repo_name => Create new repository name.
            -l base_path => Base directory path name for repository.

        -D [repo_name] => Dump an Elasticsearch database.  repo_name is name
            of repository to dump.
                Note:  repo_name is required if multiple repositories exist or
                if the -i option is used.
            -i index1 {index2 ...} => One or more indices to dump.
                Note: Can use wildcard searches in the index name.
            -o => Override the master check and dump from local node.

        -L [repo_name] => List of database dumps for an Elasticsearch
            repository.
                Note: repo_name is required if multiple repositories exist.

        -R => List of repositories in the Elasticsearch database.

        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1:  -v or -h overrides all other options.
        NOTE 2:  -C, -D, -L, and -R are XOR options.

    Notes:
        Elasticsearch configuration file format (config/elastic.py.TEMPLATE).
        The configuration file format for the Elasticsearch connection to a
        database.

            # Elasticsearch configuration file
            host = ["https://HOST_NAME1:9200", "https://HOST_NAME2:9200"]

            # Login credentials
            user = None
            japd = None

            # SSL connection
            ssl_client_ca = None

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
try:
    from .lib import gen_libs
    from .lib import gen_class
    from .elastic_lib import elastic_class
    from .elastic_lib import elastic_libs
    from . import version

except (ValueError, ImportError) as err:
    import lib.gen_libs as gen_libs                     # pylint:disable=R0402
    import lib.gen_class as gen_class                   # pylint:disable=R0402
    import elastic_lib.elastic_class as elastic_class   # pylint:disable=R0402
    import elastic_lib.elastic_libs as elastic_libs     # pylint:disable=R0402
    import version

__version__ = version.__version__


def help_message():

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
        (input) els -> ElasticSearch class instance
        (input) **kwargs:
            args -> ArgParser class instance

    """

    args = kwargs.get("args")
    repo_name = args.get_val("-C")
    repo_dir = args.get_val("-l")
    elr = elastic_class.ElasticSearchRepo(
        els.hosts, port=els.port, user=els.user, japd=els.japd,
        ca_cert=els.ca_cert, scheme=els.scheme)
    elr.connect()

    if elr.is_connected:
        if repo_name in elr.repo_dict:
            print(f"ERROR:  {repo_name} repository already exists at:"
                  f" {repo_dir}")

        else:
            err_flag, msg = elr.create_repo(
                repo_name, os.path.join(repo_dir, repo_name))

            if err_flag:
                print(f"Error detected for Repository: {repo_name} at"
                      f" {repo_dir}")
                print(f"Reason: {msg}")

    else:
        print("Error: create_repo: Failed to connect to Elasticsearch")


def print_failures(els):

    """Function:  print_failures

    Description:  Prints out failures detected within the class.

    Arguments:
        (input) els -> Elasticsearch class instance

    """

    print(f"Failed to dump on {els.failed_shards} shards")
    print(f"Detected failures: {els.failures}")


def initate_dump(els, dbs_list=None, **kwargs):

    """Function:  initate_dump

    Description:  Execute a dump of the Elasticsearch database and check on
        the return status of the database dump.

    Arguments:
        (input) els -> Elasticsearch class instance
        (input) dbs_list -> String of comma-delimited indice names to dump
        (input) **kwargs:
            args -> ArgParser class instance

    """

    args = kwargs.get("args")

    if els.master != els.node_connected_to and not args.arg_exist("-o"):
        return
 
    if args.arg_exist("-i"):
        dbs_list = ','.join(args.get_val("-i"))

    err_flag, status_msg = els.dump_db(dbs=dbs_list)

    # Failed to execute dump
    if err_flag:
        print(f"Failed to execute dump on Cluster: {els.cluster_name}")
        print(f"Message:  {status_msg}")

    # Check dump if anything other than success
    elif els.dump_status != "SUCCESS":

        if els.dump_status == "FAILED":
            print(f"Dump failed to finish on {els.cluster_name}")
            print(f"Message:  {status_msg}")

        elif els.dump_status == "PARTIAL":
            print(f"Partial dump completed on {els.cluster_name}")
            print_failures(els)

        elif els.dump_status == "INCOMPATIBLE":
            print(f"Older version of Elasticsearch in repo detected"
                  f" {els.cluster_name}")

        else:
            print(f"Unknown error detected on {els.cluster_name}")
            print(f"Message:  {status_msg}")


def list_dumps(els, **kwargs):                          # pylint:disable=W0613

    """Function:  list_dumps

    Description:  Lists the dumps in a repository.

    Arguments:
        (input) els -> Elasticsearch class instance
        (input) **kwargs:
            args -> ArgParser class instance

    """

    if els.repo_name:
        elastic_libs.list_dumps(els.dump_list)

    else:
        print("WARNING:  Repository name not found or not passed.")


def list_repos(els, **kwargs):                          # pylint:disable=W0613

    """Function:  list_repos

    Description:  Lists the repositories present.

    Arguments:
        (input) els -> Elasticsearch class instance
        (input) **kwargs:
            args -> ArgParser class instance

    """

    elr = elastic_class.ElasticSearchRepo(
        els.hosts, port=els.port, user=els.user, japd=els.japd,
        ca_cert=els.ca_cert, scheme=els.scheme)
    elr.connect()

    if elr.is_connected:
        elastic_libs.list_repos2(elr.repo_dict)

    else:
        print("Error: list_repos: Failed to connect to Elasticsearch")


def run_program(args, func_dict):

    """Function:  run_program

    Description:  Creates class instance and controls flow of the program.
        Create a program lock to prevent other instantiations from running.

    Arguments:
        (input) args -> ArgParser class instance
        (input) func_dict -> Dictionary list of functions and options

    """

    func_dict = dict(func_dict)
    cfg = gen_libs.load_module(args.get_val("-c"), args.get_val("-d"))
    user = cfg.user if hasattr(cfg, "user") else None
    japd = cfg.japd if hasattr(cfg, "japd") else None
    ca_cert = cfg.ssl_client_ca if hasattr(cfg, "ssl_client_ca") else None
    scheme = cfg.scheme if hasattr(cfg, "scheme") else "https"
    flavorid = "elasticdump"

    try:
        prog_lock = gen_class.ProgramLock(sys.argv, flavor_id=flavorid)

        for opt in set(args.get_args_keys()) & set(func_dict.keys()):
            els = elastic_class.ElasticSearchDump(
                cfg.host, port=cfg.port, repo=args.get_val(opt, def_val=None),
                user=user, japd=japd, ca_cert=ca_cert, scheme=scheme)
            els.connect()

            if els.is_connected:
                func_dict[opt](els, args=args)

            else:
                print("ERROR:  Failed to connect to Elasticsearch")

        del prog_lock

    except gen_class.SingleInstanceException:
        print(f"WARNING:  elastic_db_dump lock in place for: {flavorid}")


def main():

    """Function:  main

    Description:  Initializes program-wide used variables and processes command
        line arguments and values.

    Variables:
        dir_perms_chk -> contains options which will be directories and the
            octal permission settings
        func_dict -> dictionary list for the function calls or other options
        opt_con_req_dict -> contains options requiring other options
        opt_multi_list -> contains the options that will have multiple values
        opt_req_list -> contains options that are required for the program
        opt_val_bin -> List of options that allow 0 or 1 value for option
        opt_val -> contains options which require values
        opt_xor_dict -> contains dict with key that is xor with it's values

    Arguments:
        (input) argv -> Arguments from the command line

    """

    dir_perms_chk = {"-d": 5}
    func_dict = {
        "-C": create_repo, "-D": initate_dump, "-L": list_dumps,
        "-R": list_repos}
    opt_con_req_dict = {"-C": ["-l"], "-i": ["-D"]}
    opt_multi_list = ["-i"]
    opt_req_list = ["-c", "-d"]
    opt_val_bin = ["-D", "-L"]
    opt_val = ["-c", "-d", "-i", "-l", "-C"]
    opt_xor_dict = {
        "-C": ["-D", "-L", "-R"], "-D": ["-C", "-L", "-R"],
        "-L": ["-C", "-D", "-R"], "-R": ["-C", "-D", "-L"]}

    # Process argument list from command line.
    args = gen_class.ArgParser(
        sys.argv, opt_val=opt_val, opt_val_bin=opt_val_bin,
        multi_val=opt_multi_list)

    if args.arg_parse2()                                            \
       and not gen_libs.help_func(args, __version__, help_message)  \
       and args.arg_require(opt_req=opt_req_list)                   \
       and args.arg_xor_dict(opt_xor_val=opt_xor_dict)              \
       and args.arg_cond_req_or(opt_con_or=opt_con_req_dict)        \
       and args.arg_dir_chk(dir_perms_chk=dir_perms_chk):
        run_program(args, func_dict)


if __name__ == "__main__":
    sys.exit(main())
