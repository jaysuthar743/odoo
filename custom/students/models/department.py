from odoo import api, fields, models, _, exceptions


class Department(models.Model):
    _name = 'department'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Basic Department Model'

    name = fields.Char(string='Name', required=True)
    code = fields.Integer(string='Department Code', required=True)
