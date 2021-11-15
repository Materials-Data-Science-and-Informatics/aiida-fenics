# Enabling usage of the FEniCS computing platform with AiiDA

[![MIT license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GitHub release](https://img.shields.io/github/release/Materials-Data-Science-and-Informatics/aiida-fenics.svg)](https://github.com/Materials-Data-Science-and-Informatics/aiida-fenics/releases)
[![PyPI version](https://badge.fury.io/py/aiida-fenics.svg)](https://badge.fury.io/py/aiida-fenics)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/aiida-fenics.svg)](https://pypi.python.org/pypi/aiida-fenics)
[![Build status](https://github.com/Materials-Data-Science-and-Informatics/aiida-fenics/workflows/aiida-fenics-ci/badge.svg)](https://github.com/Materials-Data-Science-and-Informatics/aiida-fenics/actions)
[![Documentation Status](https://readthedocs.org/projects/aiida-fenics/badge/?version=develop)](https://aiida-fenics.readthedocs.io/en/develop/?badge=develop)
[![codecov](https://codecov.io/gh/Materials-Data-Science-and-Informatics/aiida-fenics/branch/develop/graph/badge.svg)](https://codecov.io/gh/Materials-Data-Science-and-Informatics/aiida-fenics)


This software contains a plugins that enables the usage of the FENiCS computing platform with the [AiiDA framework](http://www.aiida.net). It includes special plugins for software building on FENiCs like the Phasefield dislocation interaction program Pdfdisloc. The enables provenance tracking for such simulations and workflows, which is need for research datamanagement, reproducibility and FAIR data.

### Documentation

Hosted at http://aiida-fenics.readthedocs.io/en/develop/index.html.
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

From the aiida-fenics folder (after downloading the code, recommended) use:

    $ pip install .
    # or which is very useful to keep track of the changes (developers)
    $ pip install -e .

To uninstall use:

    $ pip uninstall aiida-fenics

Or install latest release version from pypi:

    $ pip install aiida-fenics

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
   * fenics.dfdisloc
```
You should see 'fenics.*' in the list

The other entry points can be checked with the AiiDA Factories (Data, Workflow, Calculation, Parser).
(this is done in test_entry_points.py)

We suggest to run all the (unit)tests in the aiida-fleur/aiida_fleur/tests/ folder.

    $ bash run_all_cov.sh

___

## Code Dependencies <a name="Dependencies"></a>

Requirements are listed in setup.json.

most important are:

* aiida_core >= 1.3.0

Mainly AiiDA:

1. Download from [www.aiida.net -> Download](www.aiida.net)
2. install and setup -> [aiida's documentation](http://aiida-core.readthedocs.org/en/stable)


## Further Information <a name="FurtherInfo"></a>

Usage examples are shown in 'examples'.


## Acknowledgements

Besides the Forschungszentrum Juelich GmbH (FZJ), this project was supported within the hub Information at the FZJ by the Helmholtz Metadata Collaboration (HMC), an incubator-platform of the Helmholtz Association within the framework of the Information and Data Science strategic initiative.
