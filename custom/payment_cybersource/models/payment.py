# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PaymentAcquirerCybersource(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[
        ('cybersource', 'Cybersource')

    ], ondelete={'cybersource': 'set default'})
    cybersource_login = fields.Char(string='API Login Id', required_if_provider='cybersource', groups='base.group_user')
    cybersource_transaction_key = fields.Char(string='API Transaction Key', required_if_provider='cybersource', groups='base.group_user')


