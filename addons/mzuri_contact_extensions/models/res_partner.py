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

from odoo import models, fields, api
from odoo.exceptions import ValidationError
class ResPartnerProductInterest(models.Model):
    _name = 'res.partner.product.interest'
    _description = 'Partner Product Interest'

    partner_id = fields.Many2one('res.partner', string="Partner", required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Product", required=True)

class ResPartnerProductOwned(models.Model):
    _name = 'res.partner.product.owned'
    _description = 'Partner Product Owned'

    product_id = fields.Many2one('product.product', string="Product", required=True)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True, ondelete='cascade')
    serial_number = fields.Char(related='product_id.serial_number', string="Serial Number", readonly=False)

    @api.onchange('serial_number')
    def _onchange_serial_number(self):
        """ Zablokuj edycję serial number po pierwszym wpisaniu """
        if self.serial_number:
            self.product_id.serial_number = self.serial_number
            self.serial_number = self.product_id.serial_number

    @api.model
    def create(self, vals):
        # Jeśli serial_number jest ustawiony, zapisujemy go w produkcie
        if 'serial_number' in vals and vals['serial_number']:
            product = self.env['product.product'].browse(vals['product_id'])
            product.serial_number = vals['serial_number']
        return super(ResPartnerProductOwned, self).create(vals)

    @api.constrains('serial_number')
    def _check_serial_number_once(self):
        """ Blokuje możliwość edytowania serial number po jego pierwszym wpisaniu """
        if self.serial_number and self.product_id.serial_number:
            raise ValidationError("Numer seryjny nie może być edytowany po zapisaniu.")

    def write(self, vals):
        # Jeśli serial_number już istnieje, blokujemy jego edycję
        if 'serial_number' in vals and self.serial_number:
            raise ValidationError("Numer seryjny nie może być edytowany po zapisaniu.")
        return super(ResPartnerProductOwned, self).write(vals)


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

    # Przycisk w widoku wywołuje tę metodę
    def action_copy_products_from_sale_order(self):
        # Wyświetlenie widoku zamówień sprzedaży powiązanych z kontaktem
        return {
            'name': 'Wybierz Zamówienie Sprzedaży',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'domain': [('partner_id', '=', self.id), ('state', '=', 'sale')],
            # Filtrujemy zamówienia powiązane z kontaktem
            'context': {'default_partner_id': self.id},
            'target': 'new',
        }

    def action_view_sale_order(self):
        action = self.env['ir.actions.act_window']._for_xml_id('sale.act_res_partner_2_sale_order')
        all_child = self.with_context(active_test=False).search([('id', 'child_of', self.ids)])
        action["domain"] = [("partner_id", "in", all_child.ids)]
        return action

    def action_add_products_to_park(self):
        """Dodaj produkty z zamówienia sprzedaży do Parku Maszynowego"""
        sale_orders = self.env['sale.order'].browse(self.env.context.get('active_ids', []))
        for sale_order in sale_orders:
            for line in sale_order.order_line:
                self.env['res.partner.product.owned'].create({
                    'partner_id': sale_order.partner_id.id,
                    'product_id': line.product_id.id,
                })
