# -*- coding: utf-8 -*-
#!/usr/bin/env python
# Theano tutorial
# Solution to Exercise in section 'Baby Steps - Algebra'

import theano as T
import numpy as np
import time

###Define a function
###============class RidgeRegression in pylearn-structured
print '''============Theano links=================='''
print "Tutorial http://deeplearning.net/software/theano/tutorial/"\
      "adding.html#adding-two-matrices"
print "Shared Variables http://deeplearning.net/software/theano/tutorial"\
      "/examples.html#using-shared-variables"
print "http://deeplearning.net/software/theano/tutorial/"\
      "using_gpu.html#what-can-be-accelerated-on-the-gpu"


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

np_rows = 500
coef = np.float32(3.0)
n_it = 100

np_X = np.random.rand(np_rows, np_rows).astype(np.float32)
print "    np_X=" + repr(np_X.shape)
print "    coef=" + repr(coef)

X = T.shared(np_X, name="X")
c = T.tensor.fscalar('c')
z = X ** c
f = T.function([c], z)


###Using CPU
start_time = time.time()
for i in range(n_it):
    res_cpu = np_X ** coef
print "CPU, time elapsed=" + \
        repr(time.time() - start_time) + \
        " seconds"

###Using GPU (share x)
start_time = time.time()
for i in range(n_it):
    res_gpu = f(coef)
print "GPU (share x), time elapsed=" + \
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
np_l = np.float32(np.random.uniform(0.1,3))

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
#============Theano links==================
#Tutorial http://deeplearning.net/software/theano/tutorial/adding.html#adding-two-matrices
#Shared Variables http://deeplearning.net/software/theano/tutorial/examples.html#using-shared-variables
#http://deeplearning.net/software/theano/tutorial/using_gpu.html#what-can-be-accelerated-on-the-gpu
#====================Square Matrix dot product===================
#Function = np.dot(np_X, np_Y)
#    np_X=(5000, 5000)
#    np_Y=(5000, 5000)
#CPU, time elapsed=34.19604301452637 seconds
#GPU, time elapsed=11.002487897872925 seconds
#=======Matrix (#rows << #cols) dot Matrix (#cols >> #rows)=======
#Function = np.dot(np_X, np_Y)
#    np_X=(500, 50000)
#    np_Y=(50000, 1)
#CPU, time elapsed=0.01610708236694336 seconds
#GPU, time elapsed=0.07469987869262695 seconds
#======================Matrix element power======================
#Function = np_X ** coef
#    np_X=(500, 500)
#    coef=3.0
#CPU, time elapsed=2.383635997772217 seconds
#GPU (share x), time elapsed=0.11840295791625977 seconds
#===def f(self, beta, **kwargs): in RidgeRegression==============
#Function = np.sum((np_y - np.dot(np_X, np_beta)) ** 2.0) + np_l * np.sum(np_beta ** 2.0)
#    np_X=(500, 50000)
#    np_beta=(50000, 1)
#    np_y=(500, 1)
#    np_l=1.2523935
#CPU, time elapsed=0.9669821262359619 seconds
#GPU, time elapsed=6.189702987670898 seconds
#GPU (element-wise op) + CPU (dot and sum), time elapsed=1.018022060394287 seconds
#GPU (element-wise op, dot) + CPU (sum), time elapsed=6.414769887924194 seconds
#GPU (element-wise op, share y) + CPU (dot and sum), time elapsed=1.185986042022705 seconds
#GPU (element-wise op, dot, share x y) + CPU (sum), time elapsed=3.0201029777526855 seconds
#GPU (share x y l), time elapsed=2.973874092102051 seconds
