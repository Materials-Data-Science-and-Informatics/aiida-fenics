#!/usr/bin/env sh
export AIIDA_PATH='.';
mkdir -p '.aiida';
#pytest -sv
#pytest -v
pytest --cov-report=xml --cov=aiida_fenics --cov=tests

# to create badge (requires coverage-badge)
#coverage-badge -o coverage.svg

# pylint (for shield create, by hand, or write script to write total into svg) 
# pylint ../../aiida_fleur/ > outlint
