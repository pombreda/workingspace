#!/usr/bin/env python

# -*- coding: utf-8 -*-

import unittest
import string
import os.path
import numpy as np
from sklearn import datasets
from sklearn.svm import SVC
from sklearn.feature_selection import SelectKBest
from sklearn.cross_validation import StratifiedKFold
from sklearn import grid_search

from epac import Pipe, Methods, CV, Perms
from epac import ClassificationReport, PvalPerms
from epac import StoreFs
from epac import CVBestSearchRefit
from epac.sklearn_plugins import Permutations
from epac.configuration import conf

X, y = datasets.make_classification(n_samples=20,
                                    n_features=10,
                                    n_informative=2)
n_folds = 2
n_folds_nested = 3
k_values = [1, 2]
C_values = [1, 2]
pipelines = Methods(*[
                    Pipe(SelectKBest(k=k),
                    Methods(*[SVC(kernel="linear", C=C)
                    for C in C_values]))
                    for k in k_values])

pipeline = CVBestSearchRefit(pipelines,
                             n_folds=n_folds_nested)

tree_mem = CV(pipeline, n_folds=n_folds,
              reducer=ClassificationReport(keep=False))
# Save Tree
import tempfile
store = StoreFs(dirpath=tempfile.mkdtemp(), clear=True)
tree_mem.save_tree(store=store)
tree_mem.run(X=X, y=y)
tree_mem.reduce()