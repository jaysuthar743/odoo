from odoo import api, fields, models, _, exceptions


class Patient(models.Model):
    _name = 'hospital.patient'
    _description = 'hospital patient Model'
    _rec_name = "name"

    name = fields.Char(string='Name', required=True, help='Patient Name')
    age = fields.Integer(string='Age', required=True, help='Patient Age')
    notes = fields.Text(string='Notes', required=True, help='Patient Notes')
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], string='State', readonly=True, default='draft')
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')
    patient_tablet_line_id = fields.One2many('hospital.patient.tablet.line', 'patient_tablet_ids', string='Tablet Line')
    image = fields.Binary(string="Patient Image")
    total = fields.Integer(string='Total', compute="_calculate_total_amount", readonly=True) # Grand Total

    _sql_constraints = [
        ('valid_age',
         'CHECK(age > 17)',
         "Age Must be More than 17")
    ]

    def action_done(self):
        for rec in self:
            rec.state = 'done'
            for tab in rec.patient_tablet_line_id:
                if tab.tablet_ids.qty <= 0:
                    raise exceptions.ValidationError(_('Sorry! %s Tablet Not In Stock', tab.tablet_ids.name))
                tab.tablet_ids.qty -= tab.tablet_qty

    @api.depends("patient_tablet_line_id.total_price")
    def _calculate_total_amount(self):
        t = 0  # total
        for rec in self:
            for r in rec.patient_tablet_line_id:
                t += r.total_price
            rec.total = t
