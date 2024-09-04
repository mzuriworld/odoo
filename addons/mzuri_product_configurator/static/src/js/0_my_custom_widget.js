odoo.define('mzuri_product_configurator.MyCustomWidget', function (require) {
    'use strict';

    var fieldRegistry = require('web.field_registry');
    var relationalFields = require('web.relational_fields');
    var core = require('web.core');
    var _t = core._t;

    var MyCustomWidget = relationalFields.FieldMany2One.extend({
        events: _.extend({}, relationalFields.FieldMany2One.prototype.events, {
            'change select': '_onAttributeChange',
        }),

        init: function () {
            this._super.apply(this, arguments);
            this.attributes = []; // tutaj przechowujemy atrybuty produktu
        },

        _renderEdit: function () {
            var self = this;
            this._super.apply(this, arguments);
            this.$el.append('<select class="form-control"/>');
            this._fetchProductAttributes().then(function (attributes) {
                self.attributes = attributes;
                self._populateAttributeSelect();
            });
        },

        _fetchProductAttributes: function () {
            return this._rpc({
                model: 'product.attribute',
                method: 'search_read',
                fields: ['name'],
            });
        },

        _populateAttributeSelect: function () {
            var $select = this.$('select');
            $select.empty();
            _.each(this.attributes, function (attribute) {
                $select.append($('<option>', {
                    value: attribute.id,
                    text: attribute.name
                }));
            });
        },

        _onAttributeChange: function (ev) {
            var attributeId = $(ev.currentTarget).val();
            // Implementacja logiki zmiany atrybutu
            console.log('Wybrano atrybut o ID:', attributeId);
        },
    });

    fieldRegistry.add('my_custom_widget', MyCustomWidget);
});
