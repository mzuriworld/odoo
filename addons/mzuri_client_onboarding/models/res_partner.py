# import hashlib
# import werkzeug
# from datetime import timedelta
# from odoo import models, fields, api
# from odoo.exceptions import AccessDenied
#
# class ResPartner(models.Model):
#     _inherit = 'res.partner'
#
#     consent_email = fields.Boolean(string="Consent to Email Contact")
#     consent_phone = fields.Boolean(string="Consent to Phone Contact")
#     consent_sms = fields.Boolean(string="Consent to SMS Contact")
#     consent_data_processing = fields.Boolean(string="Consent to Data Processing")
#     onboarding_completed = fields.Boolean(string="Onboarding Completed", default=False)
#     onboarding_token = fields.Char(string="Onboarding Token")
#     onboarding_token_expiry = fields.Datetime(string="Onboarding Token Expiry", default=lambda self: fields.Datetime.now() + timedelta(hours=72))
#
#     def generate_onboarding_token(self):
#         """Generates a token and sets its expiry time."""
#         token = hashlib.sha256(f"{self.id}{self.email}{fields.Datetime.now()}".encode('utf-8')).hexdigest()
#         expiry_time = fields.Datetime.now() + timedelta(hours=int(self.env['ir.config_parameter'].sudo().get_param('mzuri.onboarding_token_duration', 72)))
#         self.write({
#             'onboarding_token': token,
#             'onboarding_token_expiry': expiry_time
#         })
#         return token
#
#     def get_onboarding_url(self):
#         base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
#         return werkzeug.urls.url_join(base_url, f'/customer/onboarding/{self.id}?token={self.onboarding_token}')
#
#     def action_onboarding_confirm(self, token):
#         partner = self.browse(self.id)
#         if not partner._is_token_valid(token):
#             return werkzeug.exceptions.Forbidden()
#         partner.onboarding_completed = True
#         return {
#             'type': 'ir.actions.client',
#             'tag': 'reload',
#         }
#
#     def _is_token_valid(self, token):
#         """Checks if the provided token is valid and not expired."""
#         return self.onboarding_token == token and self.onboarding_token_expiry > fields.Datetime.now()
#
#     @api.model_create_multi
#     def create(self, vals_list):
#         records = super(ResPartner, self).create(vals_list)
#         for record in records:
#             # Generate token and send onboarding email
#             record.generate_onboarding_token()
#             record._send_onboarding_email()
#         return records
#
#     def _send_onboarding_email(self):
#         template = self.env.ref('mzuri_client_onboarding.email_template_customer_onboarding')
#         if template and self.email:
#             template.send_mail(self.id, force_send=True)


import hashlib
import werkzeug
from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import AccessDenied

class ResPartner(models.Model):
    _inherit = 'res.partner'

    consent_email = fields.Boolean(string="Consent to Email Contact")
    consent_phone = fields.Boolean(string="Consent to Phone Contact")
    consent_sms = fields.Boolean(string="Consent to SMS Contact")
    consent_data_processing = fields.Boolean(string="Consent to Data Processing")
    onboarding_completed = fields.Boolean(string="Onboarding Completed", default=False)
    onboarding_token = fields.Char(string="Onboarding Token")
    onboarding_token_expiry = fields.Datetime(string="Onboarding Token Expiry", default=lambda self: fields.Datetime.now() + timedelta(hours=72))
    onboarding_token_used = fields.Boolean(string="Onboarding Token Used", default=False)

    def generate_onboarding_token(self):
        """Generates a token and sets its expiry time."""
        token = hashlib.sha256(f"{self.id}{self.email}{fields.Datetime.now()}".encode('utf-8')).hexdigest()
        expiry_time = fields.Datetime.now() + timedelta(hours=int(self.env['ir.config_parameter'].sudo().get_param('mzuri.onboarding_token_duration', 72)))
        self.write({
            'onboarding_token': token,
            'onboarding_token_expiry': expiry_time,
            'onboarding_token_used': False,
        })
        return token

    def get_onboarding_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return werkzeug.urls.url_join(base_url, f'/customer/onboarding/{self.id}?token={self.onboarding_token}')

    def action_onboarding_confirm(self, token):
        partner = self.browse(self.id)
        if not partner._is_token_valid(token):
            return werkzeug.exceptions.Forbidden()
        partner.onboarding_completed = True
        partner.onboarding_token_used = True
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def _is_token_valid(self, token):
        """Checks if the provided token is valid, not expired, and not used."""
        return (self.onboarding_token == token and
                self.onboarding_token_expiry > fields.Datetime.now() and
                not self.onboarding_token_used)

    @api.model_create_multi
    def create(self, vals_list):
        records = super(ResPartner, self).create(vals_list)
        for record in records:
            # Generate token and send onboarding email
            record.generate_onboarding_token()
            record._send_onboarding_email()
        return records

    def _send_onboarding_email(self):
        template = self.env.ref('mzuri_client_onboarding.email_template_customer_onboarding')
        if template and self.email:
            template.send_mail(self.id, force_send=True)
