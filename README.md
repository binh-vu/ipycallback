
# ipycallback

[![Build Status](https://travis-ci.org/binh-vu/ipycallback.svg?branch=master)](https://travis-ci.org/binh-vu/ipycallback)
[![codecov](https://codecov.io/gh/binh-vu/ipycallback/branch/master/graph/badge.svg)](https://codecov.io/gh/binh-vu/ipycallback)


Use this widget to allow client side (javascript) to trigger event on the server side (python)

## Installation

You can install using `pip`:

```bash
pip install ipycallback
```

Or if you use jupyterlab:

```bash
pip install ipycallback
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

If you are using Jupyter Notebook 5.2 or earlier, you may also need to enable
the nbextension:
```bash
jupyter nbextension enable --py [--sys-prefix|--user|--system] ipycallback
```
