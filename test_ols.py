# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 19:37:43 2013

@author: edouard.duchesnay@cea.fr
"""


import numpy as np
import random
from mulm.models import OLSRegression

n_samples = 10
n_xfeatures = 20
n_yfeatures = 15
x_n_groups = 3
y_n_groups = 2

X = np.random.randn(n_samples, n_xfeatures)
Y = np.random.randn(n_samples, n_yfeatures)
x_group_indices = np.array([random.randint(0, x_n_groups)\
    for i in xrange(n_xfeatures)])
y_group_indices = np.array([random.randint(0, y_n_groups)\
    for i in xrange(n_yfeatures)])

regression = OLSRegression()
print regression.transform(Y, y_group_indices, X, x_group_indices)
