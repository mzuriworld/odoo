from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    delivery_date = fields.Date(string='Data dostawy')
    delivery_condition = fields.Selection(
        [
            ('exw', 'EXW'),
            ('fca', 'FCA'),
            ('cpt', 'CPT'),
            ('cip', 'CIP'),
            ('dap', 'DAP'),
            ('dpu', 'DPU'),
            ('ddp', 'DDP')
        ],
        string='Warunki dostawy',
        default='exw',
        help='''Opis warunków dostawy:
- EXW (Ex Works): Sprzedawca udostępnia towar w swoim zakładzie lub magazynie.
- FCA (Free Carrier): Sprzedawca dostarcza towar przewoźnikowi wskazanemu przez kupującego.
- CPT (Carriage Paid To): Sprzedawca opłaca przewóz towaru do określonego miejsca.
- CIP (Carriage and Insurance Paid To): Jak CPT, ale sprzedawca również ubezpiecza towar.
- DAP (Delivered At Place): Sprzedawca dostarcza towar do określonego miejsca, bez rozładunku.
- DPU (Delivered at Place Unloaded): Sprzedawca dostarcza i rozładowuje towar w określonym miejscu.
- DDP (Delivered Duty Paid): Sprzedawca ponosi wszystkie koszty i ryzyka do momentu dostarczenia towaru do miejsca przeznaczenia, włącznie z cłami i podatkami.
'''
    )