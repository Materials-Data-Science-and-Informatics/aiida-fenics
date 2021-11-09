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
"""
A parser parsing pdfdisloc output files, to store in the database.

"""
from aiida.engine import ExitCode
from aiida.parsers.parser import Parser
from aiida.plugins import CalculationFactory
from aiida.common import exceptions

PfdislocCalculation = CalculationFactory('fenics.pfdisloc')


class PfdislocParser(Parser):
    """
    Parser class for parsing output of a Pfdisloc calculation.
    """
    def __init__(self, node):
        """
        Initialize Parser instance

        Checks that the ProcessNode being passed was produced by a PfdislocCalculation.

        :param node: ProcessNode of calculation
        :param type node: :class:`aiida.orm.ProcessNode`
        """
        super().__init__(node)
        if not issubclass(node.process_class, PfdislocCalculation):
            raise exceptions.ParsingError('Can only parse PfdislocCalculation')

    def parse(self, **kwargs):
        """
        Parse outputs, store results in database.

        :returns: an exit code, if parsing fails (or nothing if parsing succeeds)
        """

        # Create Stress Array output data

        # Create Stress Trajectory output data

        return ExitCode(0)
