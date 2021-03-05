from odoo import api, fields, models, _, exceptions


class TabletLine(models.Model):
    _name = 'hospital.patient.tablet.line'
    _description = 'hospital patient tablet line Model'

    tablet_ids = fields.Many2one('hospital.patient.tablet', string='Tablets', domain=[('qty', '>=', 1)])
    patient_tablet_ids = fields.Many2one('hospital.patient', string='Patients')
    tablet_qty = fields.Integer(string='Qty.')
    tablet_price = fields.Integer(string='Price')
    total_price = fields.Integer(string='Total', readonly=True)

    @api.onchange("tablet_qty", "tablet_price")
    def _calculate_total(self):
        for rec in self:
            if rec.tablet_qty > rec.tablet_ids.qty:
                rec.tablet_qty = rec.tablet_ids.qty
                rec.total_price = rec.tablet_ids.qty
                raise exceptions.ValidationError(_('Sorry, %s Tablet Not In Stock. \nAvailable Qty: %d',
                                                   rec.tablet_ids.name, rec.tablet_ids.qty))
            rec.total_price = rec.tablet_price*rec.tablet_qty
