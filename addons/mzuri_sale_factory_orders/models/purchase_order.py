from odoo import models, fields, api
import logging
import json

_logger = logging.getLogger(__name__)
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    sale_order_id = fields.Many2one('sale.order', string="Powiązane Zamówienie Sprzedaży")

    # partner_id = fields.Many2one('res.partner', readonly=True, default=1)

    def default_get(self, fields):
        res = super(PurchaseOrder, self).default_get(fields)
        res['partner_id'] = 1  # Ustawienie domyślnej wartości na partner_id = 1
        return res

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
                # print(json.dumps(dir(line.product_id)))
                # for attr in dir(line.product_id):
                #     print("line.product_id.%s = %r" % (attr, getattr(line.product_id, attr)))

                attributes_with_catalogue_numbers = []
                # print(len(line.product_id.product_template_attribute_value_ids))

                for attribute_value in line.product_id.product_template_attribute_value_ids:
                    for attr in dir(attribute_value):
                        print("attribute_value.%s = %r" % (attr, getattr(attribute_value, attr)))
                    # print (attribute_value)
                    if attribute_value.catalogue_number:
                        attributes_with_catalogue_numbers.append(f"{attribute_value.name} ({attribute_value.catalogue_number})")
                    else:
                        attributes_with_catalogue_numbers.append(attribute_value.name)

                # Tworzymy opis z nazwą i numerami katalogowymi
                description = f", ".join(attributes_with_catalogue_numbers)
                print(description)
#{line.name}\n" +
                name = line.product_id.name
                catalogue_number = list(line.product_id.product_tmpl_id.product_properties.values())[0] or ''
                # Modyfikujemy nazwę, dodając numer katalogowy
                display_name = f"{name} ({catalogue_number})"
                # print(name)
                # print(catalogue_number)
                # print(display_name)

                # Tworzymy opis z nazwą i numerami katalogowymi
                description = f"{display_name}\n" + description

                # Pobieramy bazową cenę z 'product.template'
                base_price = line.product_id.product_tmpl_id.list_price
                print(base_price)

                # Możemy tu dodać dodatkowe obliczenia w zależności od atrybutów i opcji
                option_price = sum(
                    value.price_extra for value in  line.product_id.product_template_attribute_value_ids
                )
                base_price_tot = base_price + option_price
                print(base_price_tot)
                #
                # line.price_unit = base_price_tot

                self.order_line = [(0, 0, {
                    'product_id': line.product_id.id,
                    'name': line.name, #description,  # Dodajemy opis z numerami katalogowymi
                    'product_qty': line.product_uom_qty,
                    'price_unit': base_price_tot,
                    'date_planned': fields.Datetime.now(),
                    'product_uom': line.product_uom.id,
                    'sale_order_line_id': line.id,
                })]

    # @api.onchange('sale_order_id')
    # def _onchange_product_id_update_price(self):
    #     """
    #     Aktualizuje cenę jednostkową na podstawie ceny z 'product.template' oraz opcji.
    #     """
    #     if self.sale_order_id:
    #         sale_order_lines = self.sale_order_id.order_line
    #         for line in sale_order_lines:
    #             if line.product_id:
    #                 # Bazowa cena z product.template
    #                 base_price = line.product_id.product_tmpl_id.list_price
    #
    #                 # Dodajemy cenę za opcje/atrybuty, jeśli są wybrane
    #                 option_price = sum(
    #                     value.price_extra for value in line.product_custom_attribute_value_ids
    #                 )
    #
    #                 # Ustawiamy obliczoną cenę jako price_unit
    #                 pr = base_price + option_price
    #                 print(pr)
    #                 line.price_unit = pr
    #             else:
    #                 line.price_unit = 0.0
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    sale_order_line_id = fields.Many2one('sale.order.line', string="Related Sale Order Line")
    # sale_order_line_price_unit = fields.Float(string="Unit price from sale order")
    product_config = fields.Char(string="Product Configuration")

    # @api.onchange('product_id')
    # def _onchange_product_id(self):
    #     if self.product_id and self.sale_order_line_id:
    #         self.product_config = self.sale_order_line_id.product_config
    #         result = []
    #         for record in self:
    #             name = record.product_id.display_name or ''
    #             catalogue_number = record.product_id.product_tmpl_id.product_properties or 'TEST'
    #             # Modyfikujemy nazwę, dodając numer katalogowy
    #             display_name = f"{name} ({catalogue_number})" if catalogue_number else name
    #             result.append((record.id, display_name))
    #         self.product_id.id = result

    def action_view_configurator(self):
        self.ensure_one()
        action = self.env["sale.product.configurator"].with_context(
            default_order_id=self.order_id.id,
            default_product_id=self.product_id.id,
            default_line_id=self.id,
            custom_callback="purchase_order_line_configurator_callback",
        ).action_configure_product()
        return action

    # def name_get(self):
    #     _logger.info("Metoda name_get została wywołana dla purchase.order.line")
    #     result = []
    #     for record in self:
    #         name = record.product_id.display_name or ''
    #         catalogue_number = record.product_id.product_tmpl_id.product_properties or 'TEST'
    #         # Modyfikujemy nazwę, dodając numer katalogowy
    #         display_name = f"{name} ({catalogue_number})" if catalogue_number else name
    #         result.append((record.id, display_name))
    #     return result


    # def action_view_configurator(self):
    #     self.ensure_one()
    #     action = self.env["sale_product_configurator"].with_context(
    #         default_order_id=self.order_id.id,
    #         default_product_id=self.product_id.id,
    #         default_line_id=self.id,
    #     ).action_configure_product()
    #     return action


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
