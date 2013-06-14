# -*- coding: utf-8 -*-
#!/usr/bin/env python
# Theano tutorial
# Solution to Exercise in section 'Baby Steps - Algebra'

import theano as T
import numpy as np
import time
np_X_rows = 500
np_X_cols = 500
np_beta_cols = 5000
###Define a function
X = T.tensor.dmatrix('X')
beta = T.tensor.dmatrix('beta')
y = T.tensor.dmatrix('y')
z = y - T.dot(X, beta) ** 2
f = T.function([X, beta, y], z)

start_time = time.time()
for i in range(50):
    np_X = np.random.rand(np_X_rows, np_X_cols)
    np_beta = np.random.rand(np_X_cols, np_beta_cols)
    np_y = np.random.rand(np_X_rows, np_beta_cols)
    res_gpu = f(np_X, np_beta, np_y)
print "GPU, time elapsed=" + \
        repr(time.time() - start_time) + \
        " seconds"

start_time = time.time()
for i in range(50):
    np_X = np.random.rand(np_X_rows, np_X_cols)
    np_beta = np.random.rand(np_X_cols, np_beta_cols)
    np_y = np.random.rand(np_X_rows, np_beta_cols)
    res_cpu = np_y - np.dot(np_X, np_beta) ** 2
print "CPU, time elapsed=" + \
        repr(time.time() - start_time) + \
        " seconds"