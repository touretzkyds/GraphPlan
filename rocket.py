# Rocket planning problem from GraphPlan paper.

from graphplan import *

ROCKET = 'Rocket'
PLACE = 'Place'
CARGO = 'Cargo'

i_rocket1 = Instance('rocket1', ROCKET)

i_london = Instance('london', PLACE)
i_paris = Instance('paris', PLACE)

i_pkgA = Instance('pkgA', CARGO)
i_pkgB = Instance('pkgB', CARGO)


v_r = Variable('r', ROCKET)
v_from = Variable('from', PLACE)
v_to = Variable('to', PLACE)
v_p = Variable('p', PLACE)
v_c = Variable('c', CARGO)

o_move = Operator('move',
    # Parameters
    [v_r, v_from, v_to],
    # Preconditions
    [Proposition.newish('equal', [v_from, v_to], False),
     Proposition.newish('at', [v_r, v_from]),
     Proposition.newish('has_fuel', [v_r])],
    # Adds
    [Proposition.newish('at', [v_r, v_to])],
    # Deletes
    [Proposition.newish('at', [v_r, v_from]),
     Proposition.newish('has_fuel', [v_r])])

o_unload = Operator('unload',
    # Parameters
    [v_r, v_p, v_c],
    # Precodnitions
    [Proposition.newish('at', [v_r, v_p]),
     Proposition.newish('in', [v_c, v_r])],
    # Adds
    [Proposition.newish('at', [v_c, v_p])],
    # Deletes
    [Proposition.newish('in', [v_c, v_r])])

o_load = Operator('load',
    # Parameters
    [v_r, v_p, v_c],
    # Preconditions
    [Proposition.newish('at', [v_r, v_p]),
     Proposition.newish('at', [v_c, v_p])],
    # Adds
    [Proposition.newish('in', [v_c, v_r])],
    # Deletes
    [Proposition.newish('at', [v_c, v_p])])

prob1 = PlanningProblem('prob1',
    # Instances
    [i_rocket1, i_london, i_paris, i_pkgA, i_pkgB],
    # Operators
    [o_move, o_unload, o_load],
    # Initial state
    [Proposition.newish('at', [i_pkgA, i_london]),
     Proposition.newish('at', [i_pkgB, i_london]),
     Proposition.newish('at', [i_rocket1, i_london]),
     Proposition.newish('has_fuel', [i_rocket1])],
    # Goals
    [Proposition.newish('at', [i_pkgA, i_paris]),
     Proposition.newish('at', [i_pkgB, i_paris])])

result = prob1.solve()
prob1.dump()
print("Plan found:")
if result is not None:
    for level in result:
        for a in level:
            print(a)
