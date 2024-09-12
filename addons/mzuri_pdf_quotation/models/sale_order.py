from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # # Example of adding custom fields (optional)
    # offer_number = fields.Char(string='Offer Number')
