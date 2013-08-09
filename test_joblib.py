# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 16:00:56 2013

@author: jinpeng
"""

import numpy as np
from joblib import Parallel, delayed
import os.path as path
from tempfile import mkdtemp
from joblib import Memory
import joblib.pool.MemmapingPool
import joblib
import dill as pickle
from multiprocessing import Pool


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

a = np.vander(np.arange(3)).astype(np.float)
a = convert2memmap(a)
dict_data = {}
dict_data['a'] = a
dict_data['b'] = 5

## Fail to dump
## ==========================
f = open("/tmp/a.data", "wb")
pickle.dump(a, f)
f.close()

f = open("/tmp/a.data", "rb")
a = pickle.load(f)
f.close()

## Yes to dump
## ==========================
joblib.dump(a, "/tmp/a.data")
a = joblib.load("/tmp/a.data", "r+")


## Yes to dump
## ==========================
joblib.dump(dict_data, "/tmp/a.data")



def test_func2(path):
    dict_data = joblib.load(path, "r+")
    print "hello"
    return dict_data


p = Pool(2)
p.map(test_func2, ["/tmp/a.data", "/tmp/a.data"])

from joblib import sharedarray
import joblib.pool.MemmapingPool



test_func = mem.cache(test_func)

Parallel(n_jobs=1)(delayed(test_func)(i) for i in [a, a, a])

Parallel(n_jobs=2)(delayed(test_func)(i) for i in [a, a, a])

### Can use with latest version on github
from joblib import Parallel, delayed
import numpy as np
a = np.memmap('/tmp/memmaped', dtype=np.float32, mode='w+', shape=(3, 5))
b = np.memmap('/tmp/memmaped', dtype=np.float32, mode='r', shape=(3, 5))
Parallel(n_jobs=2)(delayed(np.mean)(x) for x in np.array_split(b, 3))

cachedir2 = mkdtemp()
memory2 = Memory(cachedir=cachedir2, mmap_mode='r')
square = memory2.cache(np.square)
a = np.vander(np.arange(3)).astype(np.float)
square(a)