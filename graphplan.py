# Python implementation of GraphPlan algorithm (Blum & Furst)
# Originally implemented in Ruby by David S. Touretzky, October 2012
# Translated to Python by Jonathan Li, October 2018

from copy import deepcopy
from pprint import pprint

NODE_COUNTER = 0

### Defining macros to serve as the equivalent of Ruby Symbols
EQUAL = 'equal'
NOOP = 'noop'

def safeIndex(l, f):
    '''
    let l be a list of items [x_i | 0 <= i <= len(l)]

    safeIndex(l,f) returns the index of the first x_i
    such that f(x_i) == True

    if such an element does not exist, safeIndex returns None
    '''

    for i in range(len(l)):
        x = l[i]
        if f(x):
            return i

    return None

class Instance:

    def __init__(self, name, kind):
        self.name = name
        self.kind = kind

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)

    def __eq__(self, other):
        return (
            isinstance(other, Instance) and
            self.name == other.name and
            self.kind == other.kind
        )

    def __hash__(self):
        '''
        Defining __eq__ causes a class to be unhashable by default,
        must explicitly re-define __hash__ if __eq__ is defined
        '''
        return hash(str(self))

class Variable:

    def __init__(self, name, kind):
        self.name = name
        self.kind = kind

    def __str__(self):
        return '?' + str(self.kind) + ':' + str(self.name)

    def __repr__(self):
        return '?' + str(self.kind) + ':' + str(self.name)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self.name == other.name and self.kind == other.kind


class Proposition:

    prophash = dict()

    def __init__(self, pred, args=[], value=True):
        self.pred = pred
        self.args = args
        self.value = value
        self.propnum = None
        if not ([arg for arg in args if isinstance(arg, Variable)]):
            # can't hash lists in python!
            signature = (pred, tuple(args), value)
            Proposition.prophash[signature] = self
            self.propnum = len(Proposition.prophash)

    @classmethod
    def newish(cls, pred, args, value=True):
        signature = (pred, tuple(args), value)
        if Proposition.prophash.get(signature, None) is not None:
            return Proposition.prophash[signature]
        else:
            return Proposition(pred, args, value)


    def __str__(self):
        if self.propnum:
            num = str(self.propnum)
        else:
            num = ''

        if self.value:
            sign = ''
        else:
            '~'

        argstring = '('
        argsep = ''

        for arg in self.args:
            argstring += argsep + str(arg)
            argsep = ','

        argstring += ')'
        return num + ':' + sign + str(self.pred) + argstring

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return (
            isinstance(other, Proposition) and
            self.pred == other.pred and
            self.args == other.args and
            self.value == other.value
        )

    def __hash__(self):
        '''
        Defining __eq__ causes a class to be unhashable by default,
        must explicitly re-define __hash__ if __eq__ is defined
        '''
        return hash(str(self))
    

    def instantiate(self, bindings):
        newargs = [bindings.get(x,x) for x in self.args]
        return Proposition.newish(self.pred, newargs, self.value)
    
class Operator:

    def __init__(self, name, params, precs, adds, deletes):
        self.name = name
        self.params = params
        self.precs = precs
        self.adds = adds
        self.deletes = deletes

    def __str__(self):
        return str(self.name) + str(self.params)

    def __repr__(self):
        return str(self)
    

    def generate_bindings(self, instance_table):
        # generate a list of lists of possible variable bindings for this operator
        bindings = [{}]
        for p in self.params:
            t = p.kind
            newbinds = []
            for inst in instance_table[t]:
                bindings_copy = deepcopy(bindings)
                for i in range(len(bindings_copy)):
                    bindings_copy[i][p] = inst
                newbinds = newbinds + bindings_copy
            bindings = newbinds
        return bindings

    def generate_bindprops(self, propnodes, instance_table):
        bindings = self.generate_bindings(instance_table)
        bindprops = []
        for bind in bindings:
            props = []
            for prec in self.precs:
                bprec = prec.instantiate(bind)
                if bprec.pred == EQUAL:
                    if (bprec.args[0] == bprec.args[1]) != bprec.value:
                        props = None
                        break
                else:
                    pnodes = [pn for pn in propnodes if pn.prop == bprec]
                    if (len(pnodes) == 0):
                        props = None
                    else:
                        props.append(pnodes[0])
                if props is None:
                    break
            bindprops = (
                bindprops + [BindProp(bind, props)]
                if props is not None else bindprops
            )
        return bindprops


class BindProp:

    def __init__(self, bindings, propnodes):
        self.bindings = bindings
        self.propnodes = propnodes

    def __str__(self):
        return 'Bind<' + str(self.bindings) + ';' + str(self.propnodes) + '>'

    def __repr__(self):
        return str(self)

    def preconditions_excluded(self):
        # return the first propNode for which its
        # excluded preconditions are also in self.propnodes
        for pn in self.propnodes:
            for q in pn.excludes:
                if q in self.propnodes:
                    return pn
        return None

class PropNode:

    def __init__(self, prop, level):
        global NODE_COUNTER
        self.prop = prop
        self.level = level
        self.number = NODE_COUNTER + 1
        NODE_COUNTER += 1
        self.propnum = None
        self.adders = []
        self.deleters = []
        self.users = []
        self.excludes = []

    def __str__(self):
        pname = str(self.prop)
        return pname

    def __repr__(self):
        return str(self)

    def excludes_prop(self, pnode):
        for anode in self.adders:
            for anode2 in pnode.adders:
                if anode2 not in anode.excludes:
                    return None

        return True

    ## defining the comparison operators between propNodes ##
    ## equivalent of Ruby's <=> ##

    def __eq__(self, other):
        if not isinstance(other, PropNode):
            return False
        return self.prop.propnum == other.prop.propnum

    def __ne__(self, other):
        if isinstance(other, PropNode):
            return self.prop.propnum != other.prop.propnum
        return True
        
    def __lt__(self, other):
        return self.prop.propnum < other.prop.propnum

    def __le__(self, other):
        return self.prop.propnum <= other.prop.propnum

    def __gt__(self, other):
        return self.prop.propnum > other.prop.propnum

    def __ge__(self, other):
        return self.prop.propnum >= other.prop.propnum

    def __hash__(self):
        '''
        Defining __eq__ causes a class to be unhashable by default,
        must explicitly re-define __hash__ if __eq__ is defined
        '''
        return hash(str(self))

class ActionNode:

    def __init__(self, name, level, binds, precs):
        global NODE_COUNTER
        self.name = name
        self.level = level
        self.number = NODE_COUNTER + 1
        NODE_COUNTER += 1
        self.binds = binds
        self.precs = precs
        self.adds = []
        self.deletes = []
        self.excludes = []

    def __str__(self):
        if self.name == NOOP:
            args = str(self.precs[0])
            args = args[(args.index(':') + 1) : ]
        else:
            args = str(self.binds)
        return str(self.level) + str(self.name) + ('-%d ' % self.number) + args

    def __repr__(self):
        return str(self)

    def deletes_addition(self, anode):
        # determines if the intersection is non-empty
        intersection = [x for x in self.deletes if x in anode.adds]
        return len(intersection) > 0

    def deletes_precondition(self, anode):
        # does deleted prop at level i+1 match precondition prop at level i?
        for d in self.deletes:
            for p in anode.precs:
                if d.prop == p.prop:
                    return True
        return False

    def competing_needs(self, anode):
        for p in self.precs:
            for p2 in anode.precs:
                if p2 in p.excludes:
                    return True
        return False

class PlanningProblem:

    def __init__(self, name, instances, operators, initial, goals):
        self.name = name
        self.instances = instances
        self.operators = operators
        self.initial = initial
        self.goals = goals
        self.propLevels = []
        self.actionLevels = []
        self.level = -1
        self.unsolvable_goalsets = [dict()]

        self.generate_instance_table()
        self.populate_prop_level_0()

    def generate_instance_table(self):
        self.instance_table = dict()
        for inst in self.instances:
            if inst.kind not in self.instance_table:
                self.instance_table[inst.kind] = []
            if inst not in self.instance_table[inst.kind]:
                self.instance_table[inst.kind].append(inst)

    def populate_prop_level_0(self):
        self.propLevels = [[]]
        for prop in self.initial:
            self.propLevels[0].append(PropNode(prop, 0))

    def extend_graph_level(self):
        # Generate next levels of action and proposition nodes
        self.actionLevels.append([])
        self.propLevels.append([])
        self.unsolvable_goalsets.append(dict())
        self.level += 1

        self.generate_noop_actions()

        for op in self.operators:
            self.generate_operator_actions(op)

        self.generate_action_excludes_links()
        self.generate_proposition_excludes_links()

    def generate_noop_actions(self):
        for pnode in self.propLevels[-2]:
            anode = ActionNode(NOOP, pnode.level, dict(), [pnode])
            pnode.users.append(anode)
            pnode2 = PropNode(pnode.prop, 1 + pnode.level)
            anode.adds.append(pnode2)
            pnode2.adders.append(anode)
            self.propLevels[-1].append(pnode2)
            self.actionLevels[-1].append(anode)

    def generate_operator_actions(self, op):
        bindprops = op.generate_bindprops(self.propLevels[-2], self.instance_table)
        bindprops = [bp for bp in bindprops
                     if bp.preconditions_excluded() is None]
        self.actionLevels[-1] += [self.generate_action_node(op,bp)
                                  for bp in bindprops]

    def generate_action_node(self, op, bp):
        # op = operator, bp = bindProp
        anode = ActionNode(op.name, self.level, bp.bindings, bp.propnodes)
        for pnode in bp.propnodes:
            pnode.users.append(anode)

        anode.adds = [
            self.get_propnode(prop.instantiate(bp.bindings), self.level+1)
            for prop in op.adds
        ]
        for pnode in anode.adds:
            pnode.adders.append(anode)

        anode.deletes = [
            self.get_propnode(prop.instantiate(bp.bindings), self.level+1)
            for prop in op.deletes
        ]
        for pnode in anode.deletes:
            pnode.deleters.append(anode)
            
        return anode

    def generate_action_excludes_links(self):
        for anode in self.actionLevels[-1]:
            for bnode in self.actionLevels[-1]:
                if anode != bnode:
                    if (
                            anode.deletes_addition(bnode) or
                            anode.deletes_precondition(bnode) or
                            anode.competing_needs(bnode)
                    ):
                        if (bnode not in anode.excludes):
                            anode.excludes.append(bnode)
                        if (anode not in bnode.excludes):
                            bnode.excludes.append(anode)

    def generate_proposition_excludes_links(self):
        for pnode in self.propLevels[-1]:
            for pnode2 in self.propLevels[-1]:
                if pnode != pnode2 and pnode.excludes_prop(pnode2):
                    pnode.excludes.append(pnode2)
    

    def leveled_off(self):
        '''
        The graph has leveled off if the last level contains no new
        propositions, and the same number of exclusion relationships as the
        level before it
        '''
        if len(self.propLevels) < 2:
            return None

        if len(self.propLevels[-1]) != len(self.propLevels[-2]):
            return None

        this_excludes = 0
        for prop in self.propLevels[-1]:
            this_excludes += len(prop.excludes)
            
        prev_excludes = 0
        for prop in self.propLevels[-2]:
            prev_excludes += len(prop.excludes)

        if this_excludes != prev_excludes:
            return None

        return True

    def get_existing_propnode(self, prop, level):
        for pnode in self.propLevels[level]:
            if pnode.prop == prop:
                return pnode
        return None

    def get_propnode(self, prop, level):
        pnode = self.get_existing_propnode(prop, level)
        if pnode is not None:
            return pnode
        pnode = PropNode(prop, level)
        self.propLevels[level].append(pnode)
        return pnode

    def solve(self):
        while not self.terminate():
            self.extend_graph_level()
            goals = [self.get_existing_propnode(g, self.level+1)
                     for g in self.goals]
            if None in goals:
                print('Some goal props not instantiated at level %d'
                      % (self.level+1))
            elif self.mutually_exclusive(goals):
                print('Some goals are mutually exclusive at level %d'
                      % (self.level+1))
            else:
                result = self.solve_goals(goals, [], goals, [])
                if result is not None:
                    return result
                else:
                    print('No solution at level %d' % (self.level + 1))

        print('Problem has no solution!')
        return None

    '''
    solve_goals will recurse on the tail of the goals_remaining, but we
    still need to keep the complete goal set around for the 
    minimal_action_set test
    '''

    def solve_goals(self, goals, goals_remaining, new_goals, selected_actions):
        # time to advance to the next level?
        if len(goals_remaining) == 0:
            if new_goals[0].level == 0:
                print('Solution found at level %d' % (self.level + 1))
                return selected_actions
            else:
                new_goals.sort()
                new_goals = tuple(new_goals) # needs to be a hashable type!
                if self.unsolvable_goalsets[new_goals[0].level]\
                       .get(new_goals,None):
                    return None
                result = self.solve_goals(new_goals, new_goals,
                                     [], [[]] + selected_actions)
                if result is not None:
                    return result
                else:
                    # no action solves this goal set, so mark as unsolvable
                    self.unsolvable_goalsets\
                        [new_goals[0].level][new_goals] = True
                    return None

        # Work on the next goal at the current level
        goal = goals_remaining[0]
        actions = goal.adders
        for a in actions:
            # Make sure this action isn't excluded by any actions already selected
            if safeIndex(selected_actions[0], lambda s: a in s.excludes) is None:
                new_actions = [selected_actions[0] + [a]] + selected_actions[1:]
                if ((not self.forward_cutoff(goals_remaining[1:], new_actions[0]))
                    and self.minimal_action_set(goals, new_actions[0])):
                    next_goals_remaining = [g for g in goals_remaining
                                            if g not in a.adds]
                    next_new_goals = new_goals + [g for g in a.precs if
                                                  g not in new_goals]
                    result = self.solve_goals(goals, next_goals_remaining,
                                         next_new_goals, new_actions)
                    if result is not None:
                        return result

        return None

    def mutually_exclusive(self, goals):
        '''
        Return True if any two goals are mutually exclusive
        '''
        for i in range(len(goals)):
            g1 = goals[i]
            for j in range(i+1, len(goals)):
                g2 = goals[j]
                if g2 in g1.excludes:
                    return True
        return False

    def forward_cutoff(self, goals, actions):
        '''
        Return True if some goals has been cut off by this aciton set,
        i.e. every action that could achieve it has been excluded
        '''
        for g in goals:
            possible_achievers = g.adders
            for a in actions:
                possible_achievers = [
                    a for a in possible_achievers
                    if a not in a.excludes
                ]
                if len(possible_achievers) == 0:
                    return True
        return False

    def minimal_action_set(self, goals, actions):
        '''
        Return False if removing any one action still satisfies all the goals.
        This can happen if actions have overlapping effects
        '''
        for a in actions:
            to_be_achieved = goals
            reduced_actions = [a2 for a2 in actions if a2 != a]
            for a2 in reduced_actions:
                to_be_achieved = [a3 for a3 in to_be_achieved
                                  if a3 not in a2.adds]
                if len(to_be_achieved) == 0:
                    print('Non-minimal action set:', actions)
                    return False
        return True

    def terminate(self):
        if not self.leveled_off():
            return False
        elif (len(self.unsolvable_goalsets[-1]) !=
              len(self.unsolvable_goalsets[-2])):
            
            return False
        return True

    def dump(self):
        for level in range(len(self.propLevels)):
            print(('*'*16) + (' Level %d ' % self.level) + ('*'*16))
            print('Proposition nodes: (' + str(len(self.propLevels[level])) + ')')
            self.propLevels[level].sort()
            for p in self.propLevels[level]:
                pname = str(p)
                print('  ' + pname)
                if (len(p.excludes) > 0):
                    print(' excl (%d)'  % len(p.excludes))
                    for e in p.excludes:
                        print(' %d' % (e.prop.propnum))
                print('\n')

            if level < len(self.actionLevels):
                print('Action nodes: (%d)' % len(self.actionLevels[level]))
                for a in self.actionLevels[level]:
                    aname = str(a)
                    print('  ' + aname)
                    if len(a.excludes) > 0:
                        print(' excl (%d):' % len(a.excludes))
                        for e in a.excludes:
                            print(' %d' % e.number)
                    print('\n')
            print

        return None
