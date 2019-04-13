#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import os
import unittest

import pytest

from {{cookiecutter.lname}} import api


@pytest.fixture(scope="module")
def dbconn():
    api.app.config['DATABASE_CONN'].close()
    api.app.config['TESTING'] = True
    api.app.config['DATABASE_CONN'] = api.dbconn()
    yield api.app.config['DATABASE_CONN']
    # write here, after yield, any tearDown code


@pytest.mark.usefixtures("dbconn")
class TestTropolink_api(unittest.TestCase):
    """Tests for `tropolink_api` package."""

    def test_000_something(self):
        """Test something."""
        assert 1 == 2
# vim:set et sts=4 ts=4 tw=80:
