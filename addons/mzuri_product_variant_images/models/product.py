from odoo import models, fields

from odoo import models, fields

class ProductTemplateAttributeValue(models.Model):
    _inherit = 'product.template.attribute.value'

    image = fields.Binary(string="Image")


#
#
# class ProductAttributeImage(models.Model):
#     _name = 'product.template.attribute.image'
#     _description = 'Product Attribute Image'
#
#     product_tmpl_id = fields.Many2one('product.template.attribute.image.attribute_id', string="Product Template", required=True)
#     # attribute_id = fields.Many2one('product.attribute', string="Attribute", required=True)
#     # value_id = fields.Many2one('product.attribute.value', string="Value", required=True)
#     image = fields.Binary(string="Image")
#
#
# class ProductTemplateWithImage(models.Model):
#     _inherit = 'product.template.attribute.value'
#
#     # attribute_image = fields.Binary(string="Attribute Image")
#     attribute_image_ids = fields.One2many('product.template.attribute.value.image', 'product_tmpl_id', string="Attribute Value Images")
#
# # class ProductProduct(models.Model):
# #     _inherit = 'product.product'
# #
# #     variant_image = fields.Binary(string="Variant Image")
#
#
