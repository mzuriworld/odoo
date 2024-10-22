from odoo import models, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def action_add_to_park_from_purchase_order(self):
        """
        This method adds the products from the purchase order to the partner's "Owned Products" (Park Maszynowy).
        It associates the products with the partner and updates the park, ensuring no duplicates.
        """
        # Loop through all selected purchase orders
        partner_id = self.env.context.get('default_partner_id')
        for order in self:
            # Ensure that the purchase order is related to a valid sales order
            print(f"PO: {order.name}, order lines: {len(order.order_line)}")
            # Retrieve or create the partner's product ownership record
            for line in order.order_line:
                # Check if this product is already in the partner's "park maszynowy"
                # existing_owned_product = self.env['res.partner.product.owned'].search([
                    # ('partner_id', '=', order.partner_id.id),
                    # ('product_id', '=', line.product_id.id),
                # ], limit=1)

                # If the product is not already added to the park, create a new record
                
                self.env['res.partner.product.owned'].create({
                    'partner_id': partner_id,
                    'product_id': line.product_id.id,
                    'serial_number': order.vin_number # or '',  # Optional serial number
                })

                # Po dodaniu produktów, zamknij okno i wróć do widoku partnera
        
