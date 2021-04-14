# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class authorize_payment_custom(models.Model):
#     _name = 'authorize_payment_custom.authorize_payment_custom'
#     _description = 'authorize_payment_custom.authorize_payment_custom'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
