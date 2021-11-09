# -*- coding: utf-8 -*-
''' Contains smoke tests for all aiida-pfdisloc entry points '''
import pytest


@pytest.mark.usefixtures('aiida_profile', 'clear_database')
class TestPluginEntrypoints:
    """
    tests all the entry points of the plugin. Therefore if the plugin is
    recognized by AiiDA and installed right.
    """

    # Calculations

    def test_pfdisloc_calculation_entry_point(self):
        from aiida.plugins import CalculationFactory
        
        calculation = CalculationFactory('fenics.pfdisloc')
        assert fleur_calculation is not None

    # Data

    #def test_meshdata_entry_point(self):
    #    from aiida.plugins import DataFactory
    #    from aiida_pfdisloc.data.mesh import FEMMeshData
    #
    #    mesh = DataFactory('fenics.fem_mesh')
    #    assert mesh == FEMMeshData

    # Parsers

    def test_pfdisloc_parser_entry_point(self):
        from aiida.plugins import ParserFactory
        from aiida_pfdisloc.parsers.pfdisloc import PfdislocParser

        parser = ParserFactory('fenics.pfdislocparser')
        assert parser == PfdislocParser

