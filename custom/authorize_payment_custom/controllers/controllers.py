# -*- coding: utf-8 -*-
# from odoo import http


# class AuthorizePaymentCustom(http.Controller):
#     @http.route('/authorize_payment_custom/authorize_payment_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/authorize_payment_custom/authorize_payment_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('authorize_payment_custom.listing', {
#             'root': '/authorize_payment_custom/authorize_payment_custom',
#             'objects': http.request.env['authorize_payment_custom.authorize_payment_custom'].search([]),
#         })

#     @http.route('/authorize_payment_custom/authorize_payment_custom/objects/<model("authorize_payment_custom.authorize_payment_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('authorize_payment_custom.object', {
#             'object': obj
#         })
