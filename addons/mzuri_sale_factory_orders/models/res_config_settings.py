# from odoo import models, fields, api
#
# class ResConfigSettings(models.TransientModel):
#     _inherit = 'res.config.settings'
#
#     default_supplier_id = fields.Many2one(
#         'res.partner',
#         string='Default Supplier',
#         domain="[('supplier_rank', '>', 0)]",
#         config_parameter='purchase.default_supplier_id',
#         default_model='purchase.order'
#     )
#
#     @api.model
#     def set_values(self):
#         super(ResConfigSettings, self).set_values()
#         self.env['ir.config_parameter'].sudo().set_param('purchase.default_supplier_id', self.default_supplier_id.id or False)
#
#     @api.model
#     def get_values(self):
#         res = super(ResConfigSettings, self).get_values()
#         supplier_id = self.env['ir.config_parameter'].sudo().get_param('purchase.default_supplier_id', default=False)
#         res.update(
#             default_supplier_id=int(supplier_id) if supplier_id else False
#         )
#         return res


# from odoo import models, fields, api
#
# class ResConfigSettings(models.TransientModel):
#     _inherit = 'res.config.settings'
#
#     default_supplier_id = fields.Many2one('res.partner', string="Default Supplier", domain="[('supplier_rank', '>', 0)]")
#
#     @api.model
#     def get_values(self):
#         res = super(ResConfigSettings, self).get_values()
#         res.update(
#             default_supplier_id=int(self.env['ir.config_parameter'].sudo().get_param('mzuri_sale_factory_orders.default_supplier_id', default=0))
#         )
#         return res
#
#     def set_values(self):
#         super(ResConfigSettings, self).set_values()
#         self.env['ir.config_parameter'].sudo().set_param('mzuri_sale_factory_orders.default_supplier_id', self.default_supplier_id.id)
