from odoo import models, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def action_start_shipment(self):
        """Open the wizard for serial number input when starting shipment"""
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'product.serial.number.wizard',
            'view_mode': 'form',
            'target': 'new',  # Open in a popup window
            'context': {
                'default_purchase_order_id': self.id
            }
        }
