# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
# from custom.appointment_website.models.models import DoctorAppointment
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager


class AppointmentWebsite(http.Controller):
    @http.route('/appointment/webform', auth='public', type="http", website=True)
    def appointment_form(self, **kw):
        if request.env.user:
            current_user = request.env.user.name
            email = request.env.user.login
        else:
            current_user, email = "", ""
        return http.request.render('appointment_website.appointment_page_template', {'name': current_user, 'email': email})

    @http.route('/create/appointment', auth='public', type="http", website=True)
    def create_appointment(self, **kw):
        request.env['doctor.appointment'].sudo().create(kw)
        return request.render('appointment_website.appointment_thank_you_page_template', {})


class CustomerPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        DocApp = request.env['doctor.appointment'].search([])
        if 'appointment_count' in counters:
            values['appointment_count'] = len(DocApp)
        return values

    @http.route(['/my/appointments'], type='http', auth="user", website=True)
    def portal_my_appointments(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        # values = self._prepare_portal_layout_values()
        # partner = request.env.user.partner_id
        DocApp = request.env['doctor.appointment'].search([])
        print("\n\n\n")

        appointment_count = len(DocApp)
        print(appointment_count)
        # make pager
        pager = portal_pager(
            url="/my/appointment",
            # url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=appointment_count,
            page=page,
            # step=self._items_per_page
        )
        # search the count to display, according to the pager data
        appointments = DocApp
        request.session['my_appointments_history'] = appointments.ids[:100]
        values = {
            'date': date_begin,
            'appointments': appointments.sudo(),
            'page_name': 'appointment',
            'pager': pager,
            'default_url': '/my/appointment',
        }
        return request.render("appointment_website.portal_my_appointments", values)
