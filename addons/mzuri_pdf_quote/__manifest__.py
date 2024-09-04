{
    'name': 'Mzuri PDF Quote',
    'version': '1.0',
    'category': 'Sales',
    'author': 'Piotr Wawrzyniak',
    'summary': 'Custom PDF Quote formats for Mzuri and dealers',
    'depends': ['sale_management', 'sale_pdf_quote_builder'],
    'data': [
        'reports/sale_order_report.xml',
        'reports/sale_report_template.xml',
    ],
    'installable': True,
    'application': False,
}
