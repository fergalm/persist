# -*- coding: utf-8 -*-

# from ipdb import set_trace as idebug

from persist import specials
from persist import funcs

def test_get_class_string():
    strr = funcs.get_class_string(specials.NonetypePersistable())

    assert strr == 'persist.specials.NonetypePersistable', strr


