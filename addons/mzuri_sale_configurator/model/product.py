# from odoo import models, fields, api
#
# class SaleOrderLine(models.Model):
#     _inherit = 'sale.order.line'
#
#     configurator_attributes = fields.One2many('product.sale.configurator.step', 'order_line_id', string="Configurator Attributes")
#
# class ProductConfiguratorStep(models.Model):
#     _name = 'product.sale.configurator.step'
#     _description = 'Product Configurator Step'
#
#     order_line_id = fields.Many2one('sale.order.line', string="Sale Order Line", required=True)
#     attribute_id = fields.Many2one('product.attribute', string="Attribute", required=True)
#     value_id = fields.Many2one('product.attribute.value', string="Value", required=True)

################################################################
# from odoo import models, fields, api

# class SaleOrderLine(models.Model):
#     _inherit = 'sale.order.line'
#
#     configurator_attributes = fields.One2many('product.sale.configurator.step', 'order_line_id', string="Configurator Attributes")
#     show_configurator = fields.Boolean(string="Show Configurator", compute="_compute_show_configurator")
#
#     @api.depends('product_id')
#     def _compute_show_configurator(self):
#
#         for line in self:
#             # Dodaj logikę do wyświetlania konfiguratora dla określonych produktów
#             if line.product_id.type == 'configurable':
#                 line.show_configurator = True
#             else:
#                 line.show_configurator = False
#
# class ProductConfiguratorStep(models.Model):
#     _name = 'product.sale.configurator.step'
#     _description = 'Product Configurator Step'
#
#     order_line_id = fields.Many2one('sale.order.line', string="Sale Order Line", required=True)
#     attribute_id = fields.Many2one('product.attribute', string="Attribute", required=True)
#     value_id = fields.Many2one('product.attribute.value', string="Value", required=True)

#########################################################################################
import logging
from odoo import models, fields, api

# Konfiguracja loggera
_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    configurator_attributes = fields.One2many('product.sale.configurator.step', 'order_line_id', string="Configurator Attributes")
    show_configurator = fields.Boolean(string="Show Configurator", compute="_compute_show_configurator")

    @api.depends('product_id')
    def _compute_show_configurator(self):
        for line in self:
            # Dodaj logikę do wyświetlania konfiguratora dla określonych produktów
            if line.product_id.type == 'configurable':
                line.show_configurator = True
                _logger.info("Product %s is configurable. Show configurator: %s", line.product_id.name, line.show_configurator)
            else:
                line.show_configurator = False
                _logger.info("Product %s is not configurable. Show configurator: %s", line.product_id.name, line.show_configurator)

class ProductConfiguratorStep(models.Model):
    _name = 'product.sale.configurator.step'
    _description = 'Product Configurator Step'

    order_line_id = fields.Many2one('sale.order.line', string="Sale Order Line", required=True)
    attribute_id = fields.Many2one('product.attribute', string="Attribute", required=True)
    value_id = fields.Many2one('product.attribute.value', string="Value", required=True)
