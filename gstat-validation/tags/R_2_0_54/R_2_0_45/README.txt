Application:  BDII Info Testing
Authors:      David.Horat@cern.ch
Version:      0.1 (XX/03/2010)
********************************************************************

DESCRIPTION
This application allows system administrators and developers to validate LDAP
information content against concrete profiles. Right now the only profile
implemented is GLUE 2.0, but it is easy to extend it to others.


USAGE
There are several ways to use this application:
- You can run the main script, ./bdii-info-testing.py
- You can run individual tests.

The same interface applies too all tests, so you can run the script without
arguments for help if needed.


CORE STRUCTURE
  bdii-info-testing.py          The main script to invoke
  README.txt                    This file
  __init__.py                   Python file to add this directory as a module
  lib/                          Directory containing auxiliary functions
    __init__.py                 Python file to add this directory as a module
    testingutils.py             Functions to connect to LDAP, configure, etc.
    UnitTest.py                 Main class to inherit from for other tests


MODULE STRUCTURE
  [name]/
    [name]DataLib.py            Library for data type checking
    [name]UnitTest.py           Class to inherit from (from UnitTest.py)
    *Test.py                    Tests
    tests/                      Directory containing tests for this module
      [name]DataLibTest.py      Tests for the library for data checking


TODO
There are several improvements that could be done:
- Package it into several RPMs (one for core and one per module)

Do you have more suggestions?
Send us an email to: project-grid-info-support@cern.ch


CHANGELOG

