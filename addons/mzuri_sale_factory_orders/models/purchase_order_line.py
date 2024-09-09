from odoo import models, fields, api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    # Add fields to support product configuration
    product_config = fields.Char(string="Product Configuration", readonly=True)
    # is_configurable = fields.Boolean(related='product_id.product_tmpl_id.has_configurator', readonly=True)

    def action_open_product_configurator(self):
        self.ensure_one()

        print("Triger funkcji javascript")
        # Trigger JavaScript function to open configurator dialog
        return {
            'type': 'ir.actions.client',
            'tag': 'purchase_order_line_configurator',
            'params': {
                'productId': self.product_id.id,
                'orderLineId': self.id,
                'defaultQty': self.product_qty,
                'defaultPartnerId': self.order_id.partner_id.id,
            }
        }

    # def action_open_product_configurator(self):
    #     """Open the product configurator wizard similar to Sale Order."""
    #     self.ensure_one()
    #     # Use the product configurator wizard to configure the product
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Product Configurator',
    #         'view_mode': 'form',
    #         'res_model': 'sale.product.configurator',
    #         'view_id': self.env.ref('sale_product_configurator.view_product_configurator_form').id,
    #         'context': {
    #             'default_order_line_id': self.id,
    #             'default_product_id': self.product_id.id,
    #             'default_qty': self.product_qty,
    #             'default_partner_id': self.order_id.partner_id.id,
    #         },
    #         'target': 'new',
    #     }

    def write(self, vals):
        res = super(PurchaseOrderLine, self).write(vals)
        if vals.get('product_config'):
            # Handle configuration changes here, e.g. update product description or other fields
            self.product_id.write({'config_details': vals['product_config']})
        return res

