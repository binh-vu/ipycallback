
# ipycallback

[![Build Status](https://travis-ci.org/binh-vu/ipycallback.svg?branch=master)](https://travis-ci.org/binh-vu/ipycallback)
[![codecov](https://codecov.io/gh/binh-vu/ipycallback/branch/master/graph/badge.svg)](https://codecov.io/gh/binh-vu/ipycallback)


A widget that allows javascript (client) and python (server) communicate with each other.

## Installation

You can install using `pip`:

```bash
pip install ipycallback
```

Or if you use jupyterlab:

```bash
pip install ipycallback
jupyter labextension install @jupyter-widgets/jupyterlab-manager ipycallback
```

If you are using Jupyter Notebook 5.2 or earlier, you may also need to enable
the nbextension:
```bash
jupyter nbextension enable --py [--sys-prefix|--user|--system] ipycallback
```

## Examples

1. Create a widget (server)

```python
from ipycallback import SlowTunnelWidget

tunnel = SlowTunnelWidget()
display(tunnel)
```

2. Send messages from python to javascript (server)

```python
tunnel.send_msg(ujson.dumps({"msg": "hello world"}))
```

3. Listen to messages from javascript (server). This will override any previous listeners.

```python
def handle_msg(version: int, msg: str):
    print('receive message', version, msg)

tunnel.on_receive(handle_msg)
```

5. Listen to messages from python (client). This will override any previous listeners.

```javascript
window.IPyCallback.get("<tunnel.tunnel_id>").on_receive((version, msg) => {
    console.log('receive message', version, msg);
});
```

6. Send messages from javascript to python (client).

```javascript
let version = window.IPyCallback.get("<tunnel.tunnel_id>").send_msg(JSON.stringify({"msg": "hello world"}));
```

7. Implement a "synchronous" call-and-wait

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

See [examples](./examples) for more.

## How does this work

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

## Development

Release the package ([original](https://github.com/jupyter-widgets/widget-ts-cookiecutter)):

1. Update the version in `package.json`, `ipycallback/_frontend.py` and `ipycallback/_version.py`.
2. Relase the npm packages:
   ```bash
   npm login
   npm publish
   ```
3. Bundle the python package: `python setup.py sdist bdist_wheel`
4. Publish the package to PyPI: `twine upload -u <username> -p <password> dist/ipycallback*`
