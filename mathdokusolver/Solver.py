'''
MathDoku solver module.
@author: Radian Baskoro
'''

import itertools
from datetime import datetime
from Utility import Utility

class Solver:
    '''
    Solver class used to solve the MathDoku problem.
    '''
        
    __debugLevel = 0
    __iterationCount = 0
    
    __initFlag = False
    
    boardSize = 0
    groups = None

    def __init__(self, debugLevel=2):
        '''
        Constructor for Solver class.
        Accepts debugLevel:
        0 - No debug information
        1 - Number of iterations and elapsed time only
        2 - All information        
        '''
        
        self.__debugLevel = debugLevel
    
    def initializeFromFile(self, filePath):
        '''
        Initializes the problem from file.
        '''
        
        inputDataFile = open(filePath, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        
        self.initialize(inputData)
    
    def initialize(self, inputData):
        '''
        Initializes the problem from string.
        '''
        
        lines = inputData.split('\n')
        
        parts = lines[0].split()
        
        self.boardSize = int(parts[0])
        groupsCount = int(parts[1])
        self.groups = [None]*groupsCount
        
        try:
            for i in range(self.boardSize+1, self.boardSize+groupsCount+1):
                parts = lines[i].split()
                
                g = Group()
                g.op = parts[1]
                g.value = int(parts[2])
                
                self.groups[int(parts[0])] = g
            
            for i in range(0, self.boardSize):
                parts = lines[i+1].split()
                
                for j in range(0, self.boardSize):
                    groupIndex = int(parts[j])
                    self.groups[groupIndex].boxes.append([i,j])
            
        except Exception:
            raise InputError('Expecting board size of %d and %d groups.' % (self.boardSize, groupsCount))
        
        self.__validate()
        self.__initFlag = True 
        
    def solve(self):
        '''
        Solves the initialized problem.
        Returns the solution in a 2 dimensional list or None if no solution is found.
        '''
        
        if not self.__initFlag: raise SolverError('Solver not initialized')
        
        startTime = datetime.now()
        
        domain = [[range(1, self.boardSize+1) for y in range(0, self.boardSize)] for x in range(0, self.boardSize)]
        conf = [[None]*self.boardSize for x in range(0, self.boardSize)]
        
        for g in self.groups:
            # First pass - assign all single cell groups
            if len(g.boxes) == 1:
                x = g.boxes[0][0]
                y = g.boxes[0][1]
                self.__setValue(domain, conf, x, y, g.value)
        
            # Second pass - heuristics
            # Group using multiplication operation: domains must be a factor of the group value
            elif g.op == Op.MULTIPLICATION:
                for box in g.boxes:
                    x = box[0]
                    y = box[1]
                    
                    toRemove = set()
                    
                    for d in domain[x][y]:
                        if g.value % d != 0:
                            toRemove.add(d)
                    
                    domain[x][y] = list(set(domain[x][y])-toRemove)
        
        # Propagating constraints also removes all infeasible number combinations from each group
        self.__propagateConstraints(domain, conf)
        
        # Third pass - greedy
        tree = SolverNode(domain, conf)
        if self.__solveTree(tree):
            if self.__debugLevel >= 1:
                elapsedTime = datetime.now() - startTime
                
                print 'Solved in %d iterations.' % self.__iterationCount
                print 'Elapsed time: %d seconds %d microseconds' % \
                    (elapsedTime.seconds, elapsedTime.microseconds) 
            
            return tree.conf
        else:
            if self.__debugLevel >= 1:
                print 'No solution found.'
            
            return None
    
    def __solveTree(self, node):
        '''
        Recursively solve the problem tree.
        '''
        
        self.__iterationCount += 1
        if self.__debugLevel >= 2:
            print '----------------'
            print 'Iteration %d' % self.__iterationCount
            print '----------------'
            Utility.printSolution(node.conf)
        
        # Assign next value, and check constraints
        if node.value != None:
            self.__setValue(node.domain, node.conf, node.x, node.y, node.value)
            if not ConstraintStore.checkConstraints(self.boardSize, self.groups, node.domain, node.conf, debugLevel=self.__debugLevel):
                return False
        
        # Done if all boxes are assigned
        unassignedBoxes = filter(lambda x: node.conf[x[0]][x[1]] == None, itertools.product(range(0, self.boardSize), range(0, self.boardSize)))
        if len(unassignedBoxes) == 0:
            if self.__debugLevel >= 2: print 'Solution found!'
            return True
        
        # Get next box
        unassignedBoxes = sorted(unassignedBoxes, key=lambda x: len(node.domain[x[0]][x[1]]))
        box = unassignedBoxes[0]
        x = box[0]
        y = box[1]
        
        # Try each domain value
        for value in node.domain[x][y]:
            childNode = SolverNode(node.domain, node.conf, x, y, value)
            if self.__solveTree(childNode):
                node.domain = childNode.domain
                node.conf = childNode.conf
                return True
        
        # No solution found in this subtree
        return False
    
    def __setValue(self, domain, conf, x, y, value):
        '''
        Sets the value at the given location and propagate constraints.
        '''
        
        conf[x][y] = value
        domain[x][y] = [value]
        
        if self.__debugLevel >= 2: print '(%d,%d) = %d' % (x, y, value)
        
        self.__propagateConstraints(domain, conf, x=x, y=y, value=value)
    
    def __propagateConstraints(self, domain, conf, x=None, y=None, value=None):
        '''
        Limits the domain values based on the known constraints.
        '''
        
        removeCount = 0
        
        if x != None and y != None and value != None:
            for i in range(0, self.boardSize):
                if y != i:
                    # Propagate to row
                    d = domain[x][i]
                    if value in d:
                        removeCount += 1
                        d.remove(value)
                        if len(d) == 1:
                            self.__setValue(domain, conf, x, i, d[0])
                
                if x != i:
                    # Propagate to column
                    d = domain[i][y]
                    if value in d:
                        removeCount += 1
                        d.remove(value)
                        if len(d) == 1:
                            self.__setValue(domain, conf, i, y, d[0])
        
        # Propagate to all groups 
        for group in self.groups:
            boxCount = len(group.boxes)
            if len(group.boxes) > 1:
                # Try every possible combination of the domain of each boxes
                # and only keep feasible values
                d = tuple(map(lambda box: domain[box[0]][box[1]], group.boxes))
                feasibleDomain = [set() for x in range(0, boxCount)]
                
                comb = list(itertools.product(*d))
                
                for c in comb:
                    groupCalcValue = group.func(*c)
                    if float(group.value) == groupCalcValue:
                        for i in range(0, boxCount):
                            feasibleDomain[i].add(c[i])
                
                for i in range(0, boxCount):
                    box = group.boxes[i]
                    x = box[0]
                    y = box[1]
                    
                    newDomain = list(set(domain[x][y])&feasibleDomain[i])
                    removeCount += len(domain[x][y])-len(newDomain) 
                    domain[x][y] = newDomain
        
        if self.__debugLevel >= 2: print "%d infeasible values removed from the domain." % removeCount
    
    def __validate(self):
        '''
        Initial validation of the problem.
        '''
        
        # All groups' cells must be attached to one another.
        for i in range(0, len(self.groups)):
            g = self.groups[i]
            
            if len(g.boxes) > 1:
                valid = [False]*len(g.boxes)
                
                for i in range(0, len(g.boxes)):
                    if not valid[i]:
                        c1 = g.boxes[i]
                        
                        for j in range(0, len(g.boxes)):
                            c2 = g.boxes[j]
                            
                            if abs(c1[0]-c2[0])+abs(c1[1]-c2[1]) == 1:
                                valid[i] = True
                                valid[j] = True
                        
                if False in valid: raise InputError ('Group #%d cells are not attached.' % i)
            
            # Check valid group operation
            if not g.op in [Op.ADDITION, Op.SUBTRACTION, Op.MULTIPLICATION, Op.DIVISION]: raise InputError ('Invalid operation in group #%d: %s' % (i, g.op))    

class Group:
    '''
    Represents a group of MathDoku boxes with an operation and value.
    '''
    
    boxes = None
    op = None
    value = None
    
    def __init__(self):
        self.boxes = list()
    
    def func(self, *n):
        '''
        Executes the group function on the given values tuple.
        '''
        
        values = sorted(n, reverse=True)
        value = float(values[0])
        
        for v in values[1:]:
            if self.op == Op.ADDITION: value += v
            elif self.op == Op.SUBTRACTION: value -= v
            elif self.op == Op.MULTIPLICATION: value *= v
            elif self.op == Op.DIVISION: value /= v
        
        return value
    
class Op:
    '''
    Valid operators enumeration.
    '''
    
    ADDITION = '+'
    SUBTRACTION = "-"
    MULTIPLICATION = '*'
    DIVISION = '/'

class SolverNode:
    '''
    Represents the solver tree node.
    '''
    
    domain = None
    conf = None
    x = None
    y = None
    value = None
    
    def __init__(self, domain, conf, x=None, y=None, value=None):
        self.domain = list()
        self.conf = list()
        
        for i in range(0, len(domain)):
            dRow = list()
            cRow = list(conf[i])
            
            for j in range(0, len(domain)):
                dRow.append(list(domain[i][j]))
            
            self.domain.append(dRow)
            self.conf.append(cRow)
        
        self.x = x
        self.y = y
        self.value = value

class ConstraintStore:
    '''
    Constraint store static class for checking feasibility.
    '''
    
    @staticmethod
    def checkConstraints(boardSize, groups, domain, conf, debugLevel=0):
        '''
        Returns true if none of the constraints are broken, false otherwise.
        '''
        
        completeDomain = set(range(1, boardSize+1))
        
        for i in range(0, boardSize):
            rowUsed = list()
            colUsed = list()
            rowDomain = set()
            colDomain = set()
            
            for j in range(0, boardSize):
                # 1 - Row values are all different
                value = conf[i][j]
                if value != None:
                    if value in rowUsed:
                        if debugLevel >= 2: print 'Row #%d constraint violated.' % i
                        return False
                    else:
                        rowUsed.append(value)
                
                # 2 - Column values are all different
                value = conf[j][i]
                if value != None:
                    if value in colUsed:
                        if debugLevel >= 2: print 'Column #%d constraint violated.' % i
                        return False
                    else:
                        colUsed.append(value)
            
                rowDomain = rowDomain.union(set(domain[i][j]))
                colDomain = colDomain.union(set(domain[j][i]))
            
            #3 - Row must contain all numbers
            if rowDomain != completeDomain:
                if debugLevel >= 2: print 'Row #%i domain constraint violated.' % i
                return False
            
            #4 - Column must contain all numbers
            if colDomain != completeDomain:
                if debugLevel >= 2: print 'Column #%i domain constraint violated.' % i
                return False
            
        
        # 3 - Group calculation is correct
        for i in range(0, len(groups)):
            group = groups[i]
            
            values = tuple(map(lambda x: conf[x[0]][x[1]], group.boxes))
            
            if not None in values:
                groupCalcValue = group.func(*values)
                
                if float(group.value) != groupCalcValue:
                    if debugLevel >= 2: print 'Group #%d constraint violated.' % i
                    return False 
        
        return True

class InputError(Exception):
    '''
    Represents an error in the problem space.
    '''
    
    def __init__(self, message):
        self.message = message

class SolverError(Exception):
    '''
    Represents an error in the solver.
    '''
    
    def __init__(self, message):
        self.message = message