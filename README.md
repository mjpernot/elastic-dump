# Python project for the dumping of a database on an Elasticsearch database.
# Classification (U)


# Description:
  Used to dump a database on an Elasticsearch database.  This includes dumping a database, listing repositories, and listing database dumps.


###  This README file is broken down into the following sections:
  * Features
  * Installation
  * Prerequisites
  * Configuration
  * Program Help Function
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

  * List of Linux packages that need to be installed on the server.
    - Centos 7 (Running Python 2.7):
      -> python-pip
    - Redhat 8 (Running Python 3.6):
      -> python3-pip


# Installation:

Install the project using git.
  * From here on out, any reference to **{Python_Project}** or **PYTHON_PROJECT** replace with the baseline path of the python program.

```
git clone git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/elastic-dump.git
cd elastic-dump
```

Install/upgrade system modules.

Centos 7 (Running Python 2.7):
```
sudo pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
```

Redhat 8 (Running Python 3.6):
NOTE: Install as the user that will run the program.

```
python -m pip install --user -r requirements3.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
```


Install supporting classes and libraries.

Centos 7 (Running Python 2.7):
```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-elastic-lib.txt --target elastic_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-elastic-python-lib.txt --target elastic_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

Redhat 8 (Running Python 3.6):
```
python -m pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-elastic-lib.txt --target elastic_lib --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-elastic-python-lib.txt --target elastic_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```


# Configuration:

Make the appropriate changes to the Elasticsearch environment.
  * Change these entries in the elasticsearch set up:
    - host = ["https://HOST_NAME1:9200", "https://HOST_NAME2:9200"]

  * If login credentials are required:
    - user = None
    - japd = None

  * If SSL connections are being used:
    - ssl_client_ca = None

  * Change these entries only if required and you know what you are doing:
    - port = 9200
    - scheme = "https"

```
cd config
cp elastic.py.TEMPLATE elastic.py
vim elastic.py
sudo chown elasticsearch:elasticsearch elastic.py
```


# Program Help Function:

  All of the programs, except the command and class files, will have an -h (Help option) that will show display a help message for that particular program.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:

```
{Python_Project}/elastic-dump/elastic_db_dump.py -h
```


# Testing:

# Unit Testing:

### Installation:

Install the project using the procedures in the Installation section.

### Testing:

```
cd {Python_Project}/elastic-dump
test/unit/elastic_db_dump/unit_test_run3.sh
```

### Code coverage:

```
cd {Python_Project}/elastic-dump
test/unit/elastic_db_dump/code_coverage.sh
```


# Integration Testing:

### Installation:

Install the project using the procedures in the Installation section.

### Configuration:

Make the appropriate changes to the Elasticsearch environment.
  * Change these entries in the elasticsearch set up:
    - host = ["https://HOST_NAME1:9200", "https://HOST_NAME2:9200"]

  * If login credentials are required:
    - user = None
    - japd = None

  * If SSL connections are being used:
    - ssl_client_ca = None

  * Change these entries only if required and you know what you are doing:
    - port = 9200
    - scheme = "https"

  * In addition to the normal configuration entries, modify these entries for this testing section.
    Note 1:  **LOGICAL_DIR_PATH** is the logical directory path to the share file system.
    Note 2:  **phy_repo_dir** is the physical directory path to the share file system.
    Note 3:  If running ElasticSearch as Docker setup, then these paths will be different.  If running as a standard setup, they will be the same.
    - log_repo_dir = "LOGICAL_DIR_PATH"
    - phy_repo_dir = "PHYSICAL_DIR_PATH"

```
cd test/integration/elastic_db_dump/config
cp elastic.py.TEMPLATE elastic.py
vim elastic.py
sudo chown elasticsearch:elasticsearch elastic.py
```

### Pre-Testing:
  *  These tests will require at least two user indices to exist in Elasticsearch.

```
curl -X GET "localhost:9200/\_cat/indices?v"
```

  *  Creating two user indices for testing.

```
curl -XPUT 'localhost:9200/twitter?pretty' -H 'Content-Type: application/json' -d'{"settings" : {"index" : {"number_of_shards" : 3, "number_of_replicas" : 0 }}}'
curl -XPUT 'localhost:9200/twitter2?pretty' -H 'Content-Type: application/json' -d'{"settings" : {"index" : {"number_of_shards" : 3, "number_of_replicas" : 0 }}}'
```

### Testing:
  * These tests must be run as the elasticsearch account:

```
cd {Python_Project}/elastic-dump
test/integration/elastic_db_dump/integration_test_run3.sh
```

### Code coverage:

```
cd {Python_Project}/elastic-dump
test/integration/elastic_db_dump/code_coverage.sh
```


# Blackbox Testing:

### Installation:

Install the project using the procedures in the Installation section.

Install/upgrade system modules.

### Configuration:

Create Elasticsearch configuration file.

Make the appropriate changes to the Elasticsearch environment.
  * Change these entries in the elasticsearch set up:
    - host = ["https://HOST_NAME1:9200", "https://HOST_NAME2:9200"]

  * If login credentials are required:
    - user = None
    - japd = None

  * If SSL connections are being used:
    - ssl_client_ca = None

  * Change these entries only if required and you know what you are doing:
    - port = 9200
    - scheme = "https"

```
cd test/blackbox/elastic_db_dump/config
cp ../../../../config/elastic.py.TEMPLATE elastic.py
vim elastic.py
sudo chown elasticsearch:elasticsearch elastic.py
```

Setup the test environment for Blackbox testing.
    Note 1:  **REPOSITORY_DIR** is the logical directory path to the share file system.  For use in a Docker set up.
    Note 2:  **PYH_REPO_DIR** is the physical directory path to the share file system.
    Note 3:  If running ElasticSearch as Docker setup, then these two paths will be different.  If running as a standard setup, they will be the same.
  * Change these entries in the blackbox_test.sh file:
    - REPOSITORY_DIR="LOGICAL_DIR_PATH/TEST_REPO_BLACKBOX_DIR"
    - PYH_REPO_DIR="PHYSICAL_DIR_PATH/TEST_REPO_BLACKBOX_DIR"

```
cd ..
cp blackbox_test.sh.TEMPLATE blackbox_test.sh
vim blackbox_test.sh
```

### Pre-Testing:
  *  These tests will require at least one user indice to exist in Elasticsearch.

```
curl -X GET "localhost:9200/\_cat/indices?v"
```

  *  Creating one user indice for testing.

```
curl -XPUT 'localhost:9200/twitter?pretty' -H 'Content-Type: application/json' -d'{"settings" : {"index" : {"number_of_shards" : 3, "number_of_replicas" : 0 }}}'
```

### Testing:
  * These tests must be run as the elasticsearch account.

```
cd {Python_Project}/elastic-dump
test/blackbox/elastic_db_dump/blackbox_test.sh
```

