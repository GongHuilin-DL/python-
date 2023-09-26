# -*- coding: utf-8 -*-

'''
=========================================
|                kiterun                |
|               2017/08/11              |
|             kiterun@126.com           |
=========================================
'''
from random import random
import math
import sys

class SimAnneal(object):
    '''
    Simulated annealing algorithm 
    '''
    def __init__(self, target_text='min'):
        self.target_text = target_text

    def newVar(self, oldList, T):
        '''
        :old : list
        :return : list, new solutions based on old solutions
        :T   : current temperature
        '''
        newList = [i + (random()*2-1) for i in oldList]
        return newList

    def juge(self, func, new, old, T):
        '''
        matropolise conditions: to get the maximun or minmun
        :new : new solution data from self.newX
        :old : old solution data
        :T   : current temperature

        '''
        dE = func(new) - func(old) if self.target_text == 'max' else func(old) - func(new)
        if dE >= 0:
            x, ans = new, func(new)
        else:
            if math.exp(dE/T) > random():
                x, ans = new,func(new)
            else:
                x, ans = old, func(old)
        return [x, ans]

class OptSolution(object):
    '''
    find the optimal solution.

    '''
    def __init__(self, temperature0=100, temDelta=0.98,
                 temFinal=1e-8, Markov_chain=2000, 
                 result=0, val_nd=[0]):
        # initial temperature
        self.temperature0 = temperature0
        # step factor for decreasing temperature
        self.temDelta = temDelta
        # the final temperature
        self.temFinal = temFinal
        # the Markov_chain length (inner loops numbers)
        self.Markov_chain = Markov_chain
        # the final result
        self.result = result
        # the initial coordidate values: 1D [0], 2D [0,0] ...
        self.val_nd = val_nd

    def mapRange(self, oneDrange):
        return (oneDrange[1]-oneDrange[0])*random() + oneDrange[0]


    def soulution(self, SA_newV, SA_juge, juge_text, ValueRange, func):
        '''
        calculate the extreme value: max or min value
        :SA_newV : function from class SimAnneal().newVar
        :SA_juge : function from class SimAnneal().juge_*
        :ValueRange : [], range of variables, 1D or 2D or 3D...
        :func : target function obtained from user

        '''
        Ti = self.temperature0
        ndim = len(ValueRange)
        f = max if juge_text=='max' else min
        loops =0

        while Ti > self.temFinal:
            res_temp, val_temp = [], []
            preV = [[self.mapRange(ValueRange[j]) for i in range(self.Markov_chain)] for j in range(ndim)]
            newV = [ SA_newV(preV[j], T=Ti) for j in range(ndim)]

            for i in range(self.Markov_chain):
                boolV = True
                for j in range(ndim):
                    boolV &= (ValueRange[j][0]<= newV[j][i] <= ValueRange[j][1])
                if boolV == True:
                    res_temp.append(SA_juge(new=[newV[k][i] for k in range(ndim)], func=func, old=[preV[k][i] for k in range(ndim)], T=Ti)[-1])
                    val_temp.append(SA_juge(new=[newV[k][i] for k in range(ndim)], func=func, old=[preV[k][i] for k in range(ndim)], T=Ti)[0])
                else:
                    continue
                loops += 1

            # get the index of extreme value
            idex = res_temp.index(f(res_temp))
            result_temp = f(self.result, f(res_temp))
            # update the cooordidate of current extrema value 
            self.val_nd = self.val_nd if result_temp == self.result else val_temp[idex]
            # update the extreme value
            self.result = result_temp
            # update the current temperature
            Ti *= self.temDelta
            print(self.val_nd, self.result)

        print(loops)

        #print('The extreme value = %f' %self.result[-1])