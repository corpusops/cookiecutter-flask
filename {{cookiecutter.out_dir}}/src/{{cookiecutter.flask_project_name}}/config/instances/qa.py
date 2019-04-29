#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from ..base import *  # noqa

DEPLOY_ENV = 'qa'

try:
    from ..local import *  # noqa
except ImportError:
    pass
# vim:set et sts=4 ts=4 tw=80:
