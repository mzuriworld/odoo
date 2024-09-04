/** @odoo-module */
import { registry } from "@web/core/registry";
import { many2OneField } from '@web/views/fields/many2one/many2one_field';
import { Component } from "@odoo/owl";
import {AbstractField} from "@web/views/fields/field";
import {fieldRegistry} from "@web/core/registry";
import { jsonrpc } from "@web/core/network/rpc_service";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
// odoo.define('mzuri_product_configurator.MyCustomWidget', function () {
//     // odoo.define('my_module.MyCustomWidget', ['web.field_registry', 'web.AbstractField'], function (require) {
//     'use strict';
//
//     // var fieldRegistry = require('web.field_registry');
//     // var AbstractField = require('web.AbstractField');
export class MyCustomWidget extends Component {
    static components = { Dialog };
    static props = {
        close: Function,
        title: String,
        orders: Array,
        onAddProduct: Function,
        onRemoveProduct: Function,
   };
    static template = 'mzuri_product_configurator.MyCustomWidgetTemplate';
        // events: {
        //     'change .attribute-select': '_onAttributeChange',
        // },

    setup() {
        this.title = this.props.title;
    }
    start() {
            this._super.apply(this, arguments);
            console.log("widget started");
            this._renderWidget();
    }
        _renderWidget() {
            var self = this;
            self.$el.html('<div class="attribute-select-wrapper"></div>');
            self._fetchAttributes().then(function (attributes) {
                self.attributes = attributes;
                self._populateAttributeSelect();
            });
        }

        _fetchAttributes() {
            return this._rpc({
                model: 'product.configurator.attribute.line',
                method: 'search_read',
                fields: ['attribute_id', 'value_ids'],
            });
        }

        _populateAttributeSelect() {
            var self = this;
            var $wrapper = self.$('.attribute-select-wrapper');
            _.each(this.attributes, function (attributeLine) {
                var $select = $('<select>', { class: 'form-control attribute-select', 'data-attribute-id': attributeLine.attribute_id[0] });
                _.each(attributeLine.value_ids, function (value) {
                    $select.append($('<option>', {
                        value: value.id,
                        text: value.display_name
                    }));
                });
                $wrapper.append($('<div>', { class: 'form-group' }).append($('<label>').text(attributeLine.attribute_id[1])).append($select));
            });
        }

        _onAttributeChange(ev) {
            var attributeId = $(ev.currentTarget).data('attribute-id');
            var valueId = $(ev.currentTarget).val();
            // Logika aktualizacji wartości atrybutu
            console.log('Wybrano atrybut o ID:', attributeId, 'z wartością ID:', valueId);
        }
    };

registry.category("fields").add('my_custom_widget', MyCustomWidget);




// odoo.define('mzuri_product_configurator.MyCustomWidget', function (require) {
//     'use strict';
//
//     var fieldRegistry = require('web.field_registry');
//     var AbstractField = require('web.AbstractField');
//
//     var MyCustomWidget = AbstractField.extend({
//         template: 'MyCustomWidgetTemplate',
//         events: {
//             'change .attribute-select': '_onAttributeChange',
//         },
//
//         start: function () {
//             this._super.apply(this, arguments);
//             this._renderWidget();
//         },
//
//         _renderWidget: function () {
//             var self = this;
//             self.$el.html('<div class="attribute-select-wrapper"></div>');
//             self._fetchAttributes().then(function (attributes) {
//                 self.attributes = attributes;
//                 self._populateAttributeSelect();
//             });
//         },
//
//         _fetchAttributes: function () {
//             return this._rpc({
//                 model: 'product.configurator.attribute.line',
//                 method: 'search_read',
//                 fields: ['attribute_id', 'value_ids'],
//             });
//         },
//
//         _populateAttributeSelect: function () {
//             var self = this;
//             var $wrapper = self.$('.attribute-select-wrapper');
//             _.each(this.attributes, function (attributeLine) {
//                 var $select = $('<select>', { class: 'form-control attribute-select', 'data-attribute-id': attributeLine.attribute_id[0] });
//                 _.each(attributeLine.value_ids, function (value) {
//                     $select.append($('<option>', {
//                         value: value.id,
//                         text: value.display_name
//                     }));
//                 });
//                 $wrapper.append($('<div>', { class: 'form-group' }).append($('<label>').text(attributeLine.attribute_id[1])).append($select));
//             });
//         },
//
//         _onAttributeChange: function (ev) {
//             var attributeId = $(ev.currentTarget).data('attribute-id');
//             var valueId = $(ev.currentTarget).val();
//             // Logika aktualizacji wartości atrybutu
//             console.log('Wybrano atrybut o ID:', attributeId, 'z wartością ID:', valueId);
//         },
//     });
//
//     fieldRegistry.add('my_custom_widget', MyCustomWidget);
//     return MyCustomWidget;
// });
