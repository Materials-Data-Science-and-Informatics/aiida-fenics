# -*- coding: utf-8 -*-
"""
A parser parsing pdfdisloc output files, to store in the database.

"""
from aiida.engine import ExitCode
from aiida.parsers.parser import Parser
from aiida.plugins import CalculationFactory
from aiida.common import exceptions
from aiida import orm

PdfdislocCalculation = CalculationFactory("pdfdisloc")


class PdfdislocParser(Parser):
    """
    Parser class for parsing output of a Pdfdisloc calculation.
    """

    def __init__(self, node):
        """
        Initialize Parser instance

        Checks that the ProcessNode being passed was produced by a PdfdislocCalculation.

        :param node: ProcessNode of calculation
        :param type node: :class:`aiida.orm.ProcessNode`
        """
        super().__init__(node)
        if not issubclass(node.process_class, PdfdislocCalculation):
            raise exceptions.ParsingError("Can only parse PdfdislocCalculation")

    def parse(self, **kwargs):
        """
        Parse outputs, store results in database.

        :returns: an exit code, if parsing fails (or nothing if parsing succeeds)
        """

        # Create Stress Array output data

        # Create Stress Trajectory output data
        """
        output_filename = self.node.get_option("output_filename")

        # Check that folder content is as expected
        files_retrieved = self.retrieved.list_object_names()
        files_expected = [output_filename]
        # Note: set(A) <= set(B) checks whether A is a subset of B
        if not set(files_expected) <= set(files_retrieved):
            self.logger.error(
                "Found files '{}', expected to find '{}'".format(
                    files_retrieved, files_expected
                )
            )
            return self.exit_codes.ERROR_MISSING_OUTPUT_FILES

        # add output file
        self.logger.info("Parsing '{}'".format(output_filename))
        with self.retrieved.open(output_filename, "rb") as handle:
            output_node = orm.SinglefileData(file=handle)
        self.out("{{cookiecutter.entry_point_prefix}}", output_node)
        """
        return ExitCode(0)
