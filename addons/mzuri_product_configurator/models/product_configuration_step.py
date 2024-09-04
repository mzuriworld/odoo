from odoo import models, fields, api

class ProductConfiguratorStep(models.Model):
    _name = 'product.configurator.step'
    _description = 'Product Configurator Step'

    name = fields.Char(string="Name", required=True)
    product_id = fields.Many2one('product.product', string="Product", required=True)
    attribute_id = fields.Many2one('product.attribute', string="Attribute", required=True)
    value_id = fields.Many2one('product.attribute.value', string="Value", required=True)
    image = fields.Binary(string="Image")
