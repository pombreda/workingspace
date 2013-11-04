# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 22:25:38 2013

@author: jinpeng
"""
import numpy as np
from multiprocessing import Pool
import random
import copy

X = np.random.randn(10, 20)

np.linalg.pinv(X)

def pseudo_inverse(X):
     print "pt 1"
     # Y = np.linalg.pinv(X)
     Xt = np.transpose(X)
     Y = np.dot(np.linalg.inv(np.dot(Xt, X)), Xt)
     print "pt 2"
     return Y

def pseudo_inverse2(X):
     print "2pt 1"
     Z = np.random.randn(20, 20)
     Y = np.dot(X, Z)
     print "2pt 2"
     return Y

pool = Pool(processes=2)
res = pool.map(pseudo_inverse, [X, X, X])
res = pool.map(pseudo_inverse2, [X, X, X])
print res