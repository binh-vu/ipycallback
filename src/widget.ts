// Copyright (c) Binh Vu
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel, DOMWidgetView, ISerializers
} from '@jupyter-widgets/base';

import {
  MODULE_NAME, MODULE_VERSION
} from './version';

// Import the CSS
import '../css/widget.css'


export class SlowTunnelModel extends DOMWidgetModel {
  defaults() {
    return {...super.defaults(),
      _model_name: SlowTunnelModel.model_name,
      _model_module: SlowTunnelModel.model_module,
      _model_module_version: SlowTunnelModel.model_module_version,
      _view_name: SlowTunnelModel.view_name,
      _view_module: SlowTunnelModel.view_module,
      _view_module_version: SlowTunnelModel.view_module_version,
      py_endpoint: [0, ''],
      js_endpoint: [0, '']
    };
  }

  static serializers: ISerializers = {
      ...DOMWidgetModel.serializers,
      // Add any extra serializers here
    }

  static model_name = 'SlowTunnelModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'SlowTunnelView';   // Set to null if no view
  static view_module = MODULE_NAME;   // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class SlowTunnelView extends DOMWidgetView {
  public onReceiveHandler: (version: number, msg: string) => void = defaultCallbackHandler;

  render() {
    // do not display this in the dom
    this.el.classList.add('ipycallback');

    // listen to the change from the server for this variable
    this.model.on('change:js_endpoint', this.receive_msg, this);
    // register this view to the global variable.
    if ((window as any).IPyCallback === undefined) {
      (window as any).IPyCallback = new Map();
    }
    (window as any).IPyCallback.set(this.model.model_id, this);
  }

  send_msg(msg: string) {
    let py_endpoint = this.model.get('py_endpoint');
    let version = py_endpoint[0] + 1;
    this.model.set('py_endpoint', [version, msg]);
    this.model.save_changes();

    return version;
  }

  receive_msg() {
    var value = this.model.get('js_endpoint');
    this.onReceiveHandler(value[0], value[1]);
  }

  on_receive(callback: (version: number, msg: string) => void) {
    this.onReceiveHandler = callback;
  }
}

function defaultCallbackHandler(version: number, msg: string) {
}