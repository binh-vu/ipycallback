#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Binh Vu.
# Distributed under the terms of the Modified BSD License.

import pytest

from ..slow_js_callback import ExampleWidget


def test_example_creation_blank():
    w = ExampleWidget()
    assert w.value == 'Hello World'
