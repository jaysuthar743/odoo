from odoo import api, fields, models, _ , exceptions


class Doctor(models.Model):
    _name = 'hospital.doctor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'hospital doctor Model'
    _rec_name = "name"

    name = fields.Char(string='Name', required=True, help='Doctor Name')
    age = fields.Integer(string='Age', required=True, help='Doctor Age')
    patient_ids = fields.One2many('hospital.patient', 'doctor_id', string='Patient')
