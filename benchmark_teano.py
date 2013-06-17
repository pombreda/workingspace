# -*- coding: utf-8 -*-
#!/usr/bin/env python
# Theano tutorial
# Solution to Exercise in section 'Baby Steps - Algebra'

import theano as T
import numpy as np
import time

###Define a function
###============class RidgeRegression in pylearn-structured
print '''============class RidgeRegression in pylearn-structured========='''
np_X_rows = 500
np_X_cols = 50000
np_beta_cols = 1

X = T.tensor.fmatrix('X')
beta = T.tensor.fmatrix('beta')
y = T.tensor.fmatrix('y')

z = y - T.dot(X, beta) ** 2
f = T.function([X, beta, y], z)

np_X = np.random.rand(np_X_rows, np_X_cols).astype(np.float32)
np_beta = np.random.rand(np_X_cols, np_beta_cols).astype(np.float32)
np_y = np.random.rand(np_X_rows, np_beta_cols).astype(np.float32)

###Using GPU
start_time = time.time()
for i in range(10):
    res_gpu = f(np_X, np_beta, np_y)
print "GPU, time elapsed=" + \
        repr(time.time() - start_time) + \
        " seconds"

###Using CPU
start_time = time.time()
for i in range(10):
    res_cpu = np_y - np.dot(np_X, np_beta) ** 2
print "CPU, time elapsed=" + \
        repr(time.time() - start_time) + \
        " seconds"

print '''========================Matrix dot product======================'''
np_rows = 5000
np_cols = 5000
n_it = 10

X = T.tensor.fmatrix('X')
Y = T.tensor.fmatrix('Y')
Z = T.dot(X, Y)
f = T.function([X, Y], Z)

np_X = np.random.rand(np_rows, np_cols).astype(np.float32)
np_Y = np.random.rand(np_cols, np_rows).astype(np.float32)

###Using GPU
start_time = time.time()
for i in range(n_it):
    res_gpu = f(np_X, np_Y)
print "GPU, time elapsed=" + \
        repr(time.time() - start_time) + \
        " seconds"

###Using CPU
start_time = time.time()
for i in range(n_it):
    res_cpu = np.dot(np_X, np_Y)
print "CPU, time elapsed=" + \
        repr(time.time() - start_time) + \
        " seconds"


print '''======================Matrix element power======================'''

np_rows = 500
coef = np.float32(3)
n_it = 100

X = T.tensor.fmatrix('X')
c = T.tensor.fscalar('c')
z = X ** c
f = T.function([X, c], z)

np_X = np.random.rand(np_rows, np_rows).astype(np.float32)


###Using GPU
start_time = time.time()
for i in range(n_it):
    res_gpu = f(np_X, coef)
print "GPU, time elapsed=" + \
        repr(time.time() - start_time) + \
        " seconds"

###Using CPU
start_time = time.time()
for i in range(n_it):
    res_cpu = np_X ** coef
print "CPU, time elapsed=" + \
        repr(time.time() - start_time) + \
        " seconds"


#Using gpu device 0: NVS 5200M
#============class RidgeRegression in pylearn-structured=========
#GPU, time elapsed=0.6793129444122314 seconds
#CPU, time elapsed=0.09348702430725098 seconds
#========================Matrix dot product======================
#GPU, time elapsed=21.853296995162964 seconds
#CPU, time elapsed=63.456523180007935 seconds
#======================Matrix element power======================
#GPU, time elapsed=0.14789605140686035 seconds
#CPU, time elapsed=1.943192958831787 seconds
