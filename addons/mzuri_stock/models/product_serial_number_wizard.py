from odoo import models, fields, api

class ProductSerialNumberWizard(models.TransientModel):
    _name = 'product.serial.number.wizard'
    _description = 'Product Serial Number Input Wizard'

    serial_number = fields.Char(string="Serial Number", required=True)
    purchase_order_id = fields.Many2one('purchase.order', string="Purchase Order")

    def assign_serial_number(self):
        """Assign the entered serial number to the products in the purchase order"""
        self.ensure_one()

        # Assuming we are assigning the serial number to the products in the order lines
        for line in self.purchase_order_id.order_line:
            product = line.product_id
            if not product.serial_number:
                product.write({'serial_number': self.serial_number})
            else:
                raise ValueError(f'Serial number already assigned to product {product.name}')
