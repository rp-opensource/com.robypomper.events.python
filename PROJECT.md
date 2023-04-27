# `rp.events` project

## Development environment

Preferred machine for develop this project is a Linux machine. This is because
some tools (like clean.sh or test.sh) are only available for bash shell. \
Anyway, you can install the WindowsLinuxSubsystems package for Windows or use
the Bash shell provided by the macOS. \
All other development commands and tools are based on Python so they can be
used across different platforms.

To obtain this project, you must use git and clone this repository. First of all
[download and install git](https://git-scm.com/downloads). Then clone the repository
on your machine.

```shell
$ git clone https://github.com/rp-opensource/com.robypomper.events.python
$ cd com.robypomper.events.python
$ git switch master
```

This project is based on Python, so you'll need to install the Python interpreter.
You can download it from the [Python website](https://www.python.org/downloads/)
or install with your package manager, here an example for ubuntu:

```shell
$ sudo apt-get install python3 python3-dev python3-venv
```

Now you are able to create the [Python Virtual Environment](https://python.land/virtual-environments/virtualenv)
to use for this project. Simply, run following command from the main project
directory. \
After that, you'll get a new and activated virtual environment. Next time, you'll
need only to activate it.

```shell
$ python -m venv venv           # Create the venv
$ venv\Scripts\activate.bat       # Activate in cmd.exe
$ venv\Scripts\Activate.ps1       # Activate in PowerShell
$ source venv/bin/activate        # Activate in Linux/MacOS
(venv)$ _
```

Finally, install the project's (as editable module), his dependencies and all
Python modules required to develop, test and build the project.

```shell
(venv)$ pip install -e .[dev,test]
```

This command, install the project sources as an editable module into the current
venv, so they can be available for test sources. Then, with the `[dev,test]` option,
the previous command install also all optional dependencies specified into the
`[project.optional-dependencies]` field from the `pyproject.toml` file.

---

## Build system

The build system of this project use the `pyproject.toml` file to declare project
meta-data like name, version, urls... but also to specify his dependencies and
the test framework.

If you didn't do that, you must install the development dependencies into the
virtual environment. Following command will install all modules listed into
the `[project.optional-dependencies].dev` field from the `pyproject.toml` file.

```shell
(venv)$ pip install -e .[dev]
```

Next, you can build the project. \
Always from the venv, run the command below to build the source and wheel
distributions into the `dist` directory.

```shell
(venv)$ python -m build
```

---

## Tools

This project provide also some tool to do regular operations on the project
files like clean temporary files or execute test in specific environments.

* [clean.sh](scripts/clean.sh): remove all temporary files generate during builds or executions.
* [test.sh](scripts/test.sh): execute project tests using a specific Python version.

More info on those tools can be found on the corresponding scripts. Any script
is documented with usage, params and examples.

---

## User configs

This is a software library so it dose not require any configuration from the
end user.

---

## Tests

TODO: ...
    execution with cmds
    write: conventions
                
                Activate the `venv` and execute the pytest.
                
                ```shell
                # In cmd.exe
                venv\Scripts\activate.bat
                # In PowerShell
                venv\Scripts\Activate.ps1
                # In Linux/MacOS
                source venv/bin/activate
                pytest
                ```

---

## Documentation

TODO: ...
  read: where to find
  write: conventions

---

## Guidelines

TODO: ...
    

---

## Publication flow

TODO: ...
  0 release branch
  1 build
  2 test
  3 publish on test repo
  4 install and test from test repo
  5 publish on repo

                https://github.com/bast/pypi-howto/blob/master/README.md
                create `~/.pypirc` file
                
                ```sh
                python -m build
                tar tf dist/*.tar.gz
                
                python setup.py sdist
                twine upload dist/* -r pypitest
                ```

---

## Common commands

### End user

In this case the End user is the developer that include the 'rp.events' module.
So, he just needs to install the module from the PyPI repository.

* Install rp.events from pypi
  ```shell
  pip install rp.events
  ```

### Developer

Development is based on venvs. So, 'rp.events' developers must activate the venv
for any development session. After that, they can execute any development command.

* Activate venv (if not already done):
  ```script
  venv\Scripts\activate.bat       # cmd.exe
  venv\Scripts\Activate.ps1       # PowerShell
  source venv/bin/activate        # Linux/MacOS
  ```
* Execute rp.events tests:
  ```shell
  (venv)$ pytest
  ```
* Build rp.events:
  ```shell
  (venv)$ python -m build
  (venv)$ tar tf dist/*.tar.gz
  ```
* Publish rp.events distribution to pypitest (works only with ~/.pypirc file configured): \
  ```shell
  (venv)$ twine upload dist/* -r pypitest           # publish on pypitest
  (venv)$ twine upload dist/*                       # publish on pypi
  ```

### Setup development environment

This project is based on Python, so first of all, please install the Python
interpreter and his tools or updated them to the latest version.
Then, for any venv created, developers must install project dev and test
dependencies.

* Install latest python:
  ```shell
  $ sudo apt install python
  ```
* Install specific version of python from the `deadsnakes/ppa` repository:
  ```shell
  $ sudo apt install software-properties-common
  $ sudo add-apt-repository ppa:deadsnakes/ppa
  $ sudo apt update
  $ sudo apt install python3.7 python3.7-distutils
  ```
* Update pip and virtualenv \
  ```shell
  $ python -m pip install --upgrade pip`
  $ pip install --upgrade virtualenv
  ```
* Create venv:
  ```shell
  $ python -m venv venv
  $ python -m venv --p 3.5 venv-3.5
  $ virtualenv  --python=/usr/bin/python3.7 venvs/3.7
  ```
* Activate venv:
  ```shell
  $ venv\Scripts\activate.bat       # cmd.exe
  $ venv\Scripts\Activate.ps1       # PowerShell
  $ source venv/bin/activate        # Linux/MacOS
  ```
*  Install 'rp.events' from local source with dev and test dependencies: \
  ```shell
  (venv)$ pip install -e .[dev,test]
  ```
