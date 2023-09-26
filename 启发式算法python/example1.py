
# -*- coding: utf-8 -*-

'''
======================================
|           kiterun                  |
|          2017/08/11                |
|        kiterun@126.com             |
======================================
'''

from random import random
import math
import sys
from time import time
from simAnneal_dev import SimAnneal
from simAnneal_dev import OptSolution
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def func(w):
    x, = w
    fx = x + 10*math.sin(5*x) + 7*math.cos(4*x)
    return fx

def func2(w):
    x, y = w
    fxy = y*np.sin(2*np.pi*x) + x*np.cos(2*np.pi*y)
    return fxy

if __name__ == '__main__':

    targ = SimAnneal(target_text='max')
    init = -sys.maxsize # for maximun case
    #init = sys.maxsize # for minimun case
    xyRange = [[-2, 2], [-2, 2]]
    xRange = [[0, 10]]
    t_start = time()

    calculate = OptSolution(Markov_chain=1000, result=init, val_nd=[0,0])
    output = calculate.soulution(SA_newV=targ.newVar, SA_juge=targ.juge, 
                        juge_text='max',ValueRange=xyRange, func=func2)

    '''
    with open('out.dat', 'w') as f:
        for i in range(len(output)):
            f.write(str(output[i]) + '\n')
    '''
    t_end = time()
    print('Running %.4f seconds' %(t_end-t_start))