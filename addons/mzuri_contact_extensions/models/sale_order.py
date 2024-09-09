from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_add_products_to_park(self):
        # Dodajemy produkty z zamówienia sprzedaży do parku maszynowego partnera
        for order in self:
            partner = order.partner_id
            for line in order.order_line:
                # Sprawdź, czy produkt już nie jest w posiadaniu, aby uniknąć duplikatów
                existing_product = self.env['res.partner.product.owned'].search([
                    ('partner_id', '=', partner.id),
                    ('product_id', '=', line.product_id.id)
                ])
                if not existing_product:
                    self.env['res.partner.product.owned'].create({
                        'partner_id': partner.id,
                        'product_id': line.product_id.id,
                        'serial_number': line.product_id.serial_number,  # Jeśli numer seryjny istnieje
                    })
        # Po dodaniu produktów, zamknij okno i wróć do widoku partnera
        return {
                'type': 'ir.actions.act_window',
                'res_model': 'res.partner',
                'view_mode': 'form',
                'res_id': order.partner_id.id,
                'target': 'main',
                'views': [(self.env.ref('base.view_partner_form').id, 'form')],
                'context': {
                    'default_partner_id': order.partner_id.id,
                    'active_tab': 'posiadane',
                },
        }
        # def action_add_products_to_park(self):
        #     # Tworzenie rekordów dla każdego wybranego produktu
        #     for sale_order in self:
        #         for line in sale_order.order_line:
        #             self.env['res.partner.product.owned'].create({
        #                 'partner_id': sale_order.partner_id.id,
        #                 'product_id': line.product_id.id,
        #             })


