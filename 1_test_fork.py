# -*- coding: utf-8 -*-

import os
import numpy as np
import time


def child(test_mat):
    print 'A new child', os.getpid()
    print np.sum(test_mat)
    time.sleep(5)
    os._exit(0)


def parent():
    test_mat = np.random.random((1, 100000000))
    print np.sum(test_mat)
    while True:
        time.sleep(5)
        newpid = os.fork()
        if newpid == 0:
            child(test_mat)
        else:
            pids = (os.getpid(), newpid)
            print "parent : %d, child %d" % pids
        if raw_input() == "q":
            break

if __name__ == "__main__":
    parent()
