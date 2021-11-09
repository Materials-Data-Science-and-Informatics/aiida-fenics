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
aiida-fenics
"""

import click
import click_completion
from aiida.cmdline.params import options, types
from aiida_fenics import __version__

# Activate the completion of parameter types provided by the click_completion package
# for bash: eval "$(_AIIDA_FLEUR_COMPLETE=source aiida-fenics)"
click_completion.init()

# Instead of using entrypoints and directly injecting verdi commands into aiida-core
# we created our own separete CLI because verdi will prob change and become
# less material science specific


@click.group('aiida-fenics',
             context_settings={'help_option_names': ['-h', '--help']})
@options.PROFILE(type=types.ProfileParamType(load_profile=True))
# Note, __version__ should always be passed explicitly here,
# because click does not retrieve a dynamic version when installed in editable mode
@click.version_option(__version__,
                      '-v',
                      '--version',
                      message='AiiDA-FeNiCS version %(version)s')
def cmd_root(profile):  # pylint: disable=unused-argument
    """CLI for the `aiida-fenics` plugin."""


# To avoid circular imports all commands are not yet connected to the root
# but they have to be here because of bash completion on the other hand, this
# makes them not work with the difflib...
# see how aiida-core does it.

#cmd_root.add_command(cmd_launch)
#cmd_root.add_command(cmd_plot)
