# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sales_limit = fields.Float(string='Sales Limit', config_parameter="sales_approve.sales_limit")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res['sales_limit'] = (self.env['ir.config_parameter'].sudo().get_param('sales_approve.sales_limit',
                                                                               default=0))
        return res

    @api.model
    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param('sales_approve.sales_limit', self.sales_limit)
        super(ResConfigSettings, self).set_values()


class SalesSelectionAdd(models.Model):
    _inherit = "sale.order"

    state = fields.Selection(selection_add=[('to_approve', 'To Approve'), ('sale', 'Sale Order')])

    def action_to_approve(self):
        self.state = 'sale'

    def action_confirm(self):
        res = super(SalesSelectionAdd, self).action_confirm()
        sales_limit = self.env['ir.config_parameter'].sudo().get_param('sales_approve.sales_limit') or False
        if sales_limit:
            if float(self.amount_total) > float(sales_limit):
                self.state = 'to_approve'
        return res
