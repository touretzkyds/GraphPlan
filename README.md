# GraphPlan
Python implementation of the GraphPlan algorithm

Built-in type:
* INT -- instances are integers

Built-in general predicates:
* EQUAL(x, y)
* NOT_EQUAL(x, y)

Built-in predicates:
* LESS_THAN(x, y) : works on integers or symbols (alphabetical order)
* LESS_EQUAL(x,y) : works on integers or symbols (alphabetical order)
* SUM(x, y, z)        :   true if x + y = z

Propositions are defined using: Proposition(pred, arg1, arg2, ...)

For negative propositions, use: ~Proposition(pred, arg1, arg2, ...)
