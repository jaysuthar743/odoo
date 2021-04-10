# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import datetime


class AppointmentWebsite(http.Controller):
    @http.route('/appointment/webform', auth='public', type="http", website=True)
    def appointment_form(self, **kw):
        return http.request.render('appointment_website.appointment_page_template', {'name': 'Jay Suthar'})

    @http.route('/create/appointment', auth='public', type="http", website=True)
    def create_appointment(self, **kw):
        # dob = datetime.datetime.strptime(kw.get('dob', datetime.datetime.today()), "%d/%m/%Y").strftime('%Y-%m-%d')
        # kw.update({
        #     'dob': dob
        # })
        request.env['doctor.appointment'].sudo().create(kw)
        return request.render('appointment_website.appointment_thank_you_page_template', {})

