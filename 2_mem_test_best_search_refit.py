# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 13:43:36 2013

@author: jinpeng
"""

from sklearn import datasets
from sklearn.svm import SVC
from epac import CV, Methods, CVBestSearchRefit
from epac import LocalEngine


def test_mem():
    X, y = datasets.make_classification(n_samples=2000,
                                        n_features=10000,
                                        n_informative=2,
                                        random_state=1)
    wf = CVBestSearchRefit(
                Methods(*[SVC(kernel="linear"), SVC(kernel="rbf")]),
                n_folds=10)
    wf.run(X=X, y=y) # Top-down process: computing recognition rates, etc.
    print wf.reduce() # Bottom-up process: computing p-values, etc.

test_mem()



'''

Manually recorded from $ top

Single process:
Memory Consumption (MB):
343 -> 349 -> 472 -> 474 -> 478 -> 479 -> 610 -> 611 -> 613 -> 
617 -> 620 -> 621 -> 623 -> stable (over 5 minutes) 
-> 500 (re-compute tree for short time) -> finish


No multi processes...

'''


