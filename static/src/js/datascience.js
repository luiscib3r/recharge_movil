odoo.define('recharge_movil', function (require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var config = require('web.config');
var core = require('web.core');
var framework = require('web.framework');
var session = require('web.session');
var Widget = require('web.Widget');

var QWeb = core.qweb;
var _t = core._t;

var Databoard = AbstractAction.extend({
    template: 'DataMain',

    start: function() {
      return this.load()
    },

    load: function () {
      var self = this;
      this._rpc({route: '/recharge_movil/data'})
      .then(function (data) {
        return self.load_widget(data)
      })
    },

    load_widget: function(data){
        return  new DataScience(this, data).replace(this.$('.o_recharge_movil_datascience'));
    },
});

var DataScience = Widget.extend({
  template: 'DataScience',

  init: function(parent, data) {
    this.data = data;
    this.parent = parent;
  }
})

core.action_registry.add('recharge_movil.datascience', Databoard);

return {
    Databoard: Databoard,
    DataScience: DataScience
};

});
