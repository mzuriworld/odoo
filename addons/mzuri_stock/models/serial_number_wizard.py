# In mzuri_stock/models/serial_number_wizard.py
from odoo import models, fields, api

class SerialNumberWizard(models.TransientModel):
    _name = 'serial.number.wizard'
    _description = 'Serial Number Wizard'

    product_id = fields.Many2one('product.product', string="Product", required=True)
    serial_number = fields.Char(string="Serial Number", required=True)

    def assign_serial_number(self):
        picking_id = self.env.context.get('active_id')
        picking = self.env['stock.picking'].browse(picking_id)
        for line in picking.move_line_ids_without_package:
            if line.product_id == self.product_id:
                line.lot_id = self.env['stock.production.lot'].create({
                    'product_id': self.product_id.id,
                    'name': self.serial_number,
                })
        return {'type': 'ir.actions.act_window_close'}

# In mzuri_stock/models/stock_picking.py
from odoo import models, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_open_serial_number_wizard(self):
        """Opens the wizard to assign serial numbers"""
        return {
            'name': 'Assign Serial Numbers',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'serial.number.wizard',
            'target': 'new',
            'context': {'default_product_id': self.move_line_ids_without_package[0].product_id.id}
        }

