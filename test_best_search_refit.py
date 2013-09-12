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
from epac import CVBestSearchRefitParallel
from epac.sklearn_plugins import Permutations
from epac import range_log2


n_features = int(1E03)
X, y = datasets.make_classification(n_samples=100,
                                    n_features=n_features,
                                    n_informative=2)
random_state = 0
C_values = [1, 10]
k_values = 0
k_max = "auto"
n_folds_nested = 5
n_folds = 10
n_perms = 10

if k_max != "auto":
    k_values = range_log2(np.minimum(int(k_max), n_features),
                          add_n=True)
else:
    k_values = range_log2(n_features, add_n=True)

cls = Methods(*[Pipe(SelectKBest(k=k), SVC(C=C, kernel="linear"))
                           for C in C_values
                           for k in k_values])
pipeline = CVBestSearchRefitParallel(cls,
                             n_folds=n_folds_nested,
                             random_state=random_state)
wf = Perms(CV(pipeline, n_folds=n_folds),
                n_perms=n_perms,
                permute="y",
                random_state=random_state)

# wf.run(X=X, y=y)
# for leaf in wf.walk_leaves():
#     print leaf.load_results()
# wf.reduce()

# from epac.map_reduce.engine import LocalEngine
# local_engine = LocalEngine(tree_root=wf, num_processes=2)
# wf = local_engine.run(X=X, y=y)
# for leaf in wf.walk_leaves():
#     print leaf.load_results()
# wf.reduce()

from epac.map_reduce.engine import SomaWorkflowEngine
sfw_engine = SomaWorkflowEngine(
                        tree_root=wf,
                        num_processes=3,
                        remove_finished_wf=False,
                        remove_local_tree=False)
wf = sfw_engine.run(X=X, y=y)
#for leaf in wf.walk_leaves():
#    print leaf.load_results()
#for node in wf.walk_true_nodes():
#    print node
#    print node.load_results()

print wf.reduce()
