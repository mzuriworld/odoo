from odoo import models, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def action_add_to_park_from_purchase_order(self):
        """
        This method adds the products from the purchase order to the partner's "Owned Products" (Park Maszynowy).
        It associates the products with the partner and updates the park, ensuring no duplicates.
        """
        # Loop through all selected purchase orders
        for order in self:
            # Ensure that the purchase order is related to a valid sales order
            if order.origin and order.partner_id:
                # Retrieve or create the partner's product ownership record
                for line in order.order_line:
                    # Check if this product is already in the partner's "park maszynowy"
                    existing_owned_product = self.env['res.partner.product.owned'].search([
                        ('partner_id', '=', order.partner_id.id),
                        ('product_id', '=', line.product_id.id),
                    ], limit=1)

                    # If the product is not already added to the park, create a new record
                    if not existing_owned_product:
                        self.env['res.partner.product.owned'].create({
                            'partner_id': order.partner_id.id,
                            'product_id': line.product_id.id,
                            # 'serial_number': line.product_id.serial_number or '',  # Optional serial number
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
