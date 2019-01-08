#!/bin/bash
# Unit test code coverage for elastic_db_dump.py module.
# This will run the Python code coverage module against all unit test modules.
# This will show the amount of code that was tested and which lines of code
#   that was skipped during the test.

coverage erase

echo ""
echo "Running unit test modules in conjunction with coverage"
coverage run -a --source=elastic_db_dump test/unit/elastic_db_dump/help_message.py
coverage run -a --source=elastic_db_dump test/unit/elastic_db_dump/print_failures.py
coverage run -a --source=elastic_db_dump test/unit/elastic_db_dump/create_repo.py
coverage run -a --source=elastic_db_dump test/unit/elastic_db_dump/initate_dump.py
coverage run -a --source=elastic_db_dump test/unit/elastic_db_dump/list_dumps.py
coverage run -a --source=elastic_db_dump test/unit/elastic_db_dump/list_repos.py
coverage run -a --source=elastic_db_dump test/unit/elastic_db_dump/run_program.py
coverage run -a --source=elastic_db_dump test/unit/elastic_db_dump/main.py

echo ""
echo "Producing code coverage report"
coverage combine
coverage report -m
