# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 12:23:41 2013

@author: jinpeng

run as:
$ python -m memory_profiler test_multi_processes.py
"""

from multiprocessing import Pool
import numpy as np
import time


# @profile
def test_memo_func(x):
    print np.sum(x)
    time.sleep(5)
    return 1


# @profile
def main_func():
    pool = Pool(processes=2)
    big_matrix = np.random.random((1, 50000000))
    big_matrixes = []    
    for i in xrange(20):
        big_matrixes.append(big_matrix)
    for i in xrange(len(big_matrixes)):
        print np.sum(big_matrix) 
    time.sleep(20)
    res_list = pool.map(test_memo_func, big_matrixes)
    return 0

if __name__ == "__main__":
    main_func()


"""


"""