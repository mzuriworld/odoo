from odoo import models, fields

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    configuration_code = fields.Char(string='Configuration Code')
