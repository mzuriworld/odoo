{
    'name': 'Mzuri Stock Customizations',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Add serial number to products and control when it is assigned.',
    'description': """
        This module adds a serial number to products, which can only be assigned when a purchase order is sent to a dealer.
    """,
    'author': 'Piotr Wawrzyniak',
    'depends': ['purchase', 'stock', 'product'],  # Depends on Purchase, Stock, and Product modules
    'data': [
        'views/serial_number_wizard_view.xml',
        'views/actions.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
}
