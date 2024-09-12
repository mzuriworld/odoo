from odoo import models, fields, api

class ResPartnerProductOwned(models.Model):
    _inherit = 'res.partner.product.owned'
    @api.model
    def name_get(self):
        result = []
        for record in self:
            name = f"{record.product_id.name} ({record.serial_number})" if record.serial_number else record.product_id.name
            result.append((record.id, name))
        return result
