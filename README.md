# GraphPlan
Python implementation of the GraphPlan algorithm

Built-in type:
* INT -- instances are integers

Built-in general predicates:
* EQUAL(x, y)
* NOT_EQUAL(x, y)

Built-in numeric predicates:
* LESS_THAN(x, y)
* LESS_EQUAL(x,y)
* SUM(x, y, z)        :   true if x + y = z

Propositions are defined using: Proposition(pred, arg1, arg2, ...)

For negative propositions, use: ~Proposition(pred, arg1, arg2, ...)
