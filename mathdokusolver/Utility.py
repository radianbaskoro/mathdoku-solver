'''
MathDoku solver utility module.
@author: Radian Baskoro
'''

class Utility:
    '''
    Contains static utility methods.
    '''
    
    @staticmethod
    def printSolution(conf):
        '''
        Prints the solution in a grid without the group boundaries.
        '''
        if not conf is None:
            print '='*(len(conf)*2+1)
            for i in range(0, len(conf)):
                print '|' + ' '.join(map(lambda x: ' ' if x == None else str(x), conf[i])) + '|'
            print '='*(len(conf)*2+1)
            print ''
