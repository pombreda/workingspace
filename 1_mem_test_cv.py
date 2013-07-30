# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 13:43:36 2013

@author: jinpeng
"""

from sklearn import datasets
from sklearn.svm import SVC
from epac import CV, Methods
from epac import LocalEngine

@profile
def test_mem():
    X, y = datasets.make_classification(n_samples=2000,
                                        n_features=10000,
                                        n_informative=2,
                                        random_state=1)
    cv_svm = CV(Methods(*[SVC(kernel="linear"), SVC(kernel="rbf")]),
                     n_folds=10)
    cv_svm.run(X=X, y=y) # Top-down process: computing recognition rates, etc.
    # local_engine = LocalEngine(cv_svm, num_processes=2)
    # cv_svm = local_engine.run(X=X, y=y)
    print cv_svm.reduce() # Bottom-up process: computing p-values, etc.

test_mem()

