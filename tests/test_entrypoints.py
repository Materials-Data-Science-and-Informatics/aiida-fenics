# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c), Forschungszentrum Jülich GmbH, IAS-9, Germany.               #
#                All rights reserved.                                         #
# This file is part of the aiida-fenics package.                              #
#                                                                             #
# The code is hosted on GitHub at                                             #
# https://github.com/Materials-Data-Science-and-Informatics/aiida-fenics      #
# For further information on the license, see the LICENSE file                #
# http://aiida-fenics.readthedocs.io/en/develop/                              #
###############################################################################
''' Contains smoke tests for all aiida-pfdisloc entry points '''
# pylint: disable=import-outside-toplevel
# pylint: disable=no-self-use

import pytest

from aiida.plugins import CalculationFactory
from aiida.plugins import ParserFactory


@pytest.mark.usefixtures('aiida_profile', 'clear_database')
class TestPluginEntrypoints:
    """
    tests all the entry points of the plugin. Therefore if the plugin is
    recognized by AiiDA and installed right.
    """

    # Calculations

    def test_pfdisloc_calculation_entry_point(self):
        """Test if the entry point fenics.pfdisloc can be loaded"""
        calculation = CalculationFactory('fenics.pfdisloc')
        assert calculation is not None

    # Data

    #def test_meshdata_entry_point(self):
    #    from aiida.plugins import DataFactory
    #    from aiida_pfdisloc.data.mesh import FEMMeshData
    #
    #    mesh = DataFactory('fenics.fem_mesh')
    #    assert mesh == FEMMeshData

    # Parsers

    def test_pfdisloc_parser_entry_point(self):
        """Test if the entry point fenics.pfdislocparser can be loaded"""
        from aiida_fenics.parsers.pfdisloc import PfdislocParser

        parser = ParserFactory('fenics.pfdislocparser')
        assert parser == PfdislocParser
