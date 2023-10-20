# Blocks world planning problem
# translation from Ruby implementation blocks.rb
# Jonathan Li, October 2018

from graphplan import *

BLOCK = 'Block'

i_A = Instance('A', BLOCK)
i_B = Instance('B', BLOCK)
i_C = Instance('C', BLOCK)
i_D = Instance('D', BLOCK)


v_obj = Variable('obj', BLOCK)
v_from = Variable('from', BLOCK)
v_to = Variable('to', BLOCK)

o_move = Operator('move',
    # Parameters
    [v_obj, v_from, v_to],
    # Preconditions
    [Proposition.newish('equal', [v_obj, v_from], False),
     Proposition.newish('equal', [v_obj, v_to], False),
     Proposition.newish('equal', [v_from, v_to], False),
     Proposition.newish('on', [v_obj, v_from]),
     Proposition.newish('clear', [v_obj]),
     Proposition.newish('clear', [v_to])],
    # Adds
    [Proposition.newish('on', [v_obj, v_to]),
     Proposition.newish('clear', [v_from])],
    # Deletes
    [Proposition.newish('on', [v_obj, v_from]),
     Proposition.newish('clear', [v_to])])

o_move_to_table = Operator('move_to_table',
    # Parameters
    [v_obj, v_from],
    # Preconditions
    [Proposition.newish('equal', [v_obj, v_from], False),
     Proposition.newish('on', [v_obj, v_from]),
     Proposition.newish('clear', [v_obj])],
    # Adds
    [Proposition.newish('on_table', [v_obj]),
     Proposition.newish('clear', [v_from])],
    # Deletes
    [Proposition.newish('on', [v_obj, v_from])])

o_move_from_table = Operator('move_from_table',
    # Parameters
    [v_obj, v_to],
    # Preconditions
    [Proposition.newish('equal', [v_obj, v_to], False),
     Proposition.newish('on_table', [v_obj]),
     Proposition.newish('clear', [v_obj]),
     Proposition.newish('clear', [v_to])],
    # Adds
    [Proposition.newish('on', [v_obj, v_to])],
    # Deletes
    [Proposition.newish('on_table', [v_obj]),
     Proposition.newish('clear', [v_to])])

prob1 = PlanningProblem('blocks_problem',
    # Instances
    [i_A, i_B, i_C],
    # Operators
    [o_move, o_move_to_table, o_move_from_table],
    # Initial state
    [Proposition.newish('on', [i_B, i_A]),
     Proposition.newish('on_table', [i_A]),
     Proposition.newish('on_table', [i_C]),
     Proposition.newish('clear', [i_B]),
     Proposition.newish('clear', [i_C])],
    # Goals
    [Proposition.newish('on', [i_A, i_B]),
     Proposition.newish('on', [i_B, i_C])])

prob2 = PlanningProblem('blocks_problem2',
    # Instances
    [i_A, i_B, i_C],
    # Operators
    [o_move, o_move_to_table, o_move_from_table],
    # Initial state
    [Proposition.newish('on', [i_A, i_B]),
     Proposition.newish('on_table', [i_B]),
     Proposition.newish('on_table', [i_C]),
     Proposition.newish('clear', [i_A]),
     Proposition.newish('clear', [i_C])],
    # Goals
    [Proposition.newish('on', [i_A, i_B]),
     Proposition.newish('on', [i_B, i_C])])

prob3 = PlanningProblem('blocks_problem2',
    # Instances
    [i_A, i_B, i_C, i_D],
    # Operators
    [o_move, o_move_to_table, o_move_from_table],
    # Initial state
    [Proposition.newish('on', [i_A, i_C]),
     Proposition.newish('on', [i_C, i_B]),
     Proposition.newish('on', [i_B, i_D]),
     Proposition.newish('on_table', [i_D]),
     Proposition.newish('clear', [i_A])],
    # Goals
    [Proposition.newish('on', [i_A, i_B]),
     Proposition.newish('on', [i_B, i_C]),
     Proposition.newish('on', [i_C, i_D])])

prob_unsolvable1 = PlanningProblem('blocks_problem',
    # Instances
    [i_A, i_B, i_C],
    # Operators
    [o_move, o_move_to_table, o_move_from_table],
    # Initial state
    [Proposition.newish('on_table', [i_A]),
     Proposition.newish('on_table', [i_B]),
     Proposition.newish('on_table', [i_C]),
     Proposition.newish('clear', [i_A]),
     Proposition.newish('clear', [i_B]),
     Proposition.newish('clear', [i_C])],
    # Goals
    [Proposition.newish('on', [i_A, i_B]),
     Proposition.newish('on', [i_B, i_C]),
     Proposition.newish('on', [i_C, i_A])])

problem = prob3

result = problem.solve()
# problem.dump
if result is not None:
  print("Extracted plan:")
  for level in result:
      for action in level:
          if action.name != NOOP:
              print(action)
else:
  print("No plan found.")
