# Missionaries and Cannibals Problem
#
from graphplan import *

# Types
SIDE = 'Side'

# Instances
i_0 = Instance(0, INT)
i_1 = Instance(1, INT)
i_2 = Instance(2, INT)
i_3 = Instance(3, INT)

i_east = Instance('east', SIDE)
i_west = Instance('west', SIDE)

# Variables
v_m1 = Variable('m1', INT)
v_m1x = Variable('m1x', INT)
v_c1 = Variable('c1', INT)
v_c1x = Variable('c1x', INT)
v_m2 = Variable('m2', INT)
v_m2x = Variable('m2x', INT)
v_c2 = Variable('c2', INT)
v_c2x = Variable('c2x', INT)

v_side1 = Variable('side1', SIDE)
v_side2 = Variable('side2', SIDE)

# Operators
o_1m = Operator('move_1m',
    # Preconditions
    [Proposition('at', v_side1),
     Proposition('other', v_side2),
     Proposition('not_equal', v_side1, v_side2),
     Proposition('state', v_side1, v_m1, v_c1),
     Proposition('state', v_side2, v_m2, v_c2),
     Proposition('sum', v_m1x, i_1, v_m1),
     Proposition('sum', v_m2, i_1, v_m2x),
     Proposition('sum', v_m1, v_m2, i_3),
     Proposition('sum', v_c1, v_c2, i_3),
     Proposition('legal', v_m1x, v_c1)],
    # Adds
    [Proposition('at', v_side2),
     Proposition('other', v_side1),
     Proposition('state', v_side1, v_m1x, v_c1),
     Proposition('state', v_side2, v_m2x, v_c2)],
    # Deletes
    [Proposition('at', v_side1),
     Proposition('other', v_side2),
     Proposition('state', v_side1, v_m1, v_c1),
     Proposition('state', v_side2, v_m2, v_c2)]
)

o_1c = Operator('move_1c',
    # Preconditions
    [Proposition('at', v_side1),
     Proposition('other', v_side2),
     Proposition('not_equal', v_side1, v_side2),
     Proposition('state', v_side1, v_m1, v_c1),
     Proposition('state', v_side2, v_m2, v_c2),
     Proposition('sum', v_c1x, i_1, v_c1),
     Proposition('sum', v_c2, i_1, v_c2x),
     Proposition('sum', v_m1, v_m2, i_3),
     Proposition('sum', v_c1, v_c2, i_3),
     Proposition('legal', v_m1, v_c1x)],
    # Adds
    [Proposition('at', v_side2),
     Proposition('other', v_side1),
     Proposition('state', v_side1, v_m1, v_c1x),
     Proposition('state', v_side2, v_m2, v_c2x)],
    # Deletes
    [Proposition('at', v_side1),
     Proposition('other', v_side2),
     Proposition('state', v_side1, v_m1, v_c1),
     Proposition('state', v_side2, v_m2, v_c2)]
)

o_2m = Operator('move_2m',
    # Preconditions
    [Proposition('at', v_side1),
     Proposition('other', v_side2),
     Proposition('not_equal', v_side1, v_side2),
     Proposition('state', v_side1, v_m1, v_c1),
     Proposition('state', v_side2, v_m2, v_c2),
     Proposition('sum', v_m1x, i_2, v_m1),
     Proposition('sum', v_m2, i_2, v_m2x),
     Proposition('sum', v_m1, v_m2, i_3),
     Proposition('sum', v_c1, v_c2, i_3),
     Proposition('legal', v_m1x, v_c1)],
    # Adds
    [Proposition('at', v_side2),
     Proposition('other', v_side1),
     Proposition('state', v_side1, v_m1x, v_c1),
     Proposition('state', v_side2, v_m2x, v_c2)],
    # Deletes
    [Proposition('at', v_side1),
     Proposition('other', v_side2),
     Proposition('state', v_side1, v_m1, v_c1),
     Proposition('state', v_side2, v_m2, v_c2)]
)

o_2c = Operator('move_2c',
    # Preconditions
    [Proposition('at', v_side1),
     Proposition('other', v_side2),
     Proposition('not_equal', v_side1, v_side2),
     Proposition('state', v_side1, v_m1, v_c1),
     Proposition('state', v_side2, v_m2, v_c2),
     Proposition('sum', v_c1x, i_2, v_c1),
     Proposition('sum', v_c2, i_2, v_c2x),
     Proposition('sum', v_m1, v_m2, i_3),
     Proposition('sum', v_c1, v_c2, i_3),
     Proposition('legal', v_m1, v_c1x)],
    # Adds
    [Proposition('at', v_side2),
     Proposition('other', v_side1),
     Proposition('state', v_side1, v_m1, v_c1x),
     Proposition('state', v_side2, v_m2, v_c2x)],
    # Deletes
    [Proposition('at', v_side1),
     Proposition('other', v_side2),
     Proposition('state', v_side1, v_m1, v_c1),
     Proposition('state', v_side2, v_m2, v_c2)]
)

o_1m1c = Operator('move_1m1c',
    # Preconditions
    [Proposition('at', v_side1),
     Proposition('other', v_side2),
     Proposition('not_equal', v_side1, v_side2),
     Proposition('state', v_side1, v_m1, v_c1),
     Proposition('state', v_side2, v_m2, v_c2),
     Proposition('sum', v_m1x, i_1, v_m1),
     Proposition('sum', v_m2, i_1, v_m2x),
     Proposition('sum', v_c1x, i_1, v_c1),
     Proposition('sum', v_c2, i_1, v_c2x),
     Proposition('sum', v_m1, v_m2, i_3),
     Proposition('sum', v_c1, v_c2, i_3),
     Proposition('legal', v_m1x, v_c1x)],
    # Adds
    [Proposition('at', v_side2),
     Proposition('other', v_side1),
     Proposition('state', v_side1, v_m1x, v_c1x),
     Proposition('state', v_side2, v_m2x, v_c2x)],
    # Deletes
    [Proposition('at', v_side1),
     Proposition('other', v_side2),
     Proposition('state', v_side1, v_m1, v_c1),
     Proposition('state', v_side2, v_m2, v_c2)]
)

prob1 = PlanningProblem('mandc',
    # Instances
    [i_0, i_1, i_2, i_3, i_east, i_west],
    # Operators
    [o_1m, o_1c, o_2m, o_2c, o_1m1c],
    # Initial state
    [Proposition('at', i_east),
     Proposition('other', i_west),
     Proposition('state', i_east, i_3, i_3),
     Proposition('state', i_west, i_0, i_0),

     Proposition('legal', i_3, i_3),
     Proposition('legal', i_2, i_2),
     Proposition('legal', i_1, i_1),
     Proposition('legal', i_3, i_2),
     Proposition('legal', i_3, i_1),
     Proposition('legal', i_3, i_0),
     Proposition('legal', i_0, i_3),
     Proposition('legal', i_0, i_2),
     Proposition('legal', i_0, i_1),
     Proposition('legal', i_0, i_0)
    ],
    # Goals
    [Proposition('state', i_west, i_3, i_3)]
)

prob1.solve()
prob1.display()
#prob1.dump()
