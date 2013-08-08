# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 16:00:56 2013

@author: jinpeng
"""

import numpy as np
from joblib import Memory
from joblib import Parallel, delayed
from math import sqrt
import os.path as path
from tempfile import mkdtemp


def convert2memmap(np_mat):
    filename = path.join(mkdtemp(), 'newfile.dat')
    mem_mat = np.memmap(filename,\
                     dtype='float32',\
                     mode='w+',\
                     shape=np_mat.shape)
    mem_mat[:] = np_mat[:]
    return mem_mat


def test_func(X):
    return X

mem = Memory(cachedir='/tmp/joblib')
a = np.vander(np.arange(3)).astype(np.float)
a = convert2memmap(a)

square = mem.cache(np.square)
b = square(a)

Parallel(n_jobs=1)(delayed(test_func)(i) for i in [a, a, a])