from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    serial_number = fields.Char(string="Serial Number", readonly=True)

    @api.model
    def assign_serial_number(self, product_id, serial_number):
        """Assigns a serial number to the product"""
        product = self.browse(product_id)
        if not product.serial_number:
            product.write({'serial_number': serial_number})
        else:
            raise ValueError('Serial number already assigned to this product.')
