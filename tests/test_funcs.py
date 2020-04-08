# -*- coding: utf-8 -*-

# from ipdb import set_trace as idebug

import specials
import funcs

def test_get_class_string():
    strr = funcs.get_class_string(specials.NonetypePersistable())

    assert strr == 'specials.NonetypePersistable', strr


