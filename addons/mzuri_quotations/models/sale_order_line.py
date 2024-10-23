from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    name_in_offer = fields.Char(string='Name in Offer')

    @api.onchange('product_id')
    def _onchange_product_id_set_name_in_offer(self):
        if self.product_id:
            self.name_in_offer = self.product_id.name

