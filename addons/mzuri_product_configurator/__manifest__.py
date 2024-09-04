{
    'name': 'Mzuri Product Configurator',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Custom Product Configurator',
    'description': """
        Custom Product Configurator
    """,
    'author': 'Your Company',
    'depends': ['sale', 'product'],
    'data': [
        'views/sale_product_configurator_dialog_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'mzuri_product_configurator/static/src/js/product_configurator_dialog.js',
            'mzuri_product_configurator/static/src/xml/product_configurator_dialog_template.xml',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
}
