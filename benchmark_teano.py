# -*- coding: utf-8 -*-
#!/usr/bin/env python
# Theano tutorial
# Solution to Exercise in section 'Baby Steps - Algebra'

import theano as T
import numpy as np
import time

###Define a function
###============class RidgeRegression in pylearn-structured
print '''============What can be accelerated on the gpu=================='''
print "http://deeplearning.net/software/theano/tutorial/\
using_gpu.html#what-can-be-accelerated-on-the-gpu"

print '''====================Square Matrix dot product==================='''
np_rows = 5000
np_cols = np_rows
n_it = 5

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

print '''=======Matrix (#rows << #cols) dot Matrix (#cols >> #rows)======='''
np_X_rows = 10
np_X_cols = 5000
np_Y_rows = np_X_cols
np_Y_cols = 1
nb_it = 1

X = T.tensor.fmatrix('X')
Y = T.tensor.fmatrix('Y')

z = T.dot(X, Y)
f = T.function([X, Y], z)

np_X = np.random.rand(np_X_rows, np_X_cols).astype(np.float32)
np_Y = np.random.rand(np_Y_rows, np_Y_cols).astype(np.float32)

###Using GPU
start_time = time.time()
for i in range(nb_it):
    res_gpu = f(np_X, np_Y)
print "GPU, time elapsed=" + \
        repr(time.time() - start_time) + \
        " seconds"

###Using CPU
start_time = time.time()
for i in range(nb_it):
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

print '''===def f(self, beta, **kwargs): in RidgeRegression=============='''
np_X_rows = 500
np_X_cols = 50000
np_beta_cols = 1
nb_it = 10

X = T.tensor.fmatrix('X')
beta = T.tensor.fmatrix('beta')
y = T.tensor.fmatrix('y')
l = T.tensor.fscalar('l')

z = T.tensor.sum(y - T.dot(X, beta) ** 2.0) + l * T.tensor.sum(beta ** 2.0)
f = T.function([X, beta, y, l], z)

np_X = np.random.rand(np_X_rows, np_X_cols).astype(np.float32)
np_beta = np.random.rand(np_X_cols, np_beta_cols).astype(np.float32)
np_y = np.random.rand(np_X_rows, np_beta_cols).astype(np.float32)
np_l = np.float32(1)

###Using GPU
start_time = time.time()
for i in range(nb_it):
    res_gpu = f(np_X, np_beta, np_y, np_l)
print "GPU, time elapsed=" + \
        repr(time.time() - start_time) + \
        " seconds"

###Using CPU
start_time = time.time()
for i in range(nb_it):
    res_cpu = np.sum((np_y - np.dot(np_X, np_beta)) ** 2.0) \
              + np_l * np.sum(np_beta ** 2.0)
print "CPU, time elapsed=" + \
        repr(time.time() - start_time) + \
        " seconds"

#Using gpu device 0: NVS 5200M
#============What can be accelerated on the gpu==================
#http://deeplearning.net/software/theano/tutorial/using_gpu.html#what-can-be-accelerated-on-the-gpu
#====================Square Matrix dot product===================
#GPU, time elapsed=10.88295602798462 seconds
#CPU, time elapsed=32.93404698371887 seconds
#=======Matrix (#rows << #cols) dot Matrix (#cols >> #rows)=======
#GPU, time elapsed=0.00887298583984375 seconds
#CPU, time elapsed=0.005689144134521484 seconds
#======================Matrix element power======================
#GPU, time elapsed=0.1274881362915039 seconds
#CPU, time elapsed=1.9256629943847656 seconds
#===def f(self, beta, **kwargs): in RidgeRegression==============
#GPU, time elapsed=0.6454651355743408 seconds
#CPU, time elapsed=0.11623001098632812 seconds
##Summation over rows/columns of tensors can be a little slower on the GPU than on the CPU.