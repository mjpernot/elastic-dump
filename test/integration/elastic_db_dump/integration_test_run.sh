#!/bin/bash
# Integration testing program for the elastic_db_dump.py program.
# This will run all the integrations tests for this program.
# Will need to run this from the base directory where the program file
#   is located at.

echo ""
echo "Integration test:  create_repo"
test/integration/elastic_db_dump/create_repo.py

echo ""
echo "Integration test:  initate_dump"
test/integration/elastic_db_dump/initate_dump.py

echo ""
echo "Integration test:  list_dumps"
test/integration/elastic_db_dump/list_dumps.py

echo ""
echo "Integration test:  list_repos"
test/integration/elastic_db_dump/list_repos.py

echo ""
echo "Integration test:  run_program"
test/integration/elastic_db_dump/run_program.py

echo ""
echo "Integration test:  main"
test/integration/elastic_db_dump/main.py

