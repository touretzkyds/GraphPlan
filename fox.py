# Fox,, goose beans planning problem.

from graphplan import *

# Types
OBJECT = 'object'
PLACE = 'place'

# Instances
i_farmer = Instance('farmer', OBJECT)
i_fox = Instance('fox', OBJECT)
i_goose = Instance('goose', OBJECT)
i_beans = Instance('beans', OBJECT)
i_east = Instance('east', PLACE)
i_west = Instance('west', PLACE)

# Variables
v_object = Variable('object', OBJECT)
v_other_object = Variable('other_object', OBJECT)
v_neighbor = Variable('neighbor', OBJECT)
v_from = Variable('from', PLACE)
v_place_g = Variable('place_g', PLACE)
v_to = Variable('to', PLACE)
v_other_g = Variable('other_g', PLACE)

# Operators

# If the goose is alone, we can move any object.
o_move1 = Operator('move1',
    # Preconditions
    [Proposition('at', i_farmer, v_from),
     Proposition('at', v_object, v_from),
     Proposition('at', i_goose, v_place_g),
     Proposition('at', i_fox, v_other_g),
     Proposition('at', i_beans, v_other_g),
     Proposition('other_place', v_from, v_to),
     Proposition('other_place', v_place_g, v_other_g)],

    # Adds
    [Proposition('at', i_farmer, v_to),
     Proposition('at', v_object, v_to)],

    # Deletes
    [Proposition('at', i_farmer, v_from),
     Proposition('at', v_object, v_from)]
)

# If the goose is with one of the fox or the beans, we can
# move anything except the farmer.
o_move2 = Operator('move2',
    # Preconditions
    [Proposition('at', i_farmer, v_from),
     Proposition('at', i_goose, v_from),
     Proposition('at', v_neighbor, v_from),
     Proposition('not_equal', v_object, i_farmer),
     Proposition('at', v_other_object, v_to),
     Proposition('other_place', v_from, v_to),
     Proposition('other_object', v_neighbor, v_other_object)],

    # Adds
    [Proposition('at', i_farmer, v_to),
     Proposition('at', v_object, v_to)],

    # Deletes
    [Proposition('at', i_farmer, v_from),
     Proposition('at', v_object, v_from)]
)

# If the goose is with both the fox and the beans, we can
# only move the goose.
o_move3 = Operator('move3',
    # Preconditions
    [Proposition('at', i_farmer, v_from),
     Proposition('at', i_goose, v_from),
     Proposition('at', i_fox, v_from),
     Proposition('at', i_beans, v_from),
     Proposition('equal', v_object, i_goose),
     Proposition('other_place', v_from, v_to)],

    # Adds
    [Proposition('at', i_farmer, v_to),
     Proposition('at', v_object, v_to)],

    # Deletes
    [Proposition('at', i_farmer, v_from),
     Proposition('at', v_object, v_from)]
)


problem = PlanningProblem('fox',
    # Instances
    [i_farmer, i_fox, i_goose, i_beans, i_east, i_west],
    # Operators
    [o_move1, o_move2, o_move3],
    # Initial state
    [Proposition('at', i_farmer, i_east),
     Proposition('at', i_fox, i_east),
     Proposition('at', i_goose, i_east),
     Proposition('at', i_beans, i_east),
     Proposition('other_place', i_east, i_west),
     Proposition('other_place', i_west, i_east),
     Proposition('other_object', i_fox, i_beans),
     Proposition('other_object', i_beans, i_fox)],
    # Goals
    [Proposition('at', i_farmer, i_west),
     Proposition('at', i_fox, i_west),
     Proposition('at', i_goose, i_west),
     Proposition('at', i_beans, i_west)]
)

problem.solve()
problem.display()
#problem.dump()
