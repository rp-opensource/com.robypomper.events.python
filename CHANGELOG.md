# `rp.events` changelog

## Version 0.0.1

### Source code
* Added the Events module (events.py and __init__.py) into src/rp/events
* Added the __init__.py file for namespace package into src/rp
  https://stackoverflow.com/questions/2699287/what-is-path-useful-for
* Created an empty requirements.txt

### Tests
* Added unit tests for the Events module
* Added pytest and pytest-cov as "test" dependency

### Examples
* Added events_register_methods.py
* Added events_with_decorators.py

### Docs
* Added README.md and README_pypi.md files
* Added "Apache License, Version 2.0" LICENCE file
  * Added PROJECT.md, CHANGELOG.md, TODOs.md and ROADMAP.md

### Project
* Added pyproject.toml based on setuptools
* Added project meta-data to project.toml
* Added project version "0.0.1" to project.toml
* Added pip and build as "dev" dependency
* Added setuptools and twine as "dev" dependency
* Added .gitignore file from https://www.toptal.com/developers/gitignore/api/python

### Tools
* Added script test.sh to run tests into a generated venvs
* Added script clean.sh to remove any generated/temporary file
