{
    'name': 'Mzuri Client Onboarding',
    'version': '1.1',
    'summary': 'Onboarding dla nowych klientów, w tym potwierdzenie danych i zgody na kontakt.',
    'description': """
        Moduł dodaje kroki onboardingowe dla klientów w Odoo, w tym wysyłanie e-maila do klienta 
        z prośbą o potwierdzenie danych oraz wyrażenie zgód na kontakt i przetwarzanie danych osobowych.
    """,
    'category': 'CRM',
    'author': 'Piotr Wawrzyniak',
    'depends': ['base', 'crm', 'contacts'],
    'data': [
        'security/onboarding_access_rules.xml',
        'data/ir_config_parameter_data.xml',
        'data/mail_template_data.xml',
        'views/onboarding_confirmation.xml',
        'views/onboarding_success.xml',
        'views/onboarding_token_invalid.xml',
        'views/res_partner_views.xml',
        'data/website_pages_data.xml',  # Dodajemy plik z rejestracją stron
    ],
    'installable': True,
    'application': False,
}
