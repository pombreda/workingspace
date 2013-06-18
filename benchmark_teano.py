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
print "Function = np.dot(np_X, np_Y)"
np_rows = 5000
np_cols = np_rows
n_it = 5

X = T.tensor.fmatrix('X')
Y = T.tensor.fmatrix('Y')
Z = T.dot(X, Y)
f = T.function([X, Y], Z)

np_X = np.random.rand(np_rows, np_cols).astype(np.float32)
np_Y = np.random.rand(np_cols, np_rows).astype(np.float32)
print "    np_X=" + repr(np_X.shape)
print "    np_Y=" + repr(np_Y.shape)


###Using CPU
start_time = time.time()
for i in range(n_it):
    res_cpu = np.dot(np_X, np_Y)
print "CPU, time elapsed=" + \
        repr(time.time() - start_time) + \
        " seconds"

###Using GPU
start_time = time.time()
for i in range(n_it):
    res_gpu = f(np_X, np_Y)
print "GPU, time elapsed=" + \
        repr(time.time() - start_time) + \
        " seconds"

print '''=======Matrix (#rows << #cols) dot Matrix (#cols >> #rows)======='''
print "Function = np.dot(np_X, np_Y)"
np_X_rows = 500
np_X_cols = 50000
np_Y_rows = np_X_cols
np_Y_cols = 1
nb_it = 1

X = T.tensor.fmatrix('X')
Y = T.tensor.fmatrix('Y')

z = T.dot(X, Y)
f = T.function([X, Y], z)

np_X = np.random.rand(np_X_rows, np_X_cols).astype(np.float32)
np_Y = np.random.rand(np_Y_rows, np_Y_cols).astype(np.float32)
print "    np_X=" + repr(np_X.shape)
print "    np_Y=" + repr(np_Y.shape)



###Using CPU
start_time = time.time()
for i in range(nb_it):
    res_cpu = np.dot(np_X, np_Y)
print "CPU, time elapsed=" + \
        repr(time.time() - start_time) + \
        " seconds"

###Using GPU
start_time = time.time()
for i in range(nb_it):
    res_gpu = f(np_X, np_Y)
print "GPU, time elapsed=" + \
        repr(time.time() - start_time) + \
        " seconds"


print '''======================Matrix element power======================'''
print "Function = np_X ** coef"

np_rows = 5000
coef = np.float32(2.0)
n_it = 100

X = T.tensor.fmatrix('X')
c = T.tensor.fscalar('c')
z = X ** c
f = T.function([X, c], z)

np_X = np.random.rand(np_rows, np_rows).astype(np.float32)
print "    np_X=" + repr(np_X.shape)
print "    coef=" + repr(coef)

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
print "Function = np.sum((np_y - np.dot(np_X, np_beta)) ** 2.0)"\
      " + np_l * np.sum(np_beta ** 2.0)"
np_X_rows = 500
np_X_cols = 50000
np_beta_cols = 1
nb_it = 100

X = T.tensor.fmatrix('X')
beta = T.tensor.fmatrix('beta')
y = T.tensor.fmatrix('y')
l = T.tensor.fscalar('l')

z = T.tensor.sum(y - T.dot(X, beta) ** 2.0) + l * T.tensor.sum(beta ** 2.0)
f = T.function([X, beta, y, l], z)

np_X = np.random.rand(np_X_rows, np_X_cols).astype(np.float32)
np_beta = np.random.rand(np_X_cols, np_beta_cols).astype(np.float32)
np_y = np.random.rand(np_X_rows, np_beta_cols).astype(np.float32)
np_l = np.float32(2.0)

print "    np_X=" + repr(np_X.shape)
print "    np_beta=" + repr(np_beta.shape)
print "    np_y=" + repr(np_y.shape)
print "    np_l=" + repr(np_l)



###Using CPU
start_time = time.time()
for i in range(nb_it):
    res_cpu = np.sum((np_y - np.dot(np_X, np_beta)) ** 2.0) \
              + np_l * np.sum(np_beta ** 2.0)
print "CPU, time elapsed=" + \
        repr(time.time() - start_time) + \
        " seconds"

###Using GPU
start_time = time.time()
for i in range(nb_it):
    res_gpu = f(np_X, np_beta, np_y, np_l)
print "GPU, time elapsed=" + \
        repr(time.time() - start_time) + \
        " seconds"
        
###Using GPU (element-wise op) + CPU (dot and sum)
y = T.tensor.fmatrix('y')
beta = T.tensor.fmatrix('beta')
X_dot_beta = T.tensor.fmatrix('X')

z1 = (y - X_dot_beta) ** np.float32(2.0)
z2 = beta ** np.float32(2.0)
f1 = T.function([y, X_dot_beta], z1)
f2 = T.function([beta], z2)

start_time = time.time()
for i in range(nb_it):
    np_X_dot_beta = np.dot(np_X, np_beta)
    res_gpu_cpu = np.sum(f1(np_y, np_X_dot_beta)) \
              + np_l * np.sum(f2(np_beta))
print "GPU (element-wise op) + CPU (dot and sum), time elapsed=" + \
        repr(time.time() - start_time) + \
        " seconds"

###Using GPU (element-wise op, dot) + CPU (sum)
X = T.tensor.fmatrix('X')
y = T.tensor.fmatrix('y')
beta = T.tensor.fmatrix('beta')
X_dot_beta = T.tensor.fmatrix('X')

z1 = (y - T.tensor.dot(X,beta)) ** np.float32(2.0)
z2 = beta ** np.float32(2.0)
f1 = T.function([X, y, beta], z1)
f2 = T.function([beta], z2)

start_time = time.time()
for i in range(nb_it):
    res_gpu_cpu = np.sum(f1(np_X, np_y, np_beta)) \
              + np_l * np.sum(f2(np_beta))
print "GPU (element-wise op, dot) + CPU (sum), time elapsed=" + \
        repr(time.time() - start_time) + \
        " seconds"
        
###Using GPU (element-wise op, share y) + CPU (dot and sum)
y = T.shared(np_y, name="y")
beta = T.tensor.fmatrix('beta')
X_dot_beta = T.tensor.fmatrix('X')

z1 = (y - X_dot_beta) ** np.float32(2.0)
z2 = beta ** np.float32(2.0)
f1 = T.function([X_dot_beta], z1)
f2 = T.function([beta], z2)

start_time = time.time()
for i in range(nb_it):
    np_X_dot_beta = np.dot(np_X, np_beta)
    res_gpu_cpu = np.sum(f1(np_X_dot_beta)) \
              + np_l * np.sum(f2(np_beta))
print "GPU (element-wise op, share y) + CPU (dot and sum), time elapsed=" + \
        repr(time.time() - start_time) + \
        " seconds"

###Using GPU (element-wise op, dot, share x y) + CPU (sum)
X = T.shared(np_X, name="X")
y = T.shared(np_y, name="y")
beta = T.tensor.fmatrix('beta')
X_dot_beta = T.tensor.fmatrix('X')

z1 = (y - T.tensor.dot(X, beta)) ** np.float32(2.0)
z2 = beta ** np.float32(2.0)
f1 = T.function([beta], z1)
f2 = T.function([beta], z2)

start_time = time.time()
for i in range(nb_it):
    res_gpu_cpu = np.sum(f1(np_beta)) \
              + np_l * np.sum(f2(np_beta))
print "GPU (element-wise op, dot, share x y) + CPU (sum), time elapsed=" + \
        repr(time.time() - start_time) + \
        " seconds"

###Using GPU (share x y l)
X = T.shared(np_X, name="X")
y = T.shared(np_y, name="y")
l = T.shared(np_l, name="l")
beta = T.tensor.fmatrix('beta')

z = T.tensor.sum(y - T.dot(X, beta) ** 2.0) + l * T.tensor.sum(beta ** 2.0)
f = T.function([beta], z)

start_time = time.time()
for i in range(nb_it):
    res_gpu = f(np_beta)
print "GPU (share x y l), time elapsed=" + \
        repr(time.time() - start_time) + \
        " seconds"


#Using gpu device 0: NVS 5200M
#============What can be accelerated on the gpu==================
#http://deeplearning.net/software/theano/tutorial/using_gpu.html#what-can-be-accelerated-on-the-gpu
#====================Square Matrix dot product===================
#Function = np.dot(np_X, np_Y)
#    np_X=(5000, 5000)
#    np_Y=(5000, 5000)
#CPU, time elapsed=31.066647052764893 seconds
#GPU, time elapsed=10.862936973571777 seconds
#=======Matrix (#rows << #cols) dot Matrix (#cols >> #rows)=======
#Function = np.dot(np_X, np_Y)
#    np_X=(10, 5000)
#    np_Y=(5000, 1)
#CPU, time elapsed=0.00872492790222168 seconds
#GPU, time elapsed=0.010727167129516602 seconds
#======================Matrix element power======================
#Function = np_X ** coef
#    np_X=(500, 500)
#    coef=2.0
#GPU, time elapsed=0.1413729190826416 seconds
#CPU, time elapsed=0.015748977661132812 seconds
#===def f(self, beta, **kwargs): in RidgeRegression==============
#Function = np.sum((np_y - np.dot(np_X, np_beta)) ** 2.0) + np_l * np.sum(np_beta ** 2.0)
#    np_X=(500, 50000)
#    np_beta=(50000, 1)
#    np_y=(500, 1)
#    np_l=1.0
#CPU, time elapsed=0.9139950275421143 seconds
#GPU, time elapsed=6.06090521812439 seconds
#GPU (element-wise op) + CPU (dot and sum), time elapsed=0.9988830089569092 seconds
#GPU (element-wise op, dot) + CPU (sum), time elapsed=6.023119926452637 seconds
