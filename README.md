# EOEPCA System Test Suite

## Test suite execution

The test suite is configured by environment variables that are defined in the file `.env`.

The test suite is invoked by...

```bash
pytest test -v
```

## Environment tailoring

The contents of `.env` can be regarded as a base set, which can be overridden with values tailored for a specific test target system - via the additional file `.env.<target>`.

The target test system is then selected by invoking `pytest` with the variable `target` set.

For example, the test suite is invoked for the `prod` test target by...

```bash
target=prod pytest test -v
```

...which will take the test configuration from combination of the files `.env` and `.env.prod`.

## Python environment

The python library dependencies required to run the test suite are specified in the `requirements.txt` file - for installation via `pip`...

```bash
pip install -r requirements.txt
```

It is recommended to use a python virtual environment for the execution of the test suite...

```bash
python -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

## HTML Report

An HTML test report can be obtained...

```bash
target=dev pytest test --html=report.html -v

# open report in browser
xdg-open report.html
```
