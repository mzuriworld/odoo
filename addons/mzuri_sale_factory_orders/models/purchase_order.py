from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    sale_order_id = fields.Many2one('sale.order', string="Powiązane Zamówienie Sprzedaży")

    @api.model
    def create(self, vals):
        if not vals.get('partner_id'):
            default_supplier_id = int(self.env['ir.config_parameter'].sudo().get_param('mzuri_sale_factory_orders.default_supplier_id', default=0))
            if default_supplier_id:
                vals['partner_id'] = default_supplier_id
        return super(PurchaseOrder, self).create(vals)

    @api.onchange('sale_order_id')
    def _onchange_sale_order_id(self):
        if self.sale_order_id:
            sale_order_lines = self.sale_order_id.order_line
            self.order_line = [(5, 0, 0)]  # Usunięcie istniejących linii zamówienia zakupu
            for line in sale_order_lines:
                # Pobieramy atrybuty produktu i numery katalogowe
                attributes_with_catalogue_numbers = []
                for attribute_value in line.product_id.product_template_attribute_value_ids:
                    if attribute_value.catalogue_number:
                        attributes_with_catalogue_numbers.append(f"{attribute_value.name} (Cat. No: {attribute_value.catalogue_number})")
                    else:
                        attributes_with_catalogue_numbers.append(attribute_value.name)

                # Tworzymy opis z nazwą i numerami katalogowymi
                description = f"{line.name}\n" + ", ".join(attributes_with_catalogue_numbers)

                self.order_line = [(0, 0, {
                    'product_id': line.product_id.id,
                    'name': description,  # Dodajemy opis z numerami katalogowymi
                    'product_qty': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'date_planned': fields.Datetime.now(),
                    'product_uom': line.product_uom.id,
                    'sale_order_line_id': line.id,
                })]


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    sale_order_line_id = fields.Many2one('sale.order.line', string="Related Sale Order Line")
    product_config = fields.Char(string="Product Configuration")

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id and self.sale_order_line_id:
            self.product_config = self.sale_order_line_id.product_config

    def action_view_configurator(self):
        self.ensure_one()
        action = self.env["sale_product_configurator"].with_context(
            default_order_id=self.order_id.id,
            default_product_id=self.product_id.id,
            default_line_id=self.id,
        ).action_configure_product()
        return action


# from odoo import models, fields, api
#
#
# class PurchaseOrder(models.Model):
#     _inherit = 'purchase.order'
#
#     sale_order_id = fields.Many2one('sale.order', string="Powiązane Zamówienie Sprzedaży")
#
#     @api.onchange('sale_order_id')
#     def _onchange_sale_order_id(self):
#         if self.sale_order_id:
#             sale_order_lines = self.sale_order_id.order_line
#             self.order_line = [(5, 0, 0)]  # Usunięcie istniejących linii zamówienia zakupu
#             for line in sale_order_lines:
#                 # Pobieramy atrybuty produktu i numery katalogowe
#                 attributes_with_catalogue_numbers = []
#                 for attribute_value in line.product_id.product_template_attribute_value_ids:
#                     if attribute_value.catalogue_number:
#                         attributes_with_catalogue_numbers.append(
#                             f"{attribute_value.name} (Cat. No: {attribute_value.catalogue_number})")
#                     else:
#                         attributes_with_catalogue_numbers.append(attribute_value.name)
#
#                 # Tworzymy opis z nazwą i numerami katalogowymi
#                 description = f"{line.name}\n" + ", ".join(attributes_with_catalogue_numbers)
#
#                 self.order_line = [(0, 0, {
#                     'product_id': line.product_id.id,
#                     'name': description,  # Dodajemy opis z numerami katalogowymi
#                     'product_qty': line.product_uom_qty,
#                     'price_unit': line.price_unit,
#                     'date_planned': fields.Datetime.now(),
#                     'product_uom': line.product_uom.id,
#                     'sale_order_line_id': line.id,
#                 })]
#
#
# class PurchaseOrderLine(models.Model):
#     _inherit = 'purchase.order.line'
#
#     sale_order_line_id = fields.Many2one('sale.order.line', string="Related Sale Order Line")
#     product_config = fields.Char(string="Product Configuration")
#
#     @api.onchange('product_id')
#     def _onchange_product_id(self):
#         if self.product_id and self.sale_order_line_id:
#             self.product_config = self.sale_order_line_id.product_config
#
#     def action_view_configurator(self):
#         self.ensure_one()
#         action = self.env["sale_product_configurator"].with_context(
#             default_order_id=self.order_id.id,
#             default_product_id=self.product_id.id,
#             default_line_id=self.id,
#         ).action_configure_product()
#         return action
#
# # from odoo import models, fields, api
# #
# # class PurchaseOrder(models.Model):
# #     _inherit = 'purchase.order'
# #
# #     sale_order_id = fields.Many2one('sale.order', string="Powiązane Zamówienie Sprzedaży")
# #
# #
# #
# #     @api.onchange('sale_order_id')
# #     def _onchange_sale_order_id(self):
# #         if self.sale_order_id:
# #             sale_order_lines = self.sale_order_id.order_line
# #             self.order_line = [(5, 0, 0)]  # Usunięcie istniejących linii zamówienia zakupu
# #             for line in sale_order_lines:
# #                 self.order_line = [(0, 0, {
# #                     'product_id': line.product_id.id,
# #                     'name': line.name,
# #                     'product_qty': line.product_uom_qty,
# #                     'price_unit': line.price_unit,
# #                     'date_planned': fields.Datetime.now(),
# #                     'product_uom': line.product_uom.id,
# #                     'sale_order_line_id': line.id,
# #                 })]
# #
# #
# # class PurchaseOrderLine(models.Model):
# #     _inherit = 'purchase.order.line'
# #
# #     sale_order_line_id = fields.Many2one('sale.order.line', string="Related Sale Order Line")
# #     product_config = fields.Char(string="Product Configuration")
# #
# #     @api.onchange('product_id')
# #     def _onchange_product_id(self):
# #         if self.product_id and self.sale_order_line_id:
# #             self.product_config = self.sale_order_line_id.product_config
# #
# #     def action_view_configurator(self):
# #         self.ensure_one()
# #         action = self.env["sale_product_configurator"].with_context(
# #             default_order_id=self.order_id.id,
# #             default_product_id=self.product_id.id,
# #             default_line_id=self.id,
# #         ).action_configure_product()
# #         return action
# #     # def action_view_configurator(self):
# #     #     return {
# #     #         'name': 'Product Configurator',
# #     #         'type': 'ir.actions.act_window',
# #     #         'res_model': 'product.configurator',
# #     #         'view_mode': 'form',
# #     #         'target': 'new',
# #     #         'context': {
# #     #             'default_product_id': self.product_id.id,
# #     #             'default_sale_order_line_id': self.sale_order_line_id.id,
# #     #             'default_purchase_order_line_id': self.id,
# #     #         },
# #     #     }
