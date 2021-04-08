# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order.line'

    img = fields.Image(related="product_id.image_512")


class StockMove(models.Model):
    _inherit = 'stock.move'

    img = fields.Image(related="product_id.image_512")


class AccountMove(models.Model):
    _inherit = 'account.move.line'

    img = fields.Image(related="product_id.image_512")
