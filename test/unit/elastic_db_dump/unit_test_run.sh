#!/bin/bash
# Unit testing program for the elastic_db_dump.py module.
# This will run all the units tests for this program.
# Will need to run this from the base directory where the module file
#   is located at.

echo ""
echo "Unit test:  help_message"
test/unit/elastic_db_dump/help_message.py

echo ""
echo "Unit test:  print_failures"
test/unit/elastic_db_dump/print_failures.py

echo ""
echo "Unit test:  create_repo"
test/unit/elastic_db_dump/create_repo.py

echo ""
echo "Unit test:  initate_dump"
test/unit/elastic_db_dump/initate_dump.py

echo ""
echo "Unit test:  list_dumps"
test/unit/elastic_db_dump/list_dumps.py

echo ""
echo "Unit test:  list_repos"
test/unit/elastic_db_dump/list_repos.py

echo ""
echo "Unit test:  run_program"
test/unit/elastic_db_dump/run_program.py

echo ""
echo "Unit test:  main"
test/unit/elastic_db_dump/main.py

