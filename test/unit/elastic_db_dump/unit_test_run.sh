#!/bin/bash
# Unit testing program for the elastic_db_dump.py module.
# This will run all the units tests for this program.
# Will need to run this from the base directory where the module file
#   is located at.

echo ""
echo "Unit test:"
test/unit/elastic_db_dump/help_message.py
test/unit/elastic_db_dump/print_failures.py
test/unit/elastic_db_dump/create_repo.py
test/unit/elastic_db_dump/initate_dump.py
test/unit/elastic_db_dump/list_dumps.py
test/unit/elastic_db_dump/list_repos.py
test/unit/elastic_db_dump/run_program.py
test/unit/elastic_db_dump/main.py

