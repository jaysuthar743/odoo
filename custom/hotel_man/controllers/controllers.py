# -*- coding: utf-8 -*-
# from odoo import http


# class HotelMan(http.Controller):
#     @http.route('/hotel_man/hotel_man/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hotel_man/hotel_man/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hotel_man.listing', {
#             'root': '/hotel_man/hotel_man',
#             'objects': http.request.env['hotel_man.hotel_man'].search([]),
#         })

#     @http.route('/hotel_man/hotel_man/objects/<model("hotel_man.hotel_man"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hotel_man.object', {
#             'object': obj
#         })
