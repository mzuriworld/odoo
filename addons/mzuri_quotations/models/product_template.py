
from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    offer_template_ids = fields.One2many(
        'offer.template',
        'id',
        string='Offer Templates',
        help='Upload different Word templates for each language.'
    )
class ProductTemplateAttributeValue(models.Model):
    _inherit = 'product.template.attribute.value'

    quotation_description = fields.Char(string='Quotation Description', translate=True)

class OfferTemplate(models.Model):
    _name = 'offer.template'
    _description = 'Offer Template'

    name = fields.Char(string="Template Name", required=True)
    language_id = fields.Many2one('res.lang', string="Language", required=True)
    template_attachment_id = fields.Many2one('ir.attachment', string="Word Template", required=True)
