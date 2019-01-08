# Python project for the dumping of a database on an Elasticsearch database.
# Classification (U)


# Description:
  This program is used to dump a database on an Elasticsearch database.  This includes dumping a database, listing repositories, and listing database dumps.


###  This README file is broken down into the following sections:
  * Features
  * Prerequisites
  * Installation
  * Configuration
  * Program Description
  * Program Help Function
  * Help Message
  * Testing
    - Unit
    - Integration
    - Blackbox


# Features:
  * Backup Elasticsearch database.
  * List current repositories in the Elasticsearch database.
  * List of database dumps for the Elasticsearch database.
  * Create new repositories for dumping Elasticsearch databases to.


# Prerequisites:
  * List of Linux packages that need to be installed on the server via git.
    - python-libs
    - python-devel
    - git
    - python-pip

  * Local class/library dependencies within the program structure.
    - lib/gen_class
    - lib/arg_parser
    - lib/gen_libs
    - elastic_lib/elastic_class
    - elastic_lib/elastic_libs


# Installation:

Install the project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.

```
umask 022
cd {Python_Project}
git clone git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/elastic-dump.git
```

Install/upgrade system modules.

```
cd elastic-dump
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-elastic-lib.txt --target elastic_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target elastic_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-requests-lib.txt --target elastic_lib/requests_lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

# Configuration:

Create Elasticsearch configuration file.  Make the appropriate changes to the Elasticsearch environment.
  * Change these entries in the elastic.py file.  List all the servers in the Elasticsearch cluster.  Add or delete HOST_NAMEs as necessary.
    - host = ["HOST_NAME1", "HOST_NAME2"]

```
cd config
cp elastic.py.TEMPLATE elastic.py
vim elastic.py
chmod 600 elastic.py
sudo chown elasticsearch:elasticsearch elastic.py
```


# Program Descriptions:
### Program: elastic_db_dump.py
##### Description: Execute a dump of an Elasticsearch database.


# Program Help Function:

  All of the programs, except the command and class files, will have an -h (Help option) that will show display a help message for that particular program.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
{Python_Project}/elastic-dump/elastic_db_dump.py -h
```


# Help Message:
  Below is the help message for the program the program.  Run the program with the -h option get the latest help message for the program.

    Program:  elastic_db_dump.py

    Description:  Execute a dump of an Elasticsearch database.

    Usage:
        elastic_db_dump.py -c file -d path {-R | -C repo_name -l rep_dir
            | -D [repo_name] [-i index1 {index2 ...}] | -L [repo_name]}
            [-v | -h]

    Arguments:
        -C repo_name => Create new repository name.  Requires -l option.
        -D [repo_name] => Dump an Elasticsearch database.  repo_name is name
            of repository to dump.  repo_name is required if multiple
            repositories exist or if used in conjunction with -i option.
        -L [repo_name] => List of database dumps for an Elasticsearch
            database.  repo_name is name of repository to dump.  repo_name is
            required if multiple repositories exist.
        -R => List of repositories in the Elasticsearch database.
        -c file => Elasticsearch configuration file.  Required argument.
        -d dir path => Directory path for option '-c'.  Required argument.
        -i index1 {index2 ...} => One or more indices to dump.  Used with the
            -D option.  Can use wildcard searches in the index name.
        -l path => Directory path name for repository.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1:  -v or -h overrides all other options.
        NOTE 2:  -C, -D, -L, and -R are XOR options.

    Notes:
        Elasticsearch configuration file format (elastic.py).  The
        configuration file format for the Elasticsearch connection to a
        database.

            # Elasticsearch configuration file.
            name = ["HOST_NAME1", "HOST_NAME2"]
            port = PORT_NUMBER (default of Elasticsearch is 9200)

        Configuration modules -> Name is runtime dependent as it can be used to
        connect to different databases with different names.

    Example:
        elastic_db_dump.py -c elastic -d config -D backup


# Testing:

# Unit Testing:

### Description: Testing consists of unit testing for the functions in the elastic_db_dump.py program.

### Installation:

Install the project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/elastic-dump.git
```

Install/upgrade system modules.

```
cd elastic-dump
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-elastic-lib.txt --target elastic_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target elastic_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-requests-lib.txt --target elastic_lib/requests_lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

# Unit test runs for elastic_db_dump.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/elastic-dump
```

### Unit:  help_message

```
test/unit/elastic_db_dump/help_message.py
```

### Unit:  print_failures

```
test/unit/elastic_db_dump/print_failures.py
```

### Unit:  create_repo

```
test/unit/elastic_db_dump/create_repo.py
```

### Unit:  initate_dump

```
test/unit/elastic_db_dump/initate_dump.py
```

### Unit:  list_dumps

```
test/unit/elastic_db_dump/list_dumps.py
```

### Unit:  run_program

```
test/unit/elastic_db_dump/run_program.py
```

### Unit:  main

```
test/unit/elastic_db_dump/main.py
```

### All unit testing

```
test/unit/elastic_db_dump/unit_test_run.sh
```

### Code coverage program

```
test/unit/elastic_db_dump/code_coverage.sh
```


# Integration Testing:

### Description: Testing consists of integration testing of functions in the elastic_db_dump.py program.

### Installation:

Install the project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/elastic-dump.git
```

Install/upgrade system modules.

```
cd elastic-dump
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-elastic-lib.txt --target elastic_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target elastic_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-requests-lib.txt --target elastic_lib/requests_lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

### Configuration:

Create Elasticsearch configuration file.  Make the appropriate changes to the Elasticsearch environment.
  * Change these entries in the elastic.py file.  List all the servers in the Elasticsearch cluster.  Add or delete HOST_NAMEs as necessary.
    - host = ["HOST_NAME1", "HOST_NAME2"]
    - repo_dir = "REPO_DIRECTORY_PATH/TEST_INTR_REPO_DIR"
  * NOTE:  **REPO_DIRECTORY_PATH** is a directory path to a shared file system by all Elasticsearch databases in the cluster.

```
cd test/integration/elastic_db_dump/config
cp elastic.py.TEMPLATE elastic.py
vim elastic.py
chmod 600 elastic.py
sudo chown elasticsearch:elasticsearch elastic.py
```

# Integration test runs for elastic_db_dump.py:
  * These tests must be run as the elasticsearch account:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
sudo bash
su - elasticsearch
cd {Python_Project}/elastic-dump
```

### Integration:  create_repo

```
test/integration/elastic_db_dump/create_repo.py
```

### Integration:  initate_dump

```
test/integration/elastic_db_dump/initate_dump.py
```

### Integration:  list_dumps

```
test/integration/elastic_db_dump/list_dumps.py
```

### Integration:  run_program

```
test/integration/elastic_db_dump/run_program.py
```

### Integration:  main

```
test/integration/elastic_db_dump/main.py
```

### All integration testing

```
test/integration/elastic_db_dump/integration_test_run.sh
```

### Code coverage program

```
test/integration/elastic_db_dump/code_coverage.sh
```


# Blackbox Testing:

### Description: Testing consists of blackbox testing of the elastic_db_dump.py program.

### Installation:

Install the project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/elastic-dump.git
```

Install/upgrade system modules.

```
cd elastic-dump
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-elastic-lib.txt --target elastic_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target elastic_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-requests-lib.txt --target elastic_lib/requests_lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

### Configuration:

Create Elasticsearch configuration file.  Make the appropriate changes to the Elasticsearch environment.
  * Change these entries in the elastic.py file.  List all the servers in the Elasticsearch cluster.  Add or delete HOST_NAMEs as necessary.
    - host = ["HOST_NAME1", "HOST_NAME2"]

```
cd test/blackbox/elastic_db_dump/config
cp ../../../../config/elastic.py.TEMPLATE elastic.py
vim elastic.py
chmod 600 elastic.py
sudo chown elasticsearch:elasticsearch elastic.py
```

Setup the test environment for Blackbox testing.
  * Change these entries in the blackbox_test.sh file:
    - REPOSITORY_DIR="DIRECTORY_PATH/TEST_REPO_BLACKBOX_DIR"
  * NOTE:  **DIRECTORY_PATH** is a directory path to a shared file system that is shared and writable by all Elasticsearch databases in the cluster.

```
cd ..
cp blackbox_test.sh.TEMPLATE blackbox_test.sh
vim blackbox_test.sh
```

# Blackbox test run for elastic_db_dump.py:

### Blackbox:
  * These tests must be run as the elasticsearch account.
  * Replace **{Python_Project}** with the baseline path of the python program.

```
sudo bash
su - elasticsearch
cd {Python_Project}/elastic-dump
test/blackbox/elastic_db_dump/blackbox_test.sh
```

