# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 16:49:30 2013

@author: jinpeng
"""

import numpy as np
import time

n = 10000
mat1 = np.memmap("/tmp/mat1",
                 dtype='float32',
                 mode='w+',
                 shape=(n, n))

mat2 = np.memmap("/tmp/mat2",
                 dtype='float32',
                 mode='w+',
                 shape=(n, n))

for i in range(0, n):
    for j in range(0, n):
        mat1[j][i] = i * j
        mat2[i][j] = i - j
    print "i=" + repr(i)

start_time = time.time()
np.dot(mat1, mat2)
print "Time elapsed=" + \
        repr(time.time() - start_time) + \
        " seconds"