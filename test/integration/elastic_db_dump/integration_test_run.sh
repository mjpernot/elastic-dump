#!/bin/bash
# Integration testing program for the elastic_db_dump.py program.
# This will run all the integrations tests for this program.
# Will need to run this from the base directory where the program file
#   is located at.

echo ""
echo "Integration test:"
/usr/bin/python test/integration/elastic_db_dump/create_repo.py
/usr/bin/python test/integration/elastic_db_dump/initate_dump.py
/usr/bin/python test/integration/elastic_db_dump/list_dumps.py
/usr/bin/python test/integration/elastic_db_dump/list_repos.py
/usr/bin/python test/integration/elastic_db_dump/run_program.py
/usr/bin/python test/integration/elastic_db_dump/main.py

