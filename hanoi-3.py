# Tower of Hanoi problem.

from graphplan import *

# Types
OBJECT = 'object'

# Instances
i_disk_1 = Instance('disk1', OBJECT)
i_disk_2 = Instance('disk2', OBJECT)
i_disk_3 = Instance('disk3', OBJECT)

i_rod_1 = Instance('rod1', OBJECT)
i_rod_2 = Instance('rod2', OBJECT)
i_rod_3 = Instance('rod3', OBJECT)

# Variables
v_disk = Variable('disk', OBJECT)
v_from = Variable('from', OBJECT)
v_to = Variable('to', OBJECT)

# Operators

# Move object from rod to rod if sm than whatever already there
o_move1 = Operator('move1',
    # Preconditions
    [Proposition('clear', v_disk),
     Proposition('clear', v_to),
     Proposition('on', v_disk, v_from),
     Proposition(LESS_THAN, v_disk, v_to)],

    # Adds
    [Proposition('clear', v_from),
     Proposition('on', v_disk, v_to)],

    # Deletes
    [Proposition('clear', v_to),
     Proposition('on', v_disk, v_from)]
)

prob1 = PlanningProblem('hanoi',
    # Instances
    [i_disk_1, i_disk_2, i_disk_3, i_rod_1, i_rod_2, i_rod_3],
    # Operators
    [o_move1],
    # Initial state
    [Proposition('on', i_disk_1, i_disk_2),
     Proposition('on', i_disk_2, i_disk_3),
     Proposition('on', i_disk_3, i_rod_1),

     Proposition('clear', i_disk_1),

     Proposition('clear', i_rod_2),
     Proposition('clear', i_rod_3)],

    # Goals
    [Proposition('on', i_disk_1, i_disk_2),
     Proposition('on', i_disk_2, i_disk_3),
     Proposition('on', i_disk_3, i_rod_3)],

)

prob1.solve()
prob1.display()

print
#prob1.dump()
