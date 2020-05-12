# -*- coding: utf-8 -*-

# from ipdb import set_trace as idebug
from pdb import set_trace as debug
import numpy as np

from persist import persist
import pytest

#Some test objects to save
class Simple(persist.Persistable):
    def __init__(self, var):
        self.var = var

class Foo(persist.Persistable):
    def __init__(self, var):
        self.a = 'Dreamed a dream by the aul canal'
        self.b = np.arange(10, dtype=int)
        self.c = test1
        self.var = var



def test1():

    x = [None, True, 1, 1.1, "one", {1:'one'},
         np.arange(10),
         np.linspace(0, 1, 10)]
    persist.persist_to_file('test.per', x=x)

    obj, meta = persist.restore_from_file('test.per')
    y = obj['x']
    print(meta)
    assert y[0] == None
    assert y[1]
    assert y[2] == 1
    assert y[4] == "one"
    assert y[5][1] == 'one'

    assert meta['func'] == 'test1'
    return y


def test_validate_dict():
    # obj = persist.Persistable()

    x = 5
    d = persist.persist({'x':x})
    assert persist.validate_dict(d)

    x = 'Raise on songs and stories'
    d = persist.persist({'x':x})
    assert persist.validate_dict(d)

    x = [5, 'Raise on songs and stories']
    d = persist.persist({'x':x})
    assert persist.validate_dict(d)

    x = {1:5, 2:'Raise on songs and stories'}
    d = persist.persist({'x':x})
    assert persist.validate_dict(d)

    x = test1
    d = persist.persist({'x':x})
    assert persist.validate_dict(d)


def test_fail_invalid_dict():

    with pytest.raises(ValueError):
        assert persist.validate_dict({'x':True})

    d = {'x':test1} #Passing in an unpersisted object
    with pytest.raises(ValueError):
        assert persist.validate_dict(d)



def test_list():
    a = [1, 'bc', test1, None]

    obj = persist.IterablePersistable().to_dict(a)
    persist.validate_dict(obj)
    b = persist.IterablePersistable().from_dict(obj)

    for aa, bb in zip(a, b):
        assert aa == bb or aa is bb


def test_tuple():
    a = (1, 'bc', test1, None)

    obj = persist.IterablePersistable().to_dict(a)
    persist.validate_dict(obj)
    b = persist.IterablePersistable().from_dict(obj)

    for aa, bb in zip(a, b):
        assert aa == bb or aa is bb




def test_dict():
    a = {'a':1, 'b':'bc', 'c':test1, 'd':None}
    obj = persist.IterablePersistable().to_dict(a)
    print(obj)
    persist.validate_dict(obj)
    b = persist.IterablePersistable().from_dict(obj)

    for k in a:
        assert a[k] == b[k]



def test_set():
    a = set({'a':1, 'b':'bc', 'c':test1, 'd':None})
    # a = {'a':1 } #, 'b':'bc', 'c':test_func, 'd':None}
    obj = persist.IterablePersistable().to_dict(a)
    print(obj)
    persist.validate_dict(obj)
    b = persist.IterablePersistable().from_dict(obj)

    assert a == b





def test_class():
    x = Simple(42)

    obj = persist.persist({'x':x})
    print(obj)
    persist.validate_dict(obj)
    # idebug()
    y = persist.restore(obj)['x']

    # assert x.c == y.c
    assert x.var == y.var


def test_class2():
    x = Foo(42)

    obj = persist.persist({'x':x})
    print(obj)
    persist.validate_dict(obj)
    # idebug()
    y = persist.restore(obj)['x']

    # assert x.c == y.c
    assert x.var == y.var


def test_meta():
    meta = persist.create_metadata()

    for k in "user date format_version func file line".split():
        assert k in meta
        assert isinstance(meta[k], str)

    assert meta['func'] == 'test_meta'
    assert meta['module'] == 'test_persist', meta['module']


def test_non_string_keys():
    x = Simple('c')
    d = {x:3}
    # idebug()
    obj = persist.persist(d)
    print(obj)
    persist.validate_dict(obj)
    persist.persist_to_file('tmp.per', d=d)


def test_datetime():
    """Tests that a datetime object gets converted to a string when string when strict is False"""
    import datetime
    dt = datetime.datetime(2011, 9, 18, 15, 30)

    with pytest.raises(TypeError):
        obj = persist.persist({'dt':dt}, strict=True)

    obj = persist.persist({'dt':dt}, strict=False)

    timestamp = "2011-09-18 15:30:00"
    val = obj['k0'][1]
    assert timestamp == val, val


def test_strict():
    """Test that strict works on nested objects"""
    import datetime
    dt = datetime.datetime(2011, 9, 18, 15, 30)

    aa = ['a', 'b', dt]
    bb = {'d':4, 'e':aa}

    # obj = persist.persist({'dt':bb}, strict=True)

    with pytest.raises(TypeError):
        obj = persist.persist({'dt':bb}, strict=True)

    obj = persist.persist({'dt':bb}, strict=False)
    print(obj)
    timestamp = "2011-09-18 15:30:00"
    val = obj['k0'][1]['k1'][1]['k2']
    assert timestamp == val
