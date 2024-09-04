from odoo import models, fields

class ProductConfigurator(models.Model):
    _name = 'product.configurator'
    _description = 'Product Configurator'

    name = fields.Char(string='Configuration Name', required=True)
    product_tmpl_id = fields.Many2one('product.template', string='Product Template', required=True)
    attribute_line_ids = fields.One2many('product.configurator.attribute.line', 'configurator_id', string='Attribute Lines')

class ProductConfiguratorAttributeLine(models.Model):
    _name = 'product.configurator.attribute.line'
    _description = 'Product Configurator Attribute Line'

    configurator_id = fields.Many2one('product.configurator', string='Product Configurator', required=True)
    attribute_id = fields.Many2one('product.attribute', string='Attribute', required=True)
    value_ids = fields.Many2many('product.attribute.value', string='Possible Values')



# from odoo import models, fields, api
#
# class ProductConfigurator(models.Model):
#     _name = 'product.configurator'
#     _description = 'Product Configurator'
#
#     name = fields.Char(string="Configuration Name", required=True)
#     product_tmpl_id = fields.Many2one('product.template', string="Product Template", required=True)
#     attribute_line_ids = fields.One2many('product.configurator.line', 'configurator_id', string="Attribute Lines")
#     configuration_code = fields.Char(string="Configuration Code", compute="_compute_configuration_code")
#
#     @api.depends('product_tmpl_id', 'attribute_line_ids')
#     def _compute_configuration_code(self):
#         for record in self:
#             code = record.product_tmpl_id.default_code or ''
#             for line in record.attribute_line_ids:
#                 code += f'-{line.attribute_id.name}-{line.value_id.name}'
#             record.configuration_code = code
#
# class ProductConfiguratorLine(models.Model):
#     _name = 'product.configurator.line'
#     _description = 'Product Configurator Line'
#
#     configurator_id = fields.Many2one('product.configurator', string="Configurator", required=True)
#     product_tmpl_id = fields.Many2one('product.template', string="Product Template", required=True)  # Dodane pole
#     attribute_id = fields.Many2one('product.attribute', string="Attribute", required=True)
#     value_id = fields.Many2one('product.attribute.value', string="Value", required=True)
