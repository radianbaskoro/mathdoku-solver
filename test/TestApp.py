'''
Sample application using the mathdokusolver module.
@author: Radian Baskoro
'''

from mathdokusolver.Solver import Solver
from mathdokusolver.Utility import Utility

if __name__ == '__main__':
    s = Solver(debugLevel=2)
    s.initializeFromFile('data/4_1')
    result = s.solve()
    Utility.printSolution(result)
