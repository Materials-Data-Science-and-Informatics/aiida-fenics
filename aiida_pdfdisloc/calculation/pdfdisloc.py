# -*- coding: utf-8 -*-
"""
Calcuation plugin for a basic pdfdisloc calculatons
"""
import yaml
from aiida import orm
from aiida.common import datastructures
from aiida.engine import CalcJob

# from aiida.plugins import DataFactory


class PdfdislocCalculation(CalcJob):
    """
    AiiDA calculation plugin wrapping the pdfdisloc executable.

    """

    _CONFIG_FILE_NAME = "config.yaml"
    _STRESS_FILE_NAME = ""
    _STRAIN_FILE_NAME = ""
    _STRESS_TRAJECTORY_FILE_NAME = ""

    @classmethod
    def define(cls, spec):
        """Define inputs and outputs of the calculation."""
        super().define(spec)

        # set default values for AiiDA options
        spec.inputs["metadata"]["options"]["resources"].default = {
            "num_machines": 1,
            "num_mpiprocs_per_machine": 1,
        }
        spec.inputs["metadata"]["options"]["parser_name"].default = "pdfdisloc"

        # new ports
        spec.input(
            "config",
            valid_type=orm.Dict,
            help="A dictionary, representing the yaml config file.",
        )
        spec.input(
            "code",
            valid_type=orm.Code,
            help="A AiiDA code node, connected to a computer containing all the environment setup to execute the model file with python.",
        )
        spec.input(
            "model",
            valid_type=orm.SinglefileData,
            help="A python file containing the model to solve.",
        )
        spec.input(
            "mesh",
            valid_type=orm.SinglefileData,
            help="A dump of a pdfdisloc mesh to be used.",
            required=False,
        )
        spec.output(
            "stress",
            valid_type=orm.ArrayData,
            help="Stresses of last time step, or the single shot calculation..",
        )
        spec.output(
            "stress_trajectory",
            valid_type=orm.TrajectoryData,
            required=False,
            help="If a time depended simulations, a trajectory will be returned.",
        )

        spec.exit_code(
            300,
            "ERROR_MISSING_OUTPUT_FILES",
            message="Calculation did not produce all expected output files.",
        )

    def prepare_for_submission(self, folder):
        """
        Create input files.

        :param folder: an `aiida.common.folders.Folder` where the plugin should temporarily place all files
            needed by the calculation.
        :return: `aiida.common.datastructures.CalcInfo` instance
        """
        retrieve_list = [
            self._STRESS_FILE_NAME,
            self._STRAIN_FILE_NAME,
            self._STRESS_TRAJECTORY_FILE_NAME,
        ]

        # Notice we do not enforce here the names but reuse the file names from the given input.
        # for flexibility, but might lead to user errors.
        local_copy_list = []
        model_file_name = self.input.model.file
        local_copy_list.append(
            (self.input.model.uuid, model_file_name, model_file_name)
        )

        if "mesh" in self.inputs:
            mesh_file_name = self.input.mesh.file
            local_copy_list.append(
                (self.input.mesh.uuid, mesh_file_name, mesh_file_name)
            )

        # copy model file from Single file data

        # write config yaml file from dict
        config = self.inputs.config
        config_filepath = folder.get_abs_path(self._CONFIG_FILE_NAME)
        with open(config_filepath, "w") as file_o:
            config = yaml.dump(
                config, stream=file_o, default_flow_style=False, sort_keys=False
            )

        codeinfo = datastructures.CodeInfo()
        codeinfo.code_uuid = self.inputs.code.uuid
        cmdline_params = ["-c", "{}".format(self._CONFIG_FILE_NAME)]
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

        return calcinfo
