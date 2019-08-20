#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import os
import unittest

import pytest

from {{cookiecutter.lname}} import api


@pytest.fixture(scope="module")
def istesting():
    api.app.config['TESTING'] = True
    yield api.app.config['TESTING']
    # write here, after yield, any tearDown code


@pytest.mark.usefixtures("dbconn")
class TestTropolink_api(unittest.TestCase):
    """Tests for `tropolink_api` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""
        assert 1 == 1
# vim:set et sts=4 ts=4 tw=80:
