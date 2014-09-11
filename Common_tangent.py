#!usr/bin/env python
'''
'''
from numpy import *
from scipy.optimize import fsolve
import matplotlib.pyplot as plt


PRECISION = 0.01
CIRCLE_1 = ((10,10),1)
CIRCLE_2 = ((5,6),2)

def point_to_point(point_1, point_2):
    '''
    Take the coordinate of two points, 
    return the distance 
    '''
    return sqrt((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)
    
def axes_limits(circle_1, circle_2):
    '''
    Take the two circle,return the axes limits
    '''
    r_max = max(circle_1[1], circle_2[1])
    x_limit = (min(circle_1[0][0], circle_2[0][0]) - r_max - 1, \
    max(circle_1[0][0], circle_2[0][0]) + r_max + 1)
    y_limit = (min(circle_1[0][1], circle_2[0][1]) - r_max - 1, \
    max(circle_1[0][1], circle_2[0][1]) + r_max + 1)
    return x_limit, y_limit

def circle_to_func(circle_1, circle_2):
    '''
    Take two circle with (circle center, radius),
    return the Common Tangent function with (A, B)
    '''
    (x1, y1) = circle_1[0]
    r1 = circle_1[1]
    (x2, y2) = circle_2[0]
    r2 = circle_2[1]
    
    dist = point_to_point(circle_1[0], circle_2[0])
    assert dist > circle_1[1] and dist > circle_2[1], \
    "Containing circle has no common tangent."
    
    return '(k*%f - %f + b) ** 2 - %f**2 * (k**2 + 1)' %(x1,y1,r1),\
    '(k*%f - %f + b) ** 2 - %f**2 * (k**2 + 1)' %(x2,y2,r2)
    
def funcForSolve(x):
    'convert the string of functions to the polynomial'
    k,b = x.tolist()
    func = circle_to_func(CIRCLE_1, CIRCLE_2)
    return [eval(func[0]), eval(func[1])]
    

def solve_func():
    '''
    get the solution of the func,
    return the k,b with [(k1,b1),(k2,b2),...]
    ''' 
    result = []
    klist = linspace(-50, 50, 200)
    blist = linspace(-100, 100, 500)
    (solved_k, solved_b) = (-float('Inf'), -float('Inf'))
    for k in klist:
        for b in blist:
            if k > solved_k:
                (solved_k, solved_b) = fsolve(funcForSolve, [k,b])
                try:
                    delta_k = min([abs(solved_k - item[0]) for item in result])                        
                except(IndexError, ValueError):
                    delta_k = 10 #for first solves
                
                if delta_k > PRECISION:
                    result.append((solved_k, solved_b))
                    break
        if len(result) >= 4:
            break
    return result
    
def argu_to_line(arguments):
    'take the k,b, return the line function'
    result = []
    for (k,b) in arguments:
        result.append("%.4f*x%+.4f" %(k,b))
    return result
        
def line_plot(circle_1, circle_2, line_func):
    'plot the circle and common tangent'
    fig = plt.figure(dpi=120)
    ax = fig.add_subplot(111)
    
    #plot the circle
    circle_plot_1 = plt.Circle(circle_1[0], circle_1[1], fill=False)
    circle_plot_2 = plt.Circle(circle_2[0], circle_2[1], fill=False)
    ax.add_artist(circle_plot_1)
    ax.add_artist(circle_plot_2)
    
    #plot the common line
    limit = axes_limits(circle_1, circle_2)
    x = linspace(limit[0][0], limit[0][1], 100)
    for func in line_func:
        plt.plot(x, eval(func), 'r')
    
    #set the limit of axes
    ax.set_xlim(limit[0])
    ax.set_ylim(limit[1])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    
    plt.show()
    fig.savefig('common_tangent.png', transparent=True, dpi=300)

if __name__ == '__main__':
    '''
    Program begin in funcForSolve.
    '''       
    argument = solve_func()
    func_line = argu_to_line(argument)
    
    for func in func_line:
        print("y=%s" %func)
        
    line_plot(CIRCLE_1, CIRCLE_2, func_line)
    
    
