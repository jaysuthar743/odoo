# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _


class SalesGlobalDiscount(models.Model):
    _inherit = "sale.order"

    discount_type = fields.Selection([('amount', 'Amount'), ('percentage', 'Percentage')], string="Discount Type",
                                     default='percentage')
    global_discount = fields.Float(string="Global Discount")

    @api.constrains("global_discount")
    def validate_global_discount(self):
        if self.discount_type == 'percentage' and (self.global_discount < 0 or self.global_discount > 100):
            raise exceptions.ValidationError(_('Sorry! Percentage Should not be greater than 100 !'))
        elif self.discount_type == 'amount' and (self.global_discount > self.amount_total):
            raise exceptions.ValidationError(_('Sorry! Amount Should not be more than Total Amount !'))

    @api.depends("discount_type", "global_discount")
    def _amount_all(self):
        res = super(SalesGlobalDiscount, self)._amount_all()
        if self.discount_type == 'amount':
            self.amount_total = self.amount_total - self.global_discount
        elif self.discount_type == 'percentage':
            self.amount_total = self.amount_total - (self.amount_total * self.global_discount / 100)
        return res
