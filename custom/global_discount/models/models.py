# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _


class SalesGlobalDiscount(models.Model):
    _inherit = "sale.order"

    discount_type = fields.Selection([('amount', 'Amount'),
                                      ('percentage', 'Percentage')],
                                     string="Discount Type",
                                     default='percentage')
    global_discount = fields.Float(string="Global Discount")
    apply_discount = fields.Boolean(string="Apply Discount")

    @api.onchange('apply_discount')
    def add_discount_order_line(self):
        prods = []
        for res in self.order_line.product_id:
            prods.append(res.name)
        if 'Restaurant Expenses' not in prods:
            if self.apply_discount:
                self.write({
                    'order_line': [(0, 0, {
                        'product_id': 45,
                        'name': 'discount'})]
                    })

        if 'Restaurant Expenses' in prods and not self.apply_discount:
            for line in self.order_line:
                for prod_id in line.product_id:
                    if prod_id.name == 'Restaurant Expenses':
                        self.write({
                            'order_line': [(3, line.id, 0)]
                        })

    @api.constrains("global_discount")
    def validate_global_discount(self):
        if self.discount_type == 'percentage' and (self.global_discount < 0 or self.global_discount > 100):
            raise exceptions.ValidationError(_('Percentage Should be between 1 to 100 !'))
        elif self.discount_type == 'amount' and (self.global_discount > self.amount_total):
            raise exceptions.ValidationError(_('Amount Should not be more than Total Amount !'))

    @api.depends("discount_type", "global_discount")
    def _amount_all(self):
        res = super(SalesGlobalDiscount, self)._amount_all()
        for rec in self:
            if rec.discount_type == 'amount':
                rec.amount_total = rec.amount_total - rec.global_discount
            elif rec.discount_type == 'percentage':
                rec.amount_total = rec.amount_total - (rec.amount_total * rec.global_discount / 100)
        return res



