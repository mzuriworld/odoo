
odoo.define('@mzuri_sale_factory_orders/purchase_order_line_configurator',[], function (require) {
    "use strict";
//    var Dialog = require('@sale_product_configurator/js/product_configurator_dialog/product_configurator_dialog');
        var Dialog = require('sale_product_configurator.dialog');

    // Function to open the product configurator dialog
    function openConfigurator(options) {
        var dialog = new Dialog(this, {
            productId: options.productId,
            orderLineId: options.orderLineId,
            defaultQty: options.defaultQty,
            defaultPartnerId: options.defaultPartnerId,
        });
        dialog.open();
    }

    // Listen for button clicks
    $(document).on('click', '.configure_product_button', function () {
        var $button = $(this);
        var productId = $button.data('product-id');
        var orderLineId = $button.data('order-line-id');
        var qty = $button.data('qty');
        var partnerId = $button.data('partner-id');

        // Call the configurator
        openConfigurator({
            productId: productId,
            orderLineId: orderLineId,
            defaultQty: qty,
            defaultPartnerId: partnerId,
        });
    });

    return {
        openConfigurator: openConfigurator,
    };
});



//    var Dialog = require('@sale_product_configurator/js/product_configurator_dialog/product_configurator_dialog');
////    var rpc = require('web.rpc');
////    var core = require('web.core');
////    var _t = core._t;
//
//    // Function to open the configurator dialog
//    function openConfiguratorJS(ev) {
//        var options = ev.target.dataset.args ? JSON.parse(ev.target.dataset.args) : {};
//        var dialog = new Dialog(this, {
//            productId: options.productId,
//            orderLineId: options.orderLineId,
//            defaultQty: options.defaultQty,
//            defaultPartnerId: options.defaultPartnerId,
//        });
//
//        // Open the dialog and handle the result
//        dialog.open().then(function (result) {
//            if (result) {
//                rpc.query({
//                    model: 'purchase.order.line', // Save the configuration back to the purchase order line
//                    method: 'write',
//                    args: [[options.orderLineId], {
//                        'product_config': result,
//                    }],
//                }).then(function () {
//                    dialog.do_notify(_t("Success"), _t("Product configuration saved successfully"));
//                }).catch(function (err) {
//                    console.log("Error saving product configuration: ", err);
//                });
//            }
//        });
//    }
//
//    // Return the method for external access
//    return {
//        openConfiguratorJS: openConfiguratorJS,
//    };
//});


//odoo.define('@mzuri_sale_factory_orders/purchase_order_line_configurator', [], function (require) {
//    "use strict";
//
//    var Dialog = require('@sale_product_configurator/js/product_configurator_dialog/product_configurator_dialog');
////    var rpc = require('web.rpc');
////    var core = require('web.core');
////    var _t = core._t;
//
//    // Function to open the configurator dialog
//    function openConfigurator(options) {
//        var dialog = new Dialog(this, {
//            productId: options.productId,
//            orderLineId: options.orderLineId,
//            defaultQty: options.defaultQty,
//            defaultPartnerId: options.defaultPartnerId,
//        });
//
//        // Open the dialog and handle the result
//        dialog.open().then(function (result) {
//            if (result) {
//                rpc.query({
//                    model: 'purchase.order.line', // Save the configuration back to the purchase order line
//                    method: 'write',
//                    args: [[options.orderLineId], {
//                        'product_config': result,
//                    }],
//                }).then(function () {
//                    dialog.do_notify(_t("Success"), _t("Product configuration saved successfully"));
//                }).catch(function (err) {
//                    console.log("Error saving product configuration: ", err);
//                });
//            }
//        });
//    }
//
//    // Return the method for external access
//    return {
//        openConfigurator: openConfigurator,
//    };
//});


//odoo.define('purchase_order_line_configurator', ['@sale_product_configurator/js/product_configurator_dialog/product_configurator_dialog'], function (require) {
//    "use strict";
//
//    // Now the dependencies (rpc and Dialog) are loaded, and you can use them
//
//    var Dialog = require('sale_product_configurator/js/product_configurator_dialog/product_configurator_dialog');
//
//    function openConfigurator(options) {
//        var dialog = new Dialog(this, {
//            productId: options.productId,
//            orderLineId: options.orderLineId,
//            defaultQty: options.defaultQty,
//            defaultPartnerId: options.defaultPartnerId,
//        });
//        dialog.open();
//    }
//
//    return {
//        openConfigurator: openConfigurator,
//    };
//});
