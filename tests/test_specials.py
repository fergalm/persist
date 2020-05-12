# -*- coding: utf-8 -*-

# from ipdb import set_trace as idebug
import pandas as pd
import numpy as np

from persist import specials
from persist import persist

def test_nonetype():
    x = None
    obj = specials.NonetypePersistable().to_dict(x)
    print(obj)
    persist.validate_dict(obj)

    x = specials.NonetypePersistable().from_dict(obj)
    assert x is None


def test_boolean():
    x = True
    obj = specials.BasicPersistable().to_dict(x)
    persist.validate_dict(obj)
    y = specials.BasicPersistable().from_dict(obj)
    assert x == y

def test_basic_float():
    x = 5.5

    obj = specials.BasicPersistable().to_dict(x)
    persist.validate_dict(obj)
    print(obj)
    y = specials.BasicPersistable().from_dict(obj)
    assert x == y

def test_basic_str():
    x = 'Raised on songs and stories'

    obj = specials.BasicPersistable().to_dict(x)
    persist.validate_dict(obj)
    y = specials.BasicPersistable().from_dict(obj)
    assert x == y


def test_func():
    obj = specials.FunctionPersistable().to_dict(test_basic_str)
    print(obj)
    persist.validate_dict(obj)
    f2 = specials.FunctionPersistable().from_dict(obj)
    assert f2 == test_basic_str


# def test_set():
#     assert False


def test_numpy1():
    x = np.arange(5, dtype=int)
    obj = specials.NumpyPersistable().to_dict(x)
    persist.validate_dict(obj)
    y = specials.NumpyPersistable().from_dict(obj)

    x = np.arange(24, dtype=int).reshape((4,6))
    obj = specials.NumpyPersistable().to_dict(x)
    print(obj)
    persist.validate_dict(obj)
    y = specials.NumpyPersistable().from_dict(obj)

    assert x.shape == y.shape
    assert np.all(x == y)


def test_numpy2():
    x = np.arange(24, dtype=float).reshape(4,6)

    obj = specials.NumpyPersistable().to_dict(x)
    persist.validate_dict(obj)
    y = specials.NumpyPersistable().from_dict(obj)
    assert np.all(x == y)




def test_pandas_dataframe():
    df = pd.DataFrame(columns="a b c".split())
    df['a'] = "one two three four five".split()
    df['b'] = np.arange(5) + 5.5
    df['c'] = pd.date_range("2010-01-01", "2010-01-05", freq="D")
    df.index = np.arange(5)

    obj = specials.PandasPersistable().to_dict(df)
    persist.validate_dict(obj)
    df2 = specials.PandasPersistable().from_dict(obj)

    assert len(df) == len(df2)
    assert all(df.columns == df2.columns)
    assert all(df.index  == df2.index)

    #Datetimes aren't properly persisted
    for col in 'a b'.split():
        assert all(df[col] == df2[col]), "%s %s %s" %(col, df[col], df2[col])
