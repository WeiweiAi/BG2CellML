import importlib
from scipy.integrate import ode
from pathlib import PurePath
import matplotlib.pyplot as graph
from matplotlib import cm
import math

# Modified from https://github.com/hsorby/cellsolver.git
# https://github.com/hsorby/cellsolver.git is licensed under Apache License 2.0

SCIPY_SOLVERS = ['dopri5', 'dop853', 'vode', 'lsoda']

def initialize_system(system):
    rates = system.create_states_array()
    states = system.create_states_array()
    variables = system.create_variables_array()

    system.initialise_variables(states, variables)
    system.compute_computed_constants(variables)

    return states, rates, variables

def algebraic_compute(system,simulation_parameters):
    variable_indices = apply_config(simulation_parameters['result']['config'], system.VARIABLE_INFO)
    variables = system.create_variables_array()
    system.initialise_variables(variables)
    system.compute_computed_constants(variables)
    results = [[] for _ in range( len(variable_indices))]
    for index, variable_index in enumerate(variable_indices):
        results[index].append(variables[variable_index])
    return results

def update(voi, states, system, rates, variables):
    system.compute_rates(voi, states, rates, variables)
    return rates

def store_result(results, states, state_indices, variables, variable_indices):

    state_indices_size = len(state_indices)
    for index, state_index in enumerate(state_indices):
        results[index].append(states[state_index])

    for index, variable_index in enumerate(variable_indices):
        results[state_indices_size + index].append(variables[variable_index])

def info_items_list(name_list):
    info_list = []
    for item in name_list:
        split_item = item.split('.')
        info_list.append({'name': split_item[1], 'component': split_item[0]})

    return info_list


def matching_info_items(item, match_items):
    for match_item in match_items:
        if item['name'] == match_item['name'] and item['component'] == match_item['component']:
            return True

    return False


def not_matching_info_items(item, match_items):
    return not matching_info_items(item, match_items)

def apply_config(config, y_info):
    indices = range(len(y_info))

    if 'parameter_includes' in config and len(config['parameter_includes']):
        info_items = info_items_list(config['parameter_includes'])
        indices = [x for x, z in enumerate(y_info) if matching_info_items(z, info_items)]
    elif 'parameter_excludes' in config and len(config['parameter_excludes']):
        info_items = info_items_list(config['parameter_excludes'])
        indices = [x for x, z in enumerate(y_info) if not_matching_info_items(z, info_items)]

    return indices

def plot_solution(x, y_n, x_info, y_n_info, title):
    extents = _get_extents(y_n, y_n_info)
    unique_extents = list(set(extents))
    ordered_unique_extents = sorted(unique_extents)
    graph_rows = len(ordered_unique_extents)
    colours = _get_colours(len(extents))
    created_subplots = []
    for index, result in enumerate(y_n):
        extent = extents[index]
        graph_row = ordered_unique_extents.index(extent) + 1
        graph.subplot(graph_rows, 1, graph_row)
        graph.plot(x, result, label=r"{0}.{1}".format(y_n_info[index]['component'], y_n_info[index]['name']),
                   color=colours[index])
        graph.legend()
        if graph_row not in created_subplots:
            if graph_row == len(ordered_unique_extents):
                graph.xlabel("{0} ({1})".format(x_info['name'], x_info['units']))
            graph.ylabel("{0}".format(y_n_info[index]['units']))
            if graph_row == 1:
                graph.title(title)

            created_subplots.append(graph_row)
    graph.show()

def _get_colours(num_colours):
    colours = []
    colour_map = cm.get_cmap('hsv')
    for i in range(num_colours):
        colour = colour_map(1. * i / num_colours)  # color will now be an RGBA tuple
        colours.append(colour)

    return colours


def _get_extents(data_in, data_info):
    extents = []
    for index, data in enumerate(data_in):
        abs_max = abs(max(data))
        max_value = math.floor(math.log10(abs_max)) if abs_max > 0.0 else 0.0
        abs_min = abs(min(data))
        min_value = math.floor(math.log10(abs_min)) if abs_min > 0.0 else 0.0
        extents.append('{0} {1} {2}'.format(max_value,
                                            min_value,
                                            data_info[index]['units']))

    return extents

def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def module_type(module):
    if hasattr(module, 'STATE_INFO'):
        return 'ode'
    else:
        return 'algebraic'
    
def scipy_based_solver(system, method, simulation_parameters):
    state_indices = apply_config(simulation_parameters['result']['config'], system.STATE_INFO)
    variable_indices = apply_config(simulation_parameters['result']['config'], system.VARIABLE_INFO)
    states, rates, variables = initialize_system(system)

    # step_size = simulation_parameters['integration']['step_size']
    interval = simulation_parameters['integration']['interval']
    output_step_size = simulation_parameters['result']['step_size']

    if isinstance(output_step_size, list):
        output_step_size = output_step_size[0]

    results = [[] for _ in range(len(state_indices) + len(variable_indices))]
    x = []

    solver = ode(update)
    solver.set_integrator(method, max_step=1e-1)
    solver.set_initial_value(states, interval[0])
    solver.set_f_params(system, rates, variables)

    system.compute_variables(solver.t, solver.y, solver.f_params, variables)
    x.append(solver.t)
    store_result(results, solver.y, state_indices, variables, variable_indices)

    end = interval[-1]
    while solver.successful() and (solver.t + output_step_size) < end:
        solver.integrate(solver.t + output_step_size)

        system.compute_variables(solver.t, solver.y, solver.f_params[1], variables)
        x.append(solver.t)
        store_result(results, solver.y, state_indices, variables, variable_indices)

    solver.integrate(end)
    x.append(solver.t)
    store_result(results, solver.y, state_indices, variables, variable_indices)

    return x, results

def main():

    full_path = '../test/cellml/SLC_SS/SLCT3V_ss_test_inOne.py'
    module_name = PurePath(full_path).stem
    loaded_module = module_from_file(module_name, full_path)
    step_size = 0.0001
    interval = [0, 1]
    result_step_size = 0.1
    config = {'show_plot': True, 'parameter_includes': ['SLCT3V_ss.v_ss'], 'parameter_excludes': []}
    
    simulation_parameters = {
        'integration': {'step_size': step_size, 'interval': interval},
        'result': {'step_size': result_step_size, 'config': config},
    }

    if module_type(loaded_module) == 'ode':
        [x, y_n] = scipy_based_solver(loaded_module, 'lsoda', simulation_parameters)
        plot_title = loaded_module.__name__
        parameter_info = [*loaded_module.STATE_INFO, *loaded_module.VARIABLE_INFO]
        indices = apply_config(config, parameter_info)
        y_n_info = [parameter_info[i] for i in indices]

        if config['show_plot']:
            plot_solution(x, y_n, loaded_module.VOI_INFO, y_n_info, plot_title)

    elif module_type(loaded_module) == 'algebraic':
        y_n=algebraic_compute(loaded_module,simulation_parameters)

    

if __name__ == "__main__":
    main()