{
    'name': 'Mzuri PDF Quotation',
    'version': '1.0',
    'category': 'Sales',
    'author': 'Piotr Wawrzyniak',
    'summary': 'Generate dynamic PDF quotations with custom backgrounds',
    'depends': ['sale', 'base'],
    'data': [
        # 'views/sale_order_views.xml',
        'report/sale_order_report_template.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'mzuri_pdf_quotation/static/src/css/custom_style.css',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
