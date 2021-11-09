#!/usr/bin/env python
# coding: utf-8

# # Tutorial Notebook to run a Pfdisloc simulation job

# imports, we have to load the aiida db environment
from aiida import load_profile
load_profile()

import os
import yaml
from aiida.orm import load_code
from aiida.engine import run, submit
from aiida import orm
from aiida.plugins import CalculationFactory
from pprint import pprint

PfdislocCalculation = CalculationFactory('fenics.pfdisloc')


# prior to this you need to have setup a code in you data base with the label 'pdfdisloc_0_1_0' and a computer in this case 'jureca'
# How to do this is described here: https://aiida.readthedocs.io/projects/aiida-core/en/latest/howto/run_codes.html
# Also see example, jureca setup
# If you want to run the code on a different computer or version you have to set it up and change the label below
code = load_code('pfdisloc_0_1_0@localhost')

config_filepath = './pf_penny_shaped_crack.yaml'
model_filepath = os.path.abspath('./martensite_seed.py')

with open(config_filepath, 'r') as fileo:
    config_dict = yaml.load(fileo, Loader=yaml.SafeLoader)

pprint(config_dict)

# create a nodes, these are not yet stored in the database, but will be on input into a calculations
config_para_node = orm.Dict(dict=config_dict)
model = orm.SinglefileData(model_filepath)
inputs = {'code': code, 'config' : config_para_node, 'model': model}

# this would run with default metadata and resources, which depending on the machine does not work
# also see https://aiida.readthedocs.io/projects/aiida-core/en/latest/topics/schedulers.html?highlight=metadata.options%20#job-resources
# and https://aiida.readthedocs.io/projects/aiida-core/en/latest/topics/calculations/usage.html?highlight=options#options
# for jureca for example you would like to do, the environment should be setup with the code, i.e it should not be loaded here...
resources = {'num_machines':1, 'num_mpiprocs_per_machine':2}
options = {'withmpi': True, 'resources': resources, 'account' : 'ias-9', 'max_wallclock_seconds' : 5*60, 'queue_name' : 'dc-cpu'}

metadata = {'label': 'My first Pfdislocjob', 'description': 'Really awesome calculation, which leads to a PhD', 'options': options}
inputs['metadata'] = metadata
inputs_dry_run = inputs
inputs_dry_run['metadata']['dry_run'] = True

# # Launching the job

# first we do a tryrun to check if all files and jobscripts are right
pfdiscal = submit(PfdislocCalculation, **inputs_dry_run)

# This will had the job to the AiiDA daemon which will run it through, i.e submit it on the computer and retrieve results
#pfdiscal = submit(PfdislocCalculation, **inputs)


# one can also run the job in the python interpretor in a blocking way and not hand it to the AiiDA daemon, i.e. it is blocked until the job is done and retrieved.

#res = run(PfdislocCalculation, **inputs)

# # Alternative way, using a builder

# Every process in aiida has a builder, which provides you with a more interactive way to do this above, without knowing all the details, so it is more 'userfiendly', since you do not need to know form where to import the calculation, or what the entry point is called to use the Factories. The builder also provides interactive help on inputs.

#pfdiscal_builder = code.get_builder()
#pfdiscal_builder.config = config_para_node
#pfdiscal_builder.model = model_file
#pfdiscal_builder.metadata.description ='My first pfdiscal simulation through a builder.'
#pfdiscal_builder.metadata.resources = resources
#pfdiscal_builder.metadata.options = options

#submit(pfdiscal_builder)
