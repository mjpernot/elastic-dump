#!/bin/bash
# Unit testing program for the elastic_db_dump.py module.
# This will run all the units tests for this program.
# Will need to run this from the base directory where the module file
#   is located at.

echo ""
echo "Unit test:"
/usr/bin/python3 test/unit/elastic_db_dump/help_message.py
/usr/bin/python3 test/unit/elastic_db_dump/print_failures.py
/usr/bin/python3 test/unit/elastic_db_dump/create_repo.py
/usr/bin/python3 test/unit/elastic_db_dump/initate_dump.py
/usr/bin/python3 test/unit/elastic_db_dump/list_dumps.py
/usr/bin/python3 test/unit/elastic_db_dump/list_repos.py
/usr/bin/python3 test/unit/elastic_db_dump/run_program.py
/usr/bin/python3 test/unit/elastic_db_dump/main.py

