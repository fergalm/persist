# -*- coding: utf-8 -*-

from persist.frozendict import FrozenDict
import pytest

def test_frozen():

    #Test smoke
    dd = FrozenDict({'a':1, 'b':2})
    assert dd['a'] == 1

    dd = FrozenDict({'a':1, 'b':2})
    assert dd['a'] == 1


    with pytest.raises(TypeError):
        dd['a'] = 3

    with pytest.raises(TypeError):
        dd.setdefault('a', 4)

    with pytest.raises(TypeError):
        dd.update({'c':3, 'd':4})

    assert isinstance(hash(dd), int)

    dd = FrozenDict({'a':1, 'b':2, 'c':list(range(5))})
    with pytest.raises(TypeError):
        hash(dd)


def test_frozen_repr():
    dd = FrozenDict({'a':1, 'b':2})

    strr = str(repr(dd))
    assert strr == "F{'a': 1, 'b': 2}"
