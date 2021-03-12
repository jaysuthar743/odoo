# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.osv import expression
from lxml import etree
# from odoo.osv.orm import setup_modifiers


class MyProduct(models.Model):
    _name = 'product.brand'
    _description = 'Product Brand Model'

    name = fields.Char()
    code = fields.Integer()


class ProductExtend(models.Model):
    _inherit = ['product.product']
    _description = 'Product Brand Extend Model'

    product_brand_ids = fields.Many2one("product.brand", "Product Brand")

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        context = self.env.context
        if args is None:
            args = []
        else:
            if context.get('prod_id'):
                prod_brand_ids = self.env['product.product']._search([('product_brand_ids', "=", context.get('prod_id'))],
                                                                     limit=limit, access_rights_uid=name_get_uid)
                domain = [('id', "in", prod_brand_ids)]
            else:
                domain = []
            return self._search(domain, limit=limit, access_rights_uid=name_get_uid)
        return super(ProductExtend, self)._name_search(name, args=args, operator=operator, limit=limit,
                                                   name_get_uid=name_get_uid)


class SalesExtend(models.Model):
    _inherit = 'sale.order'
    _description = 'Sale Extend Model'

    product_brand_ids = fields.Many2one("product.brand", "Product Brand")

    @api.model
    def _fields_view_get(self, view_id=None, view_type=False, toolbar=False, submenu=False):
        res = super(SalesExtend, self)._fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=False)
        doc = etree.XML(res['arch'])
        for node in doc.xpath("//field[@name='product_brand_ids']"):
            print("\n\n\n\n\n ", node, type(node))
            node.set('required', 'True')

        res['arch'] = etree.tostring(doc)
        return res


class ResPartnerExtend(models.Model):
    _inherit = 'res.partner'

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s - %s' % (rec.name, rec.phone)))
        return res

