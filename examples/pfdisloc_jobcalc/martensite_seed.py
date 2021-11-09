#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import fenics
import yaml

import marshmallow_dataclass  # type: ignore
import marshmallow.exceptions  # type: ignore

from pfdisloc.models import (
    DislocationModel,
    # LinearElasticModel,
    LinearIsotropicModel,
    BinaryPhaseModel)

from pfdisloc.phase_field_models import (LevitasModel, SchmittModel)

from pfdisloc.solvers import (LinearElasticitySolver,
                              HigherOrderElasticitySolver)

from pfdisloc.parameters import Config
from pfdisloc.phase_field_solvers import PhaseFieldSolver
from pfdisloc.refinement import edge_dislocation_refinement

from pfdisloc.utils import (build_boundary_conditions, convertMeshFunction,
                            Timing)

# global FEniCS configuration
fenics.parameters['form_compiler']['optimize'] = True
fenics.parameters['form_compiler']['cpp_optimize'] = True

parser = argparse.ArgumentParser(description='Solve linear elasticity for \
    material with dislocations.')

parser.add_argument('-c',
                    '--config',
                    type=argparse.FileType('r'),
                    dest='config_file',
                    required=True,
                    help='YAML configuration file')

parser.add_argument('-t',
                    '--timing',
                    action='store_true',
                    help='time components (BCs, solvers, etc.)')

parser.add_argument('-v',
                    '--verbose',
                    action='store_true',
                    help='increase output verbosity')

args = parser.parse_args()

if args.verbose:
    fenics.set_log_level(2)

config_schema = marshmallow_dataclass.class_schema(Config)()
try:
    config = config_schema.load(yaml.safe_load(args.config_file))
except marshmallow.exceptions.ValidationError as err:
    raise SystemExit('ERROR: Invalid configuration in \'{}\':\n{}'.format(
        args.config_file.name, err))

mesh = fenics.RectangleMesh(
    fenics.Point(config.domain.size) * -0.5,
    fenics.Point(config.domain.size) * 0.5, config.domain.mesh_size[0],
    config.domain.mesh_size[1], 'crossed')

if config.domain.refinement:
    refine_range = 0.5 * min(
        config.domain.size[0] / config.domain.mesh_size[0],
        config.domain.size[1] / config.domain.mesh_size[1])

    mesh = edge_dislocation_refinement(mesh, config.domain.refinement,
                                       refine_range,
                                       config.dislocations.discrete,
                                       config.dislocations.parameters)

# if len(config.materials) != 2:
#    raise RuntimeError('Two materials required for bimaterial')

V = fenics.FunctionSpace(mesh, 'Lagrange', 2)
martensite_order_parameter = fenics.Function(V, name='order parameter')

if config.phase_field.initial:
    initial_order_parameter = fenics.Expression(
        config.phase_field.initial.expression,
        domain_size_x=config.domain.size[0],
        domain_size_y=config.domain.size[1],
        domain_size_z=config.domain.size[2]
        if len(config.domain.size) == 3 else 0,
        degree=2)
else:
    initial_order_parameter = fenics.Constant(0)

martensite_order_parameter.assign(initial_order_parameter)

if config.dislocations is None:
    base_model = LinearIsotropicModel(config.materials)
    # base_model = LinearElasticModel(config.materials)
else:
    base_model = DislocationModel(config.materials,
                                  config.dislocations.parameters, mesh,
                                  config.dislocations.discrete)

model = BinaryPhaseModel(base_model, config.materials,
                         martensite_order_parameter)

V_vec = fenics.VectorFunctionSpace(mesh, 'Lagrange', 2)
elastic_solver = LinearElasticitySolver(V_vec, model)

# set boundary conditions based on selected configuration
bcs = build_boundary_conditions(config.boundary, mesh, V_vec)

for bc in bcs['dirichlet']:
    elastic_solver.add_bc(bc)

for bc in bcs['neumann']:
    elastic_solver.add_boundary_load(*bc)

# if using a core regularization, then also add stress-free boundary BCs
if config.core_regularization:
    ho_solver = HigherOrderElasticitySolver(V, config.core_regularization)
    # ho_solver.add_bc(fenics.DirichletBC(V, fenics.Constant(0.), LeftEdge(mesh)))
    # ho_solver.add_bc(fenics.DirichletBC(V, fenics.Constant(0.), RightEdge(mesh)))
    # ho_solver.add_bc(fenics.DirichletBC(V, fenics.Constant(0.), BottomEdge(mesh)))
    # ho_solver.add_bc(fenics.DirichletBC(V, fenics.Constant(0.), TopEdge(mesh)))

    true_stress = ho_solver.stress()
else:
    true_stress = None

if config.phase_field.parameters.model == 'schmitt':
    pf_model = SchmittModel(config.phase_field.parameters,
                            stress=elastic_solver.stress(),
                            strain=elastic_solver.strain())
elif config.phase_field.parameters.model == 'levitas':
    if not true_stress:
        raise RuntimeError('Levitas phase field model requires higher-order '
                           'stress calculation')

    pf_model = LevitasModel(config.phase_field.parameters,
                            materials=config.materials,
                            stress=true_stress,
                            strain=elastic_solver.strain())
else:
    raise NotImplementedError(
        'phase field model \'{}\' not yet supported'.format(
            config.phase_field.parameters.model))

pf_solver = PhaseFieldSolver(V,
                             order_parameter=martensite_order_parameter,
                             model=pf_model)

output_base_path = config.output.path

le_output = fenics.XDMFFile(f'{output_base_path}/linear_elasticity.xdmf')
le_output.parameters['flush_output'] = True
le_output.parameters['functions_share_mesh'] = True
le_output.parameters['rewrite_function_mesh'] = False

order_parameter_output = fenics.XDMFFile(
    f'{output_base_path}/order_parameter.xdmf')
order_parameter_output.parameters['flush_output'] = True
order_parameter_output.parameters['functions_share_mesh'] = True
order_parameter_output.parameters['rewrite_function_mesh'] = False

elastic_energy_density = fenics.Function(fenics.FunctionSpace(mesh, 'DG', 0),
                                         name='elastic energy density')

elastic_energy_density_output = fenics.XDMFFile(
    f'{output_base_path}/elastic_energy_density.xdmf')
elastic_energy_density_output.parameters['flush_output'] = True
elastic_energy_density_output.parameters['functions_share_mesh'] = True
elastic_energy_density_output.parameters['rewrite_function_mesh'] = False

if isinstance(base_model, DislocationModel):
    dislocation_trace_output = fenics.XDMFFile(
        f'{output_base_path}/dislocation_trace.xdmf')
    dislocation_trace_output.parameters['flush_output'] = True
    dislocation_trace_output.parameters['functions_share_mesh'] = True
    dislocation_trace_output.parameters['rewrite_function_mesh'] = False

t = 0.0
T = 1e-6
dt = 2.5e-9

elastic_solver.assemble()
elastic_solver.solve()

# write out initial values
le_output.write(elastic_solver.stress(), t)

if isinstance(base_model, DislocationModel):
    dislocation_trace_output.write(
        convertMeshFunction(base_model.dislocation_trace()), t)

if true_stress:
    linear_stress = elastic_solver.stress()
    # if mesh.topology().dim() == 2:
    #     linear_stress = out_of_plane_stress(
    #         linear_stress,
    #         config.materials[0].poisson_ratio
    #     )

    ho_solver.solve_phasefield(linear_stress, config.materials,
                               pf_solver.order_parameter(), pf_model)

    le_output.write(true_stress, t)

order_parameter_output.write(pf_solver.order_parameter(), t)

elastic_energy_density.assign(
    fenics.project(
        0.5 * fenics.inner(elastic_solver.stress(), elastic_solver.strain()),
        fenics.FunctionSpace(mesh, 'DG', 0)))

elastic_energy_density_output.write(elastic_energy_density, t)

adapted = False

timeStep = 0
while t <= T:
    with Timing(f'Finished time step #{timeStep}, t={t:.5g}', args.timing):
        # if not adapted and t >= 4e-9:
        #     dt *= 5
        #     adapted = True

        t += dt

        elastic_solver.solve()
        if true_stress:
            ho_solver.solve_phasefield(elastic_solver.stress(),
                                       config.materials,
                                       pf_solver.order_parameter(), pf_model)

        if not timeStep:
            pf_solver.assemble(dt=dt)

        pf_solver.solve()

        le_output.write(elastic_solver.stress(), t)
        if true_stress:
            le_output.write(true_stress, t)

        elastic_energy_density.assign(
            fenics.project(
                0.5 *
                fenics.inner(elastic_solver.stress(), elastic_solver.strain()),
                fenics.FunctionSpace(mesh, 'DG', 0)))

        elastic_energy_density_output.write(elastic_energy_density, t)

        order_parameter_output.write(pf_solver.order_parameter(), t)

        if isinstance(base_model, DislocationModel):
            dislocation_trace_output.write(
                convertMeshFunction(base_model.dislocation_trace()), t)

        timeStep += 1
