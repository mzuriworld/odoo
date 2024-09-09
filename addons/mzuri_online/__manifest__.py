{
    'name': 'Mzuri Online',
    'version': '1.0',
    'category': 'Custom',
    'summary': 'Remove My Odoo.com Account link from user menu',
    'description': """
        This module removes the "My Odoo.com Account" link from the user menu.
    """,
    'author': 'Piotr Wawrzyniak',
    'depends': ['web'],
    'data': [
        'views/assets.xml',
    ],
    # 'assets': {
    #     'web.assets_backend': [
    #         'mzuri_online/static/src/js/user_menu.js',
    #     ],
    # },
    'installable': True,
    'application': False,
}
