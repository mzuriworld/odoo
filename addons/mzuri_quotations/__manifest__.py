{
    'name': 'Mzuri Quotations',
    'version': '1.1',
    'summary': 'Extension for generating quotations',
    'description': 'Adds a "quotation description" field to products and product attribute lines.',
    'author': 'Piotr Wawrzyniak',
    'website': 'https://inodata.pl',
    'category': 'Sales',
    'depends': ['product', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',  # Widoki (przyciski, formularze)
        'views/product_template_views.xml',
    ],
    'installable': True,
    'application': False,
}
