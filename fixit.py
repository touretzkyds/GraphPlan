# Fixit planning problem
# translation from Ruby implementation fixit.rb
# Jonathan Li, October 2018

from graphplan import *

WHEEL = 'Wheel'
HUB = 'Hub'
NUT = 'Nut'
CONTAINER = 'Container'
TOOL = 'Tool'

i_wheel1 = Instance('wheel1', WHEEL)
i_wheel2 = Instance('wheel2', WHEEL)
i_hub = Instance('hub', HUB)
i_nuts = Instance('nuts', NUT)
i_boot = Instance('boot', CONTAINER)
i_jack = Instance('jack', TOOL)
i_pump = Instance('pump', TOOL)
i_wrench = Instance('wrench', TOOL)


v_container = Variable('container', CONTAINER)
v_wheel = Variable('wheel', WHEEL)
v_tool = Variable('tool', TOOL)
v_nut = Variable('nut', NUT)
v_hub = Variable('hub', HUB)

o_cuss = Operator(
    'cuss',
    # Parameters
    [],
    # Preconditions
    [],
    # Adds
    [Proposition.newish('not_annoyed',[])],
    # Deletes
    [] 
)

o_open = Operator(
    'open',
    # Parameters
    [v_container],
    # Preconditions
    [Proposition.newish('not_open', [v_container])],
    # Adds
    [Proposition.newish('open', [v_container])],
    # Deletes
    [Proposition.newish('not_open', [v_container])]
)

o_close = Operator(
    'close',
    # Parameters
    [v_container],
    # Preconditions
    [Proposition.newish('open', [v_container])],
    # Adds
    [Proposition.newish('not_open', [v_container])],
    # Deletes
    [Proposition.newish('open', [v_container])]
)

o_fetch_tool = Operator(
    'fetch_tool',
    # Parameters
    [v_tool, v_container],
    # Preconditions
    [Proposition.newish('in', [v_tool, v_container]),
     Proposition.newish('open', [v_container])],
    # Adds
    [Proposition.newish('have', [v_tool])],
    # Deletes
    [Proposition.newish('in', [v_tool, v_container])]
)

o_fetch_wheel = Operator(
    'fetch_wheel',
    # Parameters
    [v_wheel, v_container],
    # Preconditions
    [Proposition.newish('in', [v_wheel, v_container]),
     Proposition.newish('open', [v_container])],
    # Adds
    [Proposition.newish('have', [v_wheel])],
    # Deletes
    [Proposition.newish('in', [v_wheel, v_container])]
)

o_put_away_tool = Operator(
    'put_away_tool',
    # Parameters
    [v_tool, v_container],
    # Preconditions
    [Proposition.newish('have', [v_tool]),
     Proposition.newish('open', [v_container])],
    # Adds
    [Proposition.newish('in', [v_tool, v_container])],
    # Deletes
    [Proposition.newish('have', [v_tool])]
)


o_put_away_wheel = Operator(
    'put_away_wheel',
    # Parameters
    [v_wheel, v_container],
    # Preconditions
    [Proposition.newish('have', [v_wheel]),
     Proposition.newish('open', [v_container])],
    # Adds
    [Proposition.newish('in', [v_wheel, v_container])],
    # Deletes
    [Proposition.newish('have', [v_wheel])]
)

o_loosen = Operator(
    'loosen',
    # Parameters
    [v_nut, v_hub],
    # Preconditions
    [Proposition.newish('have', [i_wrench]),
     Proposition.newish('tight', [v_nut, v_hub]),
     Proposition.newish('on_ground', [v_hub])],
    # Adds
    [Proposition.newish('loose', [v_nut, v_hub])],
    # Deletes
    [Proposition.newish('tight', [v_nut, v_hub])]
)

o_tighten = Operator(
    'tighten',
    # Parameters
    [v_nut, v_hub],
    # Preconditions
    [Proposition.newish('have', [i_wrench]),
     Proposition.newish('loose', [v_nut, v_hub]),
     Proposition.newish('on_ground', [v_hub])],
    # Adds
    [Proposition.newish('tight', [v_nut, v_hub])],
    # Deletes
    [Proposition.newish('loose', [v_nut, v_hub])]
)

o_jack_up = Operator(
    'jack_up',
    # Parameters
    [v_hub],
    # Preconditions
    [Proposition.newish('on_ground', [v_hub]),
     Proposition.newish('have', [i_jack])],
    # Adds
    [Proposition.newish('not_on_ground', [v_hub])],
    # Deletes
    [Proposition('have', [i_jack]),
     Proposition.newish('on_ground', [v_hub])]
)    

o_jack_down = Operator(
    'jack_down',
    # Parameters
    [v_hub],
    # Preconditions
    [Proposition.newish('not_on_ground', [v_hub])],
    # Adds
    [Proposition.newish('on_ground', [v_hub]),
     Proposition.newish('have', [i_jack])],
    # Deletes
    [Proposition.newish('not_on_ground', [v_hub])]
)

o_undo = Operator(
    'undo',
    # Parameters
    [v_nut, v_hub],
    # Preconditions
    [Proposition.newish('not_on_ground', [v_hub]),
     Proposition.newish('not_unfastened', [v_hub]),
     Proposition.newish('have', [i_wrench]),
     Proposition.newish('loose', [v_nut, v_hub])],
    # Adds
    [Proposition.newish('have', [v_nut]),
     Proposition.newish('unfastened', [v_hub])],
    # Deletes
    [Proposition.newish('on', [v_nut, v_hub]),
     Proposition.newish('loose', [v_nut, v_hub]),
     Proposition.newish('not_unfastened', [v_hub])]
)

o_do_up = Operator(
    'do_up',
    # Parameters
    [v_nut, v_hub],
    # Preconditions
    [Proposition.newish('have', [i_wrench]),
     Proposition.newish('unfastened', [v_hub]),
     Proposition.newish('not_on_ground', [v_hub]),
     Proposition.newish('have', [v_nut])],
    # Adds
    [Proposition.newish('loose', [v_nut, v_hub]),
     Proposition.newish('not_unfastened', [v_hub])],
    # Deletes
    [Proposition.newish('have', [v_nut]),
     Proposition.newish('unfastened', [v_hub])]
)

o_remove_wheel = Operator(
    'remove_wheel',
    # Parameters
    [v_wheel, v_hub],
    # Preconditions
    [Proposition.newish('not_on_ground', [v_hub]),
     Proposition.newish('on', [v_wheel, v_hub]),
     Proposition.newish('unfastened', [v_hub])],
    # Adds
    [Proposition.newish('have', [v_wheel]),
     Proposition.newish('free', [v_hub])],
    # Deletes
    [Proposition.newish('on', [v_wheel, v_hub])]
)

o_put_on_wheel = Operator(
    'put_on_wheel',
    # Parameters
    [v_wheel, v_hub],
    # Preconditions
    [Proposition.newish('have', [v_wheel]),
     Proposition.newish('free', [v_hub]),
     Proposition.newish('unfastened', [v_hub]),
     Proposition.newish('not_on_ground', [v_hub])],
    # Adds
    [Proposition.newish('on', [v_wheel, v_hub])],
    # Deletes
    [Proposition.newish('have', [v_wheel]),
     Proposition.newish('free', [v_hub])]
)

o_inflate = Operator(
    'inflate',
    # Parameters
    [v_wheel],
    # Preconditions
    [Proposition.newish('have', [i_pump]),
     Proposition.newish('not_inflated', [v_wheel]),
     Proposition.newish('intact', [v_wheel])],
    # Adds
    [Proposition.newish('inflated', [v_wheel])],
    # Deletes
    [Proposition.newish('not_inflated', [v_wheel])]
)

prob = PlanningProblem(
    'fixit_problem',
    # Instances
    [i_wheel1, i_wheel2, i_hub, i_nuts, i_boot, i_jack, i_pump, i_wrench],
    # Operators
    [o_cuss, o_open, o_close, o_fetch_tool, o_fetch_wheel, o_put_away_tool,
     o_put_away_wheel, o_loosen, o_tighten, o_jack_up, o_jack_down, o_undo,
     o_do_up, o_remove_wheel, o_put_on_wheel, o_inflate],
    # Initial state
    [Proposition.newish('not_open', [i_boot]),
     Proposition.newish('intact', [i_wheel2]),
     Proposition.newish('in', [i_jack, i_boot]),
     Proposition.newish('in', [i_pump, i_boot]),
     Proposition.newish('in', [i_wheel2, i_boot]),
     Proposition.newish('in', [i_wrench, i_boot]),
     Proposition.newish('on', [i_wheel1, i_hub]),
     Proposition.newish('on_ground', [i_hub]),
     Proposition.newish('tight', [i_nuts, i_hub]),
     Proposition.newish('not_inflated', [i_wheel2]),
     Proposition.newish('not_unfastened', [i_hub])],
    # Goals
    [Proposition.newish('not_open', [i_boot]),
     Proposition.newish('in', [i_jack, i_boot]),
     Proposition.newish('in', [i_pump, i_boot]),
     Proposition.newish('in', [i_wheel1, i_boot]),
     Proposition.newish('in', [i_wrench, i_boot]),
     Proposition.newish('tight', [i_nuts, i_hub]),
     Proposition.newish('inflated', [i_wheel2]),
     Proposition.newish('on', [i_wheel2, i_hub])])

problem = prob

result = problem.solve()

if result is not None:
    print('Extracted plan!')
    for level in result:
        for action in level:
            if action.name != NOOP:
                print(action)
else:
    print('No plan found')
