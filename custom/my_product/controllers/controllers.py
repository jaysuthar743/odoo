# -*- coding: utf-8 -*-
# from odoo import http


# class MyProduct(http.Controller):
#     @http.route('/my_product/my_product/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/my_product/my_product/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('my_product.listing', {
#             'root': '/my_product/my_product',
#             'objects': http.request.env['my_product.my_product'].search([]),
#         })

#     @http.route('/my_product/my_product/objects/<model("my_product.my_product"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('my_product.object', {
#             'object': obj
#         })
