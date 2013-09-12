# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 18:09:26 2013

@author: jinpeng
"""


import numpy as np
import random
from epac import LocalEngine
from epac import ColumnSplitter
from mulm.models import MUOLS
from mulm.models import MUOLSStats

print "jinpeng pt1"
n_samples = 10
n_xfeatures = 20
n_yfeatures = 15
x_n_groups = 3
y_n_groups = 2

print "jinpeng pt2"
X = np.random.randn(n_samples, n_xfeatures)
Y = np.random.randn(n_samples, n_yfeatures)
x_group_indices = np.array([random.randint(0, x_n_groups)\
    for i in xrange(n_xfeatures)])
#    y_group_indices = np.array([random.randint(0, y_n_groups)\
#        for i in xrange(n_yfeatures)]) 
y_group_indices = np.zeros(n_yfeatures)

print "jinpeng pt3"
# 1) Prediction for each X block return a n_samples x n_yfeatures
mulm = ColumnSplitter(MUOLS(), x_group_indices, y_group_indices)
# mulm.run(X=X, Y=Y)
local_engine = LocalEngine(tree_root=mulm, num_processes=2)
mulm = local_engine.run(X=X, Y=Y)

print "jinpeng pt4"
for leaf in mulm.walk_leaves():
    print "===============leaf.load_results()================="
    print "key =", leaf.get_key()
    tab = leaf.load_results()
    print tab["MUOLS"]['Y/pred']

#print "jinpeng pt5"
## 1) Prediction for each X block return a n_samples x n_yfeatures
#mulm_stats = ColumnSplitter(MUOLSStats(), x_group_indices, y_group_indices)
##mulm_stats.run(X=X, Y=Y)
#local_engine = LocalEngine(tree_root=mulm_stats, num_processes=2)
#mulm_stats = local_engine.run(X=X, Y=Y)
#for leaf in mulm_stats.walk_leaves():
#    print "===============leaf.load_results()================="
#    print "key =", leaf.get_key()
#    tab = leaf.load_results()
#    print tab["MUOLSStats"]
