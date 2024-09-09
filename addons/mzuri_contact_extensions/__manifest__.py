{
    'name': 'Mzuri Contact Extensions',
    'version': '1.1',
    'summary': 'Rozszerzenia dla kontaktów, dodające produkty do zainteresowań i posiadanych',
    'description': """
        Moduł rozszerza model res.partner, dodając możliwość przypisywania produktów 
        do kategorii 'zainteresowania' oraz 'posiadane/park maszynowy'.
    """,
    'category': 'Contacts',
    'author': 'Piotr Wawrzyniak',
    'depends': ['base', 'product', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/sale_order_view.xml',
        # 'views/sale_order_tree_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
    'i18n': ['i18n/pl.po', 'i18n/en.po', 'i18n/ru.po'],  # Dodaj to, aby upewnić się, że plik tłumaczeń zostanie załadowany
}
