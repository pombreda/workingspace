#!/usr/bin/env python

# -*- coding: utf-8 -*-


from sklearn import datasets
from sklearn.svm import SVC
from epac import Methods
from epac.workflow.splitters import CVBestSearchRefit2

X, y = datasets.make_classification(n_samples=12,
                                    n_features=10,
                                    n_informative=2,
                                    random_state=1)
n_folds_nested = 2
C_values = [.1, 0.5, 1, 2, 5]
kernels = ["linear", "rbf"]

methods = Methods(*[SVC(C=C, kernel=kernel)
    for C in C_values for kernel in kernels])
wf = CVBestSearchRefit2(methods, n_folds=n_folds_nested)

#wf.run(X=X, y=y)
#for leaf in wf.walk_leaves():
#    print leaf.load_results()
#wf.reduce()

from epac.map_reduce.engine import LocalEngine
local_engine = LocalEngine(tree_root=wf, num_processes=2)
wf = local_engine.run(X=X, y=y)
for leaf in wf.walk_leaves():
    print leaf.load_results()
wf.reduce()

#from epac.map_reduce.engine import SomaWorkflowEngine
#sfw_engine = SomaWorkflowEngine(
#                        tree_root=wf,
#                        num_processes=3,
#                        remove_finished_wf=False,
#                        remove_local_tree=False)
#wf = sfw_engine.run(X=X, y=y)
#for leaf in wf.walk_leaves():
#    print leaf.load_results()
#wf.reduce()
