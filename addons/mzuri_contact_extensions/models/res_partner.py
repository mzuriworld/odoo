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

from odoo import models, fields, api

class ResPartnerProductOwned(models.Model):
    _name = 'res.partner.product.owned'
    _description = 'Partner Product Owned'

    product_id = fields.Many2one('product.product', string="Product", required=True)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True, ondelete='cascade')
    serial_number = fields.Char(string="Serial Number", required=False)
    name = fields.Char(
        string='Name',
        compute='_compute_name',
        store=False,  # This is not necessary as it's the default, but included for clarity
    )
    
    @api.depends('product_id', 'serial_number')
    def _compute_name(self):
        for record in self:
            product_name = record.product_id.name or ''
            serial = record.serial_number or ''
            record.name = f"{product_name} ({serial})" if serial else product_name
    
    @api.model
    def name_get(self):
        result = []
        #for record in self:
        name = self.product_id.name
        if self.serial_number:
            name = f'{name} ({self.serial_number})'
        result.append((self.id, name))
        return result

    @api.onchange('serial_number')
    def _onchange_serial_number(self):
        """ Prevent editing serial number once it has been set. """
        if self.serial_number:
            self._origin.serial_number = self.serial_number

    @api.depends('serial_number')
    def _compute_serial_number_editable(self):
        """ Helper function to make the serial number editable only if empty. """
        for record in self:
            record.serial_number_editable = not bool(record.serial_number)

    serial_number_editable = fields.Boolean(compute="_compute_serial_number_editable")



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


    def action_copy_products_from_purchase_order(self):
        """Skopiuj produkty z zamówień zakupu powiązanych z zamówieniami sprzedaży dla tego klienta"""
        SaleOrder = self.env['sale.order']
        PurchaseOrder = self.env['purchase.order']

        # Znajdź wszystkie zamówienia sprzedaży dla tego klienta
        sale_orders = SaleOrder.search([('partner_id', '=', self.id), ('state', '=', 'sale')])

        # Znajdź zamówienia zakupu powiązane z zamówieniami sprzedaży
        purchase_orders = PurchaseOrder.search([ ('state', '=', 'done')])

        # Dodaj produkty z zamówień zakupu do "Posiadane/Park Maszynowy"
        for purchase_order in purchase_orders:
            for line in purchase_order.order_line:
                self.env['res.partner.product.owned'].create({
                    'partner_id': self.id,
                    'product_id': line.product_id.id,
                    'serial_number': purchase_order.vin_number,
                })

        return True

    def action_view_purchase_orders(self):
        """ Wyświetlenie widoku zamówień zakupu powiązanych z zamówieniami sprzedaży dla tego klienta """
        SaleOrder = self.env['sale.order']

        # Znajdź wszystkie zamówienia sprzedaży dla danego partnera
        sale_orders = SaleOrder.search([('state', '=', 'sale')])
        
        
        
        try:
            compose_form_id = self.env['ir.model.data']._xmlid_lookup('mzuri_contact_extensions.view_purchase_order_tree_with_add_to_park')[1]
        except ValueError:
            compose_form_id = False

        # Wyświetlenie zamówień zakupu powiązanych z zamówieniami sprzedaży
        return {
            'name': 'Wybierz Zamówienie Zakupu',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'views': [(compose_form_id, 'tree')],
            'res_id': self.id,
            'res_model': 'purchase.order',
            'domain': [('state', '=', 'done')],
            'context': {'default_partner_id': self.id},
            'target': 'new',
        }

    def action_add_to_park_from_purchase_order(self, purchase_order_ids):
        """Dodaj produkty z wybranych zamówień zakupu do parku maszynowego"""
        print("call of action")
        PurchaseOrder = self.env.context.get('active_ids', [])

        # Pobierz zamówienia zakupu na podstawie wybranych ID
        purchase_orders = PurchaseOrder.browse(purchase_order_ids)
        print(f"PO len: {len(purchase_orders)}")
        for purchase_order in purchase_orders:
            print(f"PO: {purchase_order.name}")
            for line in purchase_order.order_line:
                self.env['res.partner.product.owned'].create({
                    'partner_id': self.id,
                    'product_id': line.product_id.id,
                    'serial_number': purchase_order.vin_number,
                })

        #return True

