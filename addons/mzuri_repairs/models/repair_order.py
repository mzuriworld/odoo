from odoo import models, fields, api

class RepairOrder(models.Model):
    _inherit = 'repair.order'

    partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    product_owned_id = fields.Many2one(
        'res.partner.product.owned',
        string="Product to Repair",
        domain="[('partner_id', '=', partner_id)]"
    )

    team = fields.Many2one(
        'res.partner',
        string='Team',
        domain=[('is_company', '=', True)],
        help='Select the team handling the repair.'
    )

    report_date = fields.Datetime(string="Data zgłoszenia", default=fields.Datetime.now, readonly=True)
    event_date = fields.Date(string="Data zdarzenia")
    fault_description = fields.Text(string="Opis usterki")
    worked_hours = fields.Float(string="Przepracowane godziny", required=True)

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self.product_owned_id = False  # Reset the product field when the customer is changed


    @api.model
    def days_between(self, start_date, end_date):
        if start_date and end_date:
            start = fields.Date.from_string(start_date)
            end = fields.Date.from_string(end_date)
            return (end - start).days
        return 0

    # Field to store photos related to the repair request
    request_photo_ids = fields.Many2many(
        'ir.attachment',
        'repair_order_request_photos_rel',  # Unique table name for this Many2many relation
        'repair_order_id', 'attachment_id',
        string='Request Photos',
        help='Photos related to the initial repair request'
    )

    # Field to store photos related to the repair process
    repair_photo_ids = fields.Many2many(
        'ir.attachment',
        'repair_order_repair_photos_rel',  # Unique table name for this Many2many relation
        'repair_order_id', 'attachment_id',
        string='Repair Photos',
        help='Photos related to the actual repair process'
    )

    @api.constrains('state', 'repair_photo_ids')
    def _check_repair_photos(self):
        """Ensure that repair photos are uploaded before marking the repair as done."""
        for record in self:
            if record.state == 'done' and not record.repair_photo_ids:
                raise models.ValidationError("You must add at least one photo of the repair before marking it as done.")