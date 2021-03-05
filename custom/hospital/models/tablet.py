from odoo import api, fields, models, _, exceptions


class Tablet(models.Model):
    _name = 'hospital.patient.tablet'
    _description = 'hospital patient tablet Model'

    name = fields.Char(string='Name', required=True, help='Tablet Name')
    qty = fields.Integer(string='Qty.', required=True, help='Tablet Qty.')

    @api.constrains("qty")
    def _check_qty_stock(self):
        for rec in self:
            if rec.qty <= 0:
                raise exceptions.ValidationError(_('Sorry! %s Tablet Not In Stock', rec.name))
