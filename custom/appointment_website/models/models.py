# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class DoctorAppointment(models.Model):
    _name = 'doctor.appointment'
    _description = 'Doctor Appointment'

    name = fields.Char(string="Name")
    age = fields.Integer(string="Age", default=27)
    dob = fields.Date(string="DOB", default=datetime.today())
    email = fields.Char(string="Email", default="odoo@gmail.com")
    contact = fields.Char(string="Contact", default="9714987522")
    #
    # def _prepare_portal_layout_values(self):
    #     """Values for /my/* templates rendering.
    #
    #     Does not include the record counts.
    #     """
    #     # get customer sales rep
    #     sales_user = False
    #     partner = request.env.user.partner_id
    #     if partner.user_id and not partner.user_id._is_public():
    #         sales_user = partner.user_id
    #
    #     return {
    #         'sales_user': sales_user,
    #         'page_name': 'home',
    #     }