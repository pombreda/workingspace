# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 10:48:34 2013

@author: jinpeng
"""


import dill as pickle


class A:
    def __init__(self):
        self.a = 1
        self.b = 2
    def test(self):
        print "hello a"
        self.a = self.a + self.b


class B(A):
    def __init__(self):
        A.__init__(self)
    def test(self):
        print "hello b"
        self.a = self.a + self.b


class C(B):
    def __init__(self):
        B.__init__(self)
    def test(self):
        print "hello c"
        self.a = self.a + self.b


class OA(object):
    def __init__(self):
        self.a = 1
        self.b = 2
    def test(self):
        print "hello oa"
        self.a = self.a + self.b


class OB(OA):
    def __init__(self):
        super(OB, self).__init__()
    def test(self):
        print "hello ob"
        self.a = self.a + self.b


class cadder(object):
    def __init__(self,augend):
        self.augend = augend
        self.zero = [0]
    def __call__(self,addend):
        return addend+self.augend+self.zero[0]


import dill as pickle
from epac.workflow.base import BaseNode
# Cannot dump from object
class OB(BaseNode):
    def __init__(self):
        super(OB, self).__init__()
        self.a = 1
        self.b = 1
    def test(self):
        print "hello ob"
        self.a = self.a + self.b

dump_str = pickle.dumps(OB)
f = open("/tmp/dump_str", "wb")
f.write(dump_str)
f.close()


#Open by another python 
#======================
import dill as pickle
f = open("/tmp/dump_str", "rb")
dump_str = f.read()
f.close()
obj = pickle.loads(dump_str)
obj.test()
