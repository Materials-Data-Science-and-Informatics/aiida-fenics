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
Calculation plugin for a basic pfdisloc calculations
"""
# pylint: disable=too-many-locals

import os
import yaml
from aiida import orm
from aiida.common import datastructures
from aiida.engine import CalcJob

# from aiida.plugins import DataFactory


class PfdislocCalculation(CalcJob):
    """
    AiiDA calculation plugin wrapping a pfdisloc simulation.

    """

    _CONFIG_FILE_NAME = 'config.yaml'
    #_STRESS_FILE_NAME = ""
    #_STRAIN_FILE_NAME = ""
    #_STRESS_TRAJECTORY_FILE_NAME = ""
    _DISLOCATION_TRACE_FILE_NAME_H = 'dislocation_trace.h5'
    _DISLOCATION_TRACE_FILE_NAME = 'dislocation_trace.xdmf'
    _ORDER_PARAMETER_FILE_NAME_H = 'order_parmeter.h5'
    _ORDER_PARAMETER__FILE_NAME = 'order_parameter.xdmf'
    _ENVIRONMENT_FILE_NAME = 'pip_python_env.txt'

    @classmethod
    def define(cls, spec):
        """Define inputs and outputs of the calculation."""
        super().define(spec)

        # set default values for AiiDA options
        spec.inputs['metadata']['options']['resources'].default = {
            'num_machines': 1,
            'num_mpiprocs_per_machine': 1,
        }
        spec.inputs['metadata']['options'][
            'parser_name'].default = 'fenics.pfdislocparser'

        # new ports
        spec.input(
            'config',
            valid_type=orm.Dict,
            help='A dictionary, representing the yaml config file.',
        )
        spec.input(
            'code',
            valid_type=orm.Code,
            help=(
                'A AiiDA code node, connected to a computer containing all the '
                'environment setup to execute the model file with python.'),
        )
        spec.input(
            'model',
            valid_type=orm.SinglefileData,
            help='A python file containing the model to solve.',
            required=False,
        )
        spec.input(
            'mesh',
            valid_type=orm.SinglefileData,
            help='A dump of a pdfdisloc mesh to be used.',
            required=False,
        )
        spec.output(
            'stress',
            valid_type=orm.ArrayData,
            required=False,
            help='Stresses of last time step, or the single shot calculation..',
        )
        spec.output(
            'stress_trajectory',
            valid_type=orm.TrajectoryData,
            required=False,
            help=
            'If a time depended simulations, a trajectory will be returned.',
        )

        spec.exit_code(
            300,
            'ERROR_MISSING_OUTPUT_FILES',
            message='Calculation did not produce all expected output files.',
        )

    def prepare_for_submission(self, folder):
        """
        Create input files.

        :param folder: an `aiida.common.folders.Folder` where the plugin
            should temporarily place all files needed by the calculation.
        :return: `aiida.common.datastructures.CalcInfo` instance
        """

        # Notice we do not enforce here the names but reuse the file names from the given input.
        # for flexibility, but might lead to user errors.
        local_copy_list = []
        if 'model' in self.inputs:
            model_file_name = self.inputs.model.filename
            local_copy_list.append(
                (self.inputs.model.uuid, model_file_name, model_file_name))
        else:
            model_file_name = 'martensite_seed.py'

        if 'mesh' in self.inputs:
            mesh_file_name = self.inputs.mesh.filename
            local_copy_list.append(
                (self.inputs.mesh.uuid, mesh_file_name, mesh_file_name))

        # copy model file from Single file data

        # write config yaml file from dict
        config = self.inputs.config.get_dict()
        config_filepath = folder.get_abs_path(self._CONFIG_FILE_NAME)
        with open(config_filepath, 'w') as file_o:
            yaml.dump(config,
                      stream=file_o,
                      default_flow_style=False,
                      sort_keys=False)

        path_prefix = config.get('output', {}).get('path', '')
        retrieve_list = [
            #self._STRESS_FILE_NAME,
            #self._STRAIN_FILE_NAME,
            #self._STRESS_TRAJECTORY_FILE_NAME,
            os.path.join(path_prefix, self._DISLOCATION_TRACE_FILE_NAME_H),
            os.path.join(path_prefix, self._DISLOCATION_TRACE_FILE_NAME),
            os.path.join(path_prefix, self._ORDER_PARAMETER_FILE_NAME_H),
            os.path.join(path_prefix, self._ORDER_PARAMETER__FILE_NAME),
            self._ENVIRONMENT_FILE_NAME
        ]

        codeinfo = datastructures.CodeInfo()
        codeinfo.code_uuid = self.inputs.code.uuid
        cmdline_params = [
            f'{model_file_name}', '-c', '{}'.format(self._CONFIG_FILE_NAME)
        ]
        # for command in settings_dict.get('cmdline', []):
        #        cmdline_params.append(command)
        codeinfo.cmdline_params = list(cmdline_params)
        # codeinfo.stdout_name = self.metadata.options.output_filename
        # codeinfo.stdout_name = self._SHELLOUT_FILE_NAME
        # codeinfo.stderr_name = self._ERROR_FILE_NAME

        codeinfo.withmpi = self.inputs.metadata.options.withmpi

        # Prepare a `CalcInfo` to be returned to the engine
        calcinfo = datastructures.CalcInfo()
        calcinfo.codes_info = [codeinfo]
        calcinfo.local_copy_list = local_copy_list
        calcinfo.retrieve_list = []
        for file_ in retrieve_list:
            calcinfo.retrieve_list.append(file_)

        # prepend text to output environment
        cmd = f'\npip freeze > {self._ENVIRONMENT_FILE_NAME}'
        prepend_text = calcinfo.prepend_text
        if prepend_text is None:
            prepend_text = cmd
        else:
            prepend_text += cmd
        calcinfo.prepend_text = prepend_text

        return calcinfo
