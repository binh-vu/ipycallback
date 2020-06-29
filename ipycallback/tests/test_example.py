#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Binh Vu.
# Distributed under the terms of the Modified BSD License.

import pytest

from ..slow_tunnel import SlowTunnelWidget


def test_example_creation_blank():
    w = SlowTunnelWidget()
