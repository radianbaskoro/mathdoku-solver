'''
MathDoku solver unit tests.
@author: Radian Baskoro
'''
import unittest
from mathdokusolver.Solver import *

class SolverTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    '''
    Initialization tests
    '''
    
    def testInitialization(self):
        i = '3 2\n'
        i += '1 1 1\n'
        i += '1 0 1\n'
        i += '1 1 1\n'
        i += '0 + 3\n'
        i += '1 + 15\n'
        
        s = Solver()
        s.initialize(i)
        
        cage = s.cages[0]
        self.assertEqual(len(cage.cells), 1)
        self.assertIn([1,1], cage.cells)
        self.assertEqual(cage.op, Op.ADDITION)
        self.assertEqual(cage.value, 3)
        
        cage = s.cages[1]
        self.assertEqual(len(cage.cells), 8)
        self.assertIn([0,0], cage.cells)
        self.assertIn([0,1], cage.cells)
        self.assertIn([0,2], cage.cells)
        self.assertIn([1,0], cage.cells)
        self.assertIn([1,2], cage.cells)
        self.assertIn([2,0], cage.cells)
        self.assertIn([2,1], cage.cells)
        self.assertIn([2,2], cage.cells)
        self.assertEqual(cage.op, Op.ADDITION)
        self.assertEqual(cage.value, 15)

    '''
    Validation tests
    '''
    
    def testBoardMustMatchBoardSize(self):
        i = '5 2\n'
        i += '0 0 0 0\n'
        i += '1 1 1 1\n'
        i += '1 1 1 1\n'
        i += '1 1 1 1\n'
        i += '0 + 10\n'
        i += '1 + 30\n'
        
        try:
            s = Solver()
            s.initialize(i)
            self.assertTrue(False, 'Board size does not match')
        except InputError:
            pass
    
    def testCagesMustMatchCageCount(self):
        i = '4 3\n'
        i += '0 0 0 0\n'
        i += '1 1 1 1\n'
        i += '1 1 1 1\n'
        i += '1 1 1 1\n'
        i += '0 + 10\n'
        i += '1 + 30\n'
        
        try:
            s = Solver()
            s.initialize(i)
            self.assertTrue(False, 'Cage count does not match')
        except InputError:
            pass
        
    def testAllCageCellsMustBeAttached(self):
        i = '4 2\n'
        i += '0 0 0 1\n'
        i += '1 1 1 0\n'
        i += '1 1 1 1\n'
        i += '1 1 1 1\n'
        i += '0 + 7\n'
        i += '1 + 33\n'
        
        try:
            s = Solver()
            s.initialize(i)
            self.assertTrue(False, 'Cage cells are not attached')
        except InputError:
            pass
    
    def testInvalidOperations(self):
        i = '3 2\n'
        i += '1 1 1\n'
        i += '1 0 1\n'
        i += '1 1 1\n'
        i += '0 ^ 3\n'
        i += '1 + 15\n'
        
        try:
            s = Solver()
            s.initialize(i)
            self.assertTrue(False, 'Unknown operation')
        except InputError:
            pass
        
class ConstraintStoreTest(unittest.TestCase):
    boardSize = 0
    cages = None

    def setUp(self):
        i = '4 6\n'
        i += '0 0 0 1\n'
        i += '2 2 3 1\n'
        i += '4 2 1 1\n'
        i += '4 2 5 5\n'
        i += '0 * 24\n'
        i += '1 + 10\n'
        i += '2 * 24\n'
        i += '3 + 1\n'
        i += '4 - 1\n'
        i += '5 / 4\n'
        
        '''
        Solution:
        
        '''
        
        s = Solver()
        s.initialize(i)
        
        self.boardSize = s.boardSize
        self.cages = s.cages

    def tearDown(self):
        pass

    '''
    Constraint tests
    '''
    
    def testRowsMustBeAllDifferent(self):
        domain = [[range(0, self.boardSize) for y in range(0, self.boardSize)] for x in range(0, self.boardSize)]
        conf = [[None]*self.boardSize for x in range(0, self.boardSize)]
        
        conf[0][0] = 1
        conf[0][1] = 1
        
        result = ConstraintStore.checkConstraints(self.boardSize, self.cages, domain, conf)
        self.assertFalse(result, 'Rows must be all different')

    
    def testColumnsMustBeAllDifferent(self):
        domain = [[range(0, self.boardSize) for y in range(0, self.boardSize)] for x in range(0, self.boardSize)]
        conf = [[None]*self.boardSize for x in range(0, self.boardSize)]
        
        conf[0][0] = 1
        conf[1][0] = 1
        
        result = ConstraintStore.checkConstraints(self.boardSize, self.cages, domain, conf)
        self.assertFalse(result, 'Columns must be all different')

    def testInvalidAdditionCageCalculation(self):
        domain = [[range(0, self.boardSize) for y in range(0, self.boardSize)] for x in range(0, self.boardSize)]
        conf = [[None]*self.boardSize for x in range(0, self.boardSize)]
        
        conf[0][0] = 1
        conf[0][1] = 2
        conf[0][2] = 3
        
        result = ConstraintStore.checkConstraints(self.boardSize, self.cages, domain, conf)
        self.assertFalse(result, 'Addition cage calculation is invalid')
        
if __name__ == '__main__':
    unittest.main()