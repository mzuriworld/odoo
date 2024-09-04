from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    dealer_id = fields.Many2one(
        'res.partner',
        string='Dealer',
        compute='_compute_dealer_id',
        store=True,
        readonly=False
    )

    @api.depends('create_uid')
    def _compute_dealer_id(self):
        for order in self:
            if order.create_uid and order.create_uid.company_id:
                order.dealer_id = order.create_uid.company_id.partner_id
            else:
                order.dealer_id = False
    def _get_report_base_filename(self):
        self.ensure_one()
        if self.is_dealer_order:
            return 'Dealer Quote %s' % (self.name)
        else:
            return 'Mzuri Quote %s' % (self.name)
