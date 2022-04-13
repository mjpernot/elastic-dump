# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


## [1.1.0] - 2022-04-13
- Updated to work in Elasticsearch 7.17.0
- Updated elastic-lib to v4.0.0

### Changed
- Documentation updates.


## [1.1.0] - 2021-11-22
- Updated to work in Elasticsearch 7.12.0
- Use login credentials and SSL connections

### Fixed
- list_dumps:  Removed \*\*kwargs from elastic_libs.list_dumps call.

### Changed
- list_repos, create_repo:  Added connect call and check for elasticsearch connection status.
- run_program:  Added connect call, check for elasticsearch connection status, and set login credentials and SSL connection settings.
- Removed unnecessary \*\*kwargs in function defintions.
- config/elastic.py.TEMPLATE:  Added login credentials and SSL connection entries.
- Documentation updates.


## [1.0.3] - 2020-06-24
### Fixed
- initate_dump:  Fixed call print_failures function.
- main, run_program:  Fixed handling command line arguments.

### Changed
- run_program, list_repos, list_dumps, initate_dump, print_failures, create_repo:  Changed variable names to standard naming convention.
- initate_dump: Added printing template variable.
- Documentation updates.


## [1.0.2] - 2019-10-28
### Fixed
- create_repo, run_program:  Fixed mutable list/dictionary argument issue.

### Changed
- create_repo:  Repo_name will be joined to repo_dir to create new repository.
- main:  Refactored "if" statements.
- run_program, list_repos, list_dumps, initate_dump, print_failures, create_repo:  Changed variables to standard naming convention.
- Documentation updates.


## [1.0.1] - 2018-11-22
### Changed
- Documentation updates.


## [1.0.0] - 2018-11-15
- General Release.

### Changed
- Documentation updates.


## [0.3.15] - 2018-11-14
### Changed
- Documentation updates.


## [0.3.14] - 2018-08-09
### Changed
- main:  Added new option "-i" to dump specific indices.
- initate_dump:  Parse "args_array" for "-i" option.


## [0.3.13] - 2018-07-06
Breaking Change

### Changed
- initate_dump:  Changed to use the new "ElasticSearchDump" class.
- run_program:  Changed "ElasticDump" class to "ElasticSearchDump" class.
- create_repo:  Refactor function to use the new "ElasticSearchRepo" class.
- main:  Changed "func_dict" to point to "list_repos" function.

### Added
- list_repos:  Lists the repositories present.


## [0.3.12] - 2018-06-06
### Changed
- create_repo:  Replaced kwargs.get with variables.


## [0.3.11] - 2018-06-04
### Changed
- Documentation updates.


## [0.3.10] - 2018-06-01
### Changed
- Documentation updates.


## [0.3.9] - 2018-04-26
### Changed
- Documentation updates.


## [0.3.8] - 2018-04-23
### Changed
- Reversed the changes for v0.3.7.


## [0.3.7] - 2018-04-23
### Changed
- Documentation updates.


## [0.3.6] - 2018-04-13
### Added
- create_repo: Create a repository for Elasticsearch database dumps.

### Changed
- main:  Added new option "-C" to create new repositories and additional checks.
- run_program:  Passed args_array as keyword argument to all function calls.


## [0.3.5] - 2018-04-11
### Changed
- run_program:  Changed "cfg.name" to "cfg.host".


## [0.3.4] - 2018-04-10
Breaking Change

### Changed
- Changed "gen_libs" calls to new naming schema.
- Changed "arg_parser" calls to new naming schema.
- Changed "gen_class" calls to new naming schema.
- Changed "elastic_class" calls to new naming schema.
- Changed "elastic_libs" calls to new naming schema.
- Changed function names from uppercase to lowercase.
- Setup single-source version control.


## [0.3.3] - 2018-04-10
### Added
- Added single-source version control.


## [0.3.2] - 2017-10-12
### Changed
- List_Dumps:  Pass dump list to funcion instead of class.
- Initate_Dump:  Clean up exception handler messages.


## [0.3.1] - 2017-10-11
### Fixed
- "-D" option with incorrect repository name still prints out header, giving impression something is there.

### Added
- List_Dumps:  Check repository name is valid.


## [0.3.0] - 2017-10-10
- Field release.


## [0.2.1] - 2017-09-19
### Changed 
- Run_Program:  Update exception handler message.


## [0.2.0] - 2017-09-18
- Beta release.


## [0.1.2] - 2017-09-18
### Changed
- List_Repos:  Replace Request query with referencing to class attribute.
- Run_Program:  Remove args_array from function calls.

### Removed
- List_Repos
- List_Dumps


## [0.1.1] - 2017-09-15
### Changed
- main:  Add argument value to -D and -L options to allow for a repository name to be passed to class.  This is if there are multiple repositories in Elasticsearch database.


## [0.1.0] - 2017-09-13
- Alpha release.


## [0.0.4] - 2017-09-13
### Added
-  List_Repo function.

### Changed
- main:  Add -R -> list repositories option.


## [0.0.3] - 2017-09-12
### Changed
- Initate_Dump:  Recode check on dump status.
- main:  Add -L -> list dumps option.

### Added
- List_Dump function.


## [0.0.2] - 2017-09-11
- Correction to first testing cycle.

### Changed
- Add main option argument ability to call different options.

### Added
- Initate_Dump function
- Print_Failures function


## [0.0.1] - 2017-09-05
- Pre-Alpha release.

