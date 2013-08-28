#!/usr/bin/env python

# -*- coding: utf-8 -*-


from sklearn import datasets
from sklearn.svm import SVC
from epac import Methods
from epac import CV
from epac.workflow.splitters import CVBestSearchRefit
from epac.map_reduce.reducers import ClassificationReport


X, y = datasets.make_classification(n_samples=12,
n_features=10,
n_informative=2,
random_state=1)
n_folds_nested = 2
C_values = [.1, 0.5, 1, 2, 5]
kernels = ["linear", "rbf"]
methods = Methods(*[SVC(C=C, kernel=kernel)
    for C in C_values for kernel in kernels])
sv_node = CV(methods, reducer=ClassificationReport(keep=False))
sv_node.run(X=X, y=y)
sv_node.reduce()

wf = CVBestSearchRefit(methods, n_folds=n_folds_nested)
wf.transform(X=X, y=y)
wf.reduce()
wf.run(X=X, y=y)
wf.reduce()
