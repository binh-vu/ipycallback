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


export
class SlowJSCallbackModel extends DOMWidgetModel {
  defaults() {
    return {...super.defaults(),
      _model_name: SlowJSCallbackModel.model_name,
      _model_module: SlowJSCallbackModel.model_module,
      _model_module_version: SlowJSCallbackModel.model_module_version,
      _view_name: SlowJSCallbackModel.view_name,
      _view_module: SlowJSCallbackModel.view_module,
      _view_module_version: SlowJSCallbackModel.view_module_version,
      value : [0, '']
    };
  }

  static serializers: ISerializers = {
      ...DOMWidgetModel.serializers,
      // Add any extra serializers here
    }

  static model_name = 'SlowJSCallbackModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'SlowJSCallbackView';   // Set to null if no view
  static view_module = MODULE_NAME;   // Set to null if no view
  static view_module_version = MODULE_VERSION;
}


export
class SlowJSCallbackView extends DOMWidgetView {
  render() {
    // do not display this in the dom
    this.el.classList.add('ipycallback');

    // register this view to the global variable.
    if ((window as any).IPyCallback === undefined) {
      (window as any).IPyCallback = new Map();
    }
    (window as any).IPyCallback.set(this.model.model_id, this);
  }

  send_msg(msg: string) {
    let value = this.model.get('value');
    this.model.set('value', [value[0] + 1, msg]);
    this.model.save_changes();
  }
}
