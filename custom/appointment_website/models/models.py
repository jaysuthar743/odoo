# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class DoctorAppointment(models.Model):
    _name = 'doctor.appointment'
    _description = 'Doctor Appointment'
    _rec_name = 'name'

    name = fields.Char(string="Name")
    age = fields.Integer(string="Age", default=27)
    dob = fields.Date(string="DOB", default=datetime.today())
    email = fields.Char(string="Email", default="odoo@gmail.com")
    contact = fields.Char(string="Contact", default="9714987522")


