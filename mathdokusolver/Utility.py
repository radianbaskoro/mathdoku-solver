'''
MathDoku solver utility module.
@author: Radian Baskoro
'''

class Utility:
    '''
    Contains static utility methods.
    '''
    
    @staticmethod
    def formatSolution(conf):
        '''
        Prints the solution in a grid without the group boundaries.
        '''
        
        fsol = ''
        if not conf is None:
            fsol += '='*(len(conf)*2+1) + '\n'
            for i in range(0, len(conf)):
                fsol += '|' + ' '.join(map(lambda x: ' ' if x == None else str(x), conf[i])) + '|\n'
            fsol += '='*(len(conf)*2+1) + '\n'
        
        return fsol
