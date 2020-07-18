#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Binh Vu.
# Distributed under the terms of the Modified BSD License.

"""
A widget that allow javascript code to send some values to python code.
"""
from typing import Callable
from uuid import uuid4

from ipywidgets import DOMWidget
from traitlets import Unicode, Tuple, Int
from ._frontend import module_name, module_version


class SlowTunnelWidget(DOMWidget):
    """A widget that allows javascript (client) and python (server) communicate with each other.

    Low-level ipywidgets documentation: https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20Low%20Level.html

    It contains two endpoints (or queue):
    1. `py_endpoint` for the client to "send" messages to the server. Specifically, when the value is changed in the client,
        Jupyter notebook `comms` fires a message to the python kernel. The python code that listens to the change event
        of this endpoint will pick it up and the `on_receive_handler` function will be called with two parameters:
        the version of this message, and the message.
    2. `js_endpoint` for the server to "send" messages to the client. The mechanic is similar to the `py_endpoint`.

    Note that each message is associated with a "version". Normally, you won't need to handle message's version
    if your applications don't need to have a synchronous "call-and-receive" mechanism. An example of an application
    that need synchronous "call-and-receive" is fulltext search where users type some keyword, the request is send
    to the server, while the response is generated, users may modify their query, which create another request to the
    server. Even though you may try to cancel the previous request, you still may end up receiving two responses
    in which the later response is from the *former* request. A solution to this problem is to associate each request
    with a value (version) that represent the order of the requests. On the server side, a message with older version
    will be discard and won't be send to the client, while on the client side, when they receive a message, they can
    discard the message if they have made a newer message. In this scenario, we should have the message's version in
    `py_endpoint` will always be equal to the message's version in the `js_endpoint` or be the `js_endpoint` message's
    version plus 1 (when there is a request that server is handling). Below is a snippet showing how this works:

    ```javascript
    // (client)
    // send a message to the server, this function returns a version of this message, which is just the previous
    // version + 1
    let version = tunnel.send_msg("message");
    tunnel.on_receive((resp_version, response) => {
        // ignore the response if it is old
        if (resp_version < version) return;

        // put your code to handle the response in here
    });
    ```

    ```python
    # (server)
    def on_receive(version: int, msg: str):
        # handle the message
        resp_msg = msg

        # generate a response with a specific version to ensure the order
        tunnel.send_msg_with_version(version, resp_msg)
    ```

    In case your applications only need to sync the state of the client and server models (may be because you
    don't want to write an extension for that), then you can use just one endpoint: `js_endpoint` if you want to
    push the server's state to the client (use the `send_msg` function in python), or `py_endpoint` if you want to
    push the client's state to the server (use the `send_msg` function in javascript).
    """
    _model_name = Unicode('SlowTunnelModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('SlowTunnelView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    py_endpoint = Tuple(Int(0), Unicode(''), default_value=(0, '')).tag(sync=True)
    js_endpoint = Tuple(Int(0), Unicode(''), default_value=(0, '')).tag(sync=True)
    tunnel_id = Unicode().tag(sync=True)

    def __init__(self, **kwargs):
        if 'tunnel_id' not in kwargs:
            kwargs['tunnel_id'] = str(uuid4())

        super().__init__(**kwargs)

        self.observe(self._on_receive, names='py_endpoint')
        self.on_receive_handler = default_callback

    def send_msg(self, msg: str):
        """Send a message to the channel"""
        self.js_endpoint = (self.js_endpoint[0] + 1, msg)

    def on_receive(self, callback: Callable[[int, str], None]):
        """Register a handler
        """
        self.on_receive_handler = callback

    def send_msg_with_version(self, version: int, msg: str):
        """Push a message back to the channel. Only push newer version"""
        if version > self.js_endpoint[0]:
            self.js_endpoint = (version, msg)

    def _on_receive(self, event: dict):
        self.on_receive_handler(event['new'][0], event['new'][1])


def default_callback(_version, _msg):
    pass
