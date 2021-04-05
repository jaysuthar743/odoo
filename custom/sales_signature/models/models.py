# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleSignature(models.Model):
    _inherit = "sale.order"

    sale_signature = fields.Text(string="Sale Signature")

    def action_view_delivery(self):
        res = super(SaleSignature, self).action_view_delivery()
        self.picking_ids.write({'sale_signature': self.sale_signature})
        return res

    def action_view_invoice(self):
        res = super(SaleSignature, self).action_view_invoice()
        self.invoice_ids.write({'sale_signature': self.sale_signature})
        return res


class StockPickingSignature(models.Model):
    _inherit = "stock.picking"

    sale_signature = fields.Text(string="Signature")


class AccountMoveSignature(models.Model):
    _inherit = "account.move"

    sale_signature = fields.Text(string="Signature")
