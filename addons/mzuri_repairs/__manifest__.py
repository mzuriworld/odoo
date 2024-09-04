{
    'name': 'Mzuri Repairs',
    'version': '1.0',
    'category': 'Repairs',
    'summary': 'Customizations for Repair Management',
    'description': """
    This module customizes the Odoo Repair module to add a kanban view for repair requests similar to the maintenance module.
    """,
    'author': 'Piotr Wawrzyniak',
    'depends': ['repair', 'maintenance'],
    'data': [
        'views/repair_order_kanban_view.xml',
        'views/repair_view.xml',
        'views/repair_order_action.xml',
        'views/repair_order_view.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
