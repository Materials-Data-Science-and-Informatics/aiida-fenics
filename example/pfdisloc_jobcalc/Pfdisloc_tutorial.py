#!/usr/bin/env python
# coding: utf-8

# # Tutorial Notebook to run a Pfdisloc simulation job

# In[ ]:


# prior to this you need


# In[ ]:


# imports, we have to load the aiida db environment
from aiida import load_profile
load_profile()


# In[ ]:

import yaml
from aiida.orm import load_code
from aiida.engine import run, submit
from aiida import orm
from aiida.plugins import CalculationFactory


# In[ ]:


PdfdislocCalculation = CalculationFactory('fenics.pfdisloc')


# # Basic stuff, prior

# check the setup and if the daemon is running

# In[ ]:


#get_ipython().system('verdi status')


# In[ ]:


#get_ipython().system('verdi daemon status')


# check what codes are setup in your database

# In[ ]:


#get_ipython().system('verdi code list -a')


# In[ ]:


# prior to this you need to have setup a code in you data base with the label 'pdfdisloc_0_1_0' and a computer in this case 'jureca'
# How to do this is described here: https://aiida.readthedocs.io/projects/aiida-core/en/latest/howto/run_codes.html
# Also see example, jureca setup
# If you want to run the code on a different computer or version you have to set it up and change the label below
code = load_code('pfdisloc_0_1_0@localhost')


# # Preparing the inputs

# In[ ]:


config_filepath = './pf_penny_shaped_crack.yaml'
model_filepath = './martensite_seed.py'


# In[ ]:
with open(config_filepath, 'r') as fileo:
    config_dict = yaml.load(fileo)

print(config_dict)

# create a nodes, these are not yet stored in the database, but will be on input into a calculations
config_para_node = orm.Dict(config_dict)
model = orm.SingleFileData(model_filepath)
inputs = {'code': code, 'config' : config_para_node, 'model': model}


# In[ ]:


# this would run with default metadata and resources, which depending on the machine does not work
# also see https://aiida.readthedocs.io/projects/aiida-core/en/latest/topics/schedulers.html?highlight=metadata.options%20#job-resources
# and https://aiida.readthedocs.io/projects/aiida-core/en/latest/topics/calculations/usage.html?highlight=options#options
# for jureca for example you would like to do, the environment should be setup with the code, i.e it should not be loaded here...
resources = {'withmpi': True, 'num_machines':1, 'num_mpiprocs_per_machine':128}
options = {'resource': resources, 'custom_scheduler_commands' : '#SBATCH --account=ias-9', 'max_wallclock_seconds' : 5*60, 'queue_name' : 'dc-cpu'}

metadata = {'label': 'My first Pfdislocjob', 'description': 'Really awesome calculation, which leads to a PhD', 'options': options}
inputs['metadata'] = metadata
inputs_dry_run = inputs
inputs_dry_run['metadata']['dry-run'] = True


# # Launching the job

# first we do a tryrun to check if all files and jobscripts are right

# In[ ]:


pfdiscal = submit(PdfdislocCalculation, **inputs_dry_run)


# In[ ]:


# This will had the job to the AiiDA daemon which will run it through, i.e submit it on the computer and retrieve results
#pfdiscal = submit(PdfdislocCalculation, **inputs)


# In[ ]:


#get_ipython().system('verdi process list -a')


# In[ ]:


# one can also run the job in the python interpretor in a blocking way and not hand it to the AiiDA daemon, i.e. it is blocked until the job is done and retrieved.


# In[ ]:


#res = run(PdfdislocCalculation, **inputs)


# # Alternative way, using a builder

# Every process in aiida has a builder, which provides you with a more interactive way to do this above, without knowing all the details, so it is more 'userfiendly', since you do not need to know form where to import the calculation, or what the entry point is called to use the Factories. The builder also provides interactive help on inputs.

# In[ ]:


#pfdiscal_builder = code.get_builder()
#pfdiscal_builder.config = config_para_node
#pfdiscal_builder.model = model_file
#pfdiscal_builder.metadata.description ='My first pfdiscal simulation through a builder.'
#pfdiscal_builder.metadata.resource = resource
#pfdiscal_builder.metadata.options = options


# In[ ]:


#submit(pfdiscal_builder)

