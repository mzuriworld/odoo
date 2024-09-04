# from odoo import http
# from odoo.http import request
# from odoo.exceptions import AccessDenied
#
#
# class CustomerOnboardingController(http.Controller):
#
#     @http.route('/customer/onboarding/<int:partner_id>', type='http', auth="public", website=True)
#     def customer_onboarding(self, partner_id, token, **kwargs):
#         partner = request.env['res.partner'].sudo().browse(partner_id)
#         if not partner:
#             return request.not_found()
#
#         # Sprawdzenie, czy token jest prawidłowy
#         if not partner._is_token_valid(token):
#             return request.render('http_routing.403')
#
#         return request.render('mzuri_client_onboarding.onboarding_confirmation_page', {'partner': partner})


# from odoo import http
# from odoo.http import request
# from odoo.exceptions import AccessDenied
#
#
# class CustomerOnboardingController(http.Controller):
#
#     @http.route('/customer/onboarding/<int:partner_id>', type='http', auth="public", website=True)
#     def customer_onboarding(self, partner_id, token, **kwargs):
#         partner = request.env['res.partner'].sudo().browse(partner_id)
#         if not partner:
#             return request.not_found()
#
#         # Sprawdzenie, czy token jest prawidłowy
#         if not partner._is_token_valid(token):
#             return request.render('http_routing.403')
#
#         return request.render('mzuri_client_onboarding.onboarding_confirmation_page', {'partner': partner})
#
#     @http.route('/customer/onboarding/confirm', type='http', auth="public", website=True, methods=['POST'])
#     def customer_onboarding_confirm(self, **kwargs):
#         partner_id = int(kwargs.get('partner_id'))
#         token = kwargs.get('token')
#
#         partner = request.env['res.partner'].sudo().browse(partner_id)
#         if not partner or not partner._is_token_valid(token):
#             return request.render('http_routing.403')
#
#         # Zapisz wybory użytkownika
#         partner.write({
#             'consent_email': 'consent_email' in kwargs,
#             'consent_phone': 'consent_phone' in kwargs,
#             'consent_sms': 'consent_sms' in kwargs,
#             'consent_data_processing': 'consent_data_processing' in kwargs,
#             'onboarding_completed': True,
#         })
#
#         return request.render('mzuri_client_onboarding.onboarding_success_page', {'partner': partner})


from odoo import http
from odoo.http import request
from odoo.exceptions import AccessDenied


class CustomerOnboardingController(http.Controller):

    @http.route('/customer/onboarding/<int:partner_id>', type='http', auth="public", website=True)
    def customer_onboarding(self, partner_id, token, **kwargs):
        partner = request.env['res.partner'].sudo().browse(partner_id)
        if not partner:
            return request.not_found()

        # Sprawdzenie, czy token jest prawidłowy
        if not partner._is_token_valid(token):
            return request.render('mzuri_client_onboarding.onboarding_token_invalid')

        return request.render('mzuri_client_onboarding.onboarding_confirmation_page', {'partner': partner})

    @http.route('/customer/onboarding/confirm', type='http', auth="public", website=True, methods=['POST'])
    def customer_onboarding_confirm(self, **kwargs):
        partner_id = int(kwargs.get('partner_id'))
        token = kwargs.get('token')

        partner = request.env['res.partner'].sudo().browse(partner_id)
        if not partner or not partner._is_token_valid(token):
            return request.render('mzuri_client_onboarding.onboarding_token_invalid')

        # Zapisz wybory użytkownika
        partner.write({
            'consent_email': 'consent_email' in kwargs,
            'consent_phone': 'consent_phone' in kwargs,
            'consent_sms': 'consent_sms' in kwargs,
            'consent_data_processing': 'consent_data_processing' in kwargs,
            'onboarding_completed': True,
            'onboarding_token_used': True,
        })

        return request.render('mzuri_client_onboarding.onboarding_success_page', {'partner': partner})
