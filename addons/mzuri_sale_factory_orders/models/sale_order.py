from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    purchase_order_ids = fields.One2many('purchase.order', 'sale_order_id', string="Powiązane Zamówienia Zakupu")
