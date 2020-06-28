#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Binh Vu.
# Distributed under the terms of the Modified BSD License.

"""
A widget that allow javascript code to send some values to python code.
"""
from typing import Callable

from ipywidgets import DOMWidget
from traitlets import Unicode, Tuple, Int
from ._frontend import module_name, module_version


class SlowJSCallbackWidget(DOMWidget):
    """A widget that allow javascript code to send some values to python code.
    """
    _model_name = Unicode('SlowJSCallbackModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('SlowJSCallbackView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    value = Tuple(Int(0), Unicode(''), default_value=(0, '')).tag(sync=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.observe(self._on_receive, names='value')
        self.on_receive_handler = default_callback

    def on_receive(self, callback: Callable[[str], None]):
        """Register a handler
        """
        self.on_receive_handler = callback

    def _on_receive(self, event: dict):
        self.on_receive_handler(event['new'][1])


def default_callback(_val):
    pass
