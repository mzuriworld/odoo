{
    'name': 'Mzuri Sale PDF Preview',
    'version': '1.0',
    'summary': 'Zastępuje przycisk Preview przyciskiem do generowania PDF w ofercie sprzedaży',
    'description': """
        Ten moduł zastępuje przycisk "Preview" w widoku oferty sprzedaży (quotation) przyciskiem "Podgląd PDF", 
        który generuje standardowy PDF oferty.
    """,
    'category': 'Sales',
    'author': 'Piotr Wawrzyniak',
    'depends': ['sale'],
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
}
