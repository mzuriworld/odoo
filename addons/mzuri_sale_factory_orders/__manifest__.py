{
    'name': 'Mzuri Sales Factory Orders',
    'version': '1.1',
    'summary': 'Integracja modułów Sale i Purchase w celu wyświetlania i kopiowania konfiguracji produktów.',
    'description': """
        Moduł łączy moduły Sale i Purchase, umożliwiając wyświetlanie sprzedanych produktów wraz z konfiguracją 
        w module Purchase oraz kopiowanie i edytowanie tych produktów przy użyciu konfiguratorem z Sale.
    """,
    'category': 'Sales',
    'author': 'Piotr Wawrzyniak',
    'depends': ['sale', 'purchase', 'sale_product_configurator'],
    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',  # Plik z grupami uprawnień
        'views/purchase_order_views.xml',
        'views/sale_order_views.xml',
        'views/purchase_order_line.xml',
        # 'views/res_config_settings_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'mzuri_sale_factory_orders/static/src/js/product_configurator_widget.js',
            # 'sale_product_configurator/static/src/js/product_configurator_dialog.js',
        ],
    },

    # 'assets': {
    #     'web.assets_backend': [
    #         'mzuri_sale_factory_orders/static/src/js/purchase_order_line_configurator.js',
    #     ],
    # },
    'installable': True,
    'application': False,
}
