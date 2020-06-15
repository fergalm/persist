# -*- coding: utf-8 -*-

# from ipdb import set_trace as idebug
from pdb import set_trace as debug

from persist.persist import  create_metadata
from persist import handler
import logging
import os

def func_pass(a, b, c=None):
    return True

def test_pick_persistable_filename():
    fn = handler.pick_persistable_filename('.', func_pass)

    tokens = "_".join(fn.split('_')[:4])
    assert tokens == "./test_handler_func_pass"

    f = lambda x: x+1
    fn = handler.pick_persistable_filename('path', f)
    tokens = "_".join(fn.split('_')[:3])
    assert tokens == "path/test_handler_<lambda>"



def test_persist_state(monkeypatch):

    logger = logging.getLogger(__name__)
    handler.persist_state(logger, '.', func_pass, 1, 2, c=3)


def test_missing_user():
    """Test edge case where env var USER not defined"""

    del os.environ['USER']
    meta = create_metadata()
    assert meta['user'] == 'unknown'
