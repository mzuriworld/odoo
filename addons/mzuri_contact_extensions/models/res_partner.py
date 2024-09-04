# from odoo import models, fields
#
# class ResPartner(models.Model):
#     _inherit = 'res.partner'
#
#     product_interest_ids = fields.Many2many(
#         'product.product',
#         'res_partner_product_interest_rel',
#         'partner_id',
#         'product_id',
#         string="Zainteresowania"
#     )
#     product_owned_ids = fields.Many2many(
#         'product.product',
#         'res_partner_product_owned_rel',
#         'partner_id',
#         'product_id',
#         string="Posiadane/Park Maszynowy"
#     )

from odoo import models, fields

class ResPartnerProductInterest(models.Model):
    _name = 'res.partner.product.interest'
    _description = 'Partner Product Interest'

    partner_id = fields.Many2one('res.partner', string="Partner", required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Product", required=True)

class ResPartnerProductOwned(models.Model):
    _name = 'res.partner.product.owned'
    _description = 'Partner Product Owned'

    partner_id = fields.Many2one('res.partner', string="Partner", required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Product", required=True)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    product_interest_ids = fields.One2many(
        'res.partner.product.interest',
        'partner_id',
        string="Zainteresowania"
    )
    product_owned_ids = fields.One2many(
        'res.partner.product.owned',
        'partner_id',
        string="Posiadane/Park Maszynowy"
    )
