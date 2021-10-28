# Phasefield dislocation interaction simulations with AiiDA

[![MIT license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GitHub release](https://img.shields.io/github/release/broeder-j/aiida-pdfdisloc.svg)](https://github.com/broeder-j/aiida-pdfdisloc/releases)
[![PyPI version](https://badge.fury.io/py/aiida-pdfdisloc.svg)](https://badge.fury.io/py/aiida-pdfdisloc)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/aiida-pdfdisloc.svg)](https://pypi.python.org/pypi/aiida-pdfdisloc)
[![Build status](https://github.com/broeder-j/aiida-pdfdisloc/workflows/aiida-pdfdisloc/badge.svg?branch=develop&event=push)](https://github.com/broeder-j/aiida-pdfdisloc/actions)
[![Documentation Status](https://readthedocs.org/projects/aiida-pdfdisloc/badge/?version=develop)](https://aiida-pdfdisloc.readthedocs.io/en/develop/?badge=develop)
[![codecov](https://codecov.io/gh/broeder-j/aiida-pdfdisloc/branch/develop/graph/badge.svg)](https://codecov.io/gh/broeder-j/aiida-pdfdisloc)


This software contains a plugin that enables the usage of the Phasefield dislocation interaction program Pdfdisloc with the [AiiDA framework](http://www.aiida.net).

### Documentation

Hosted at http://aiida-pdfdisloc.readthedocs.io/en/develop/index.html.
For other information see the AiiDA-core docs, or the FeniCs project.

### License:

MIT license.
See the license file.

### How to cite:
If you use this package please consider citing:
```
```


### Comments/Disclaimer:


### Contents

1. [Introduction](#Introduction)
2. [Installation Instructions](#Installation)
3. [Code Dependencies](#Dependencies)
4. [Further Information](#FurtherInfo)

## Introduction <a name="Introduction"></a>

This is a python package (AiiDA plugin and utility)
allowing to use the pdfdisloc code in the AiiDA Framework.
The Pdfdisloc program contains workflows based on Fenics a finite element solver,
that is widely applied in the material science and physics community.

### The plugin :

The plugin consists of:

    1. A data-structure representing Meshes.
    2. pdfdisloc calculation


## Installation Instructions <a name="Installation"></a>

From the aiida-pdfdisloc folder (after downloading the code, recommended) use:

    $ pip install .
    # or which is very useful to keep track of the changes (developers)
    $ pip install -e .

To uninstall use:

    $ pip uninstall aiida-pdfdisloc

Or install latest release version from pypi:

    $ pip install aiida-pdfdisloc

### Test Installation
To test rather the installation was successful use:
```bash
$ verdi plugins list aiida.calculations
```
```bash
   # example output:

   ## Pass as a further parameter one (or more) plugin names
   ## to get more details on a given plugin.
   ...
   * dfdisloc.dfdisloc
```
You should see 'dfdisloc.*' in the list

The other entry points can be checked with the AiiDA Factories (Data, Workflow, Calculation, Parser).
(this is done in test_entry_points.py)

We suggest to run all the (unit)tests in the aiida-fleur/aiida_fleur/tests/ folder.

    $ bash run_all_cov.sh

___

## Code Dependencies <a name="Dependencies"></a>

Requirements are listed in 'setup_requirements.txt' and setup.json.

most important are:

* aiida_core >= 1.0.1

Mainly AiiDA:

1. Download from [www.aiida.net -> Download](www.aiida.net)
2. install and setup -> [aiida's documentation](http://aiida-core.readthedocs.org/en/stable)


## Further Information <a name="FurtherInfo"></a>

Usage examples are shown in 'examples'.


## Acknowledgements

Besides the Forschungszentrum Juelich, this work is supported by the [MaX



