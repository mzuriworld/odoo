# mzuri_security/__manifest__.py
{
    'name': 'Mzuri Security',
    'version': '1.0',
    'category': 'Security',
    'summary': 'Manage user groups and permissions for dealers and Mzuri employees',
    'author': 'Piotr Wawrzyniak',
    'depends': ['base', 'sale', 'purchase', 'repair'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        'views/security_views.xml',

    ],
    'installable': True,
    'application': True,
}
