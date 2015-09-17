# -*- coding: utf-8 -*-
from lims.extensions import Lims


def test_Lims_init():
    # test that Lims can be initialized without setup
    lims = Lims()
    assert hasattr(lims, 'init_app')
