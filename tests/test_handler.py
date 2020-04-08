# -*- coding: utf-8 -*-

# from ipdb import set_trace as idebug
from pdb import set_trace as debug

import logging
import handler

def func_pass(a, b, c=None):
    return True

def test_pick_persistable_filename():
    fn = handler.pick_persistable_filename(func_pass)

    tokens = "_".join(fn.split('_')[:4])
    assert tokens == "test_handler_func_pass"

    f = lambda x: x+1
    fn = handler.pick_persistable_filename(f)
    tokens = "_".join(fn.split('_')[:3])
    assert tokens == "test_handler_<lambda>"



def test_persist_state(monkeypatch):

    logger = logging.getLogger(__name__)
    handler.persist_state(logger, func_pass, 1, 2, c=3)

