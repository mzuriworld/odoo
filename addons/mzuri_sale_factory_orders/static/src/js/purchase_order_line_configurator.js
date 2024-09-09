odoo.define('mzuri_sale_factory_orders.purchase_product_configurator_dialog', [], function (Dialog, rpc, core) {
    "use strict";

//    var _t = core._t;

//    Dialog.include({
//        custom_callback: function () {
//            this._super.apply(this, arguments);
//            var self = this;
//            rpc.query({
//                model: 'purchase.order.line',
//                method: 'write',
//                args: [[this.options.default_line_id], {'product_config': this.state.product_config}],
//            }).then(function () {
//                self.do_notify(_t("Success"), _t("Product configuration saved successfully"));
//            });
//        },
//    });
});



//odoo.define('mzuri_sale_factory_orders.purchase_product_configurator_dialog', function (require) {
//    "use strict";
//
//    var Dialog = require('sale_product_configurator.dialog');
//    var rpc = require('web.rpc');
//
//    Dialog.include({
//        custom_callback: function () {
//            this._super.apply(this, arguments);
//            var self = this;
//            rpc.query({
//                model: 'purchase.order.line',
//                method: 'write',
//                args: [[this.options.default_line_id], {'product_config': this.state.product_config}],
//            }).then(function () {
//                self.do_notify(_t("Success"), _t("Product configuration saved successfully"));
//            });
//        },
//    });
//});
