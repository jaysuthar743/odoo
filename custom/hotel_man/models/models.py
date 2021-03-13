# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, exceptions
import time


class HotelRoom(models.Model):
    _name = 'hotel.room'
    _description = 'Hotel Room'
    _rec_name = "room_no"

    room_no = fields.Char("Room No.", readonly=True, required=True, copy=False, default=lambda self: _('New'))
    room_type_id = fields.Many2one("hotel.room.type", string="Room Type")
    room_floor = fields.Selection([("1", "1"), ("2", "2"), ("3", "3")], string="Room Floor", default="1")
    room_size = fields.Integer("Room Size", default=2)
    room_state = fields.Selection([("draft", "Draft"), ("allocated", "Allocated")], string="Room State", default="draft")

    @api.model
    def create(self, vals):
        context = self.env.context
        print("\n\n\n->>")
        print(context)
        if context.get("process"):
            vals['room_state'] = 'allocated'

        if vals.get('room_no', _('New')) == _('New'):
            vals['room_no'] = self.env['ir.sequence'].next_by_code('hotel.room.sequence') or _('New')
        res = super(HotelRoom, self).create(vals)
        return res


class HotelRoomType(models.Model):
    _name = 'hotel.room.type'
    _description = 'Hotel Room Type'
    _rec_name = "room_type"

    room_type = fields.Char("Room Type.")


class HotelGuest(models.Model):
    _inherit = "res.partner"
    _rec_name = "reg_id"

    reg_id = fields.Many2one("hotel.room.registration", "Registration")


class HotelRegistration(models.Model):
    _name = 'hotel.room.registration'
    _description = 'Hotel Room Registration'
    _rec_name = "reg_no"

    reg_no = fields.Char("Room Sequence", readonly=True, required=True, copy=False, default=lambda self: _('New'))
    customer_name = fields.Char("Customer Name", required=True)
    mobile_no = fields.Char("Customer Phone No.")
    birthdate = fields.Date("Customer Birthdate")
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    document_id = fields.One2many("hotel.document", "reg_id", string="Customer Document")
    reg_state = fields.Selection([("draft", "Draft"), ("process", "Process"), ("done", "Done")],
                                 string="Registration State", default="draft")
    guest_id = fields.One2many("res.partner", "reg_id", string="Guest")

    def action_process(self):
        for rec in self:
            rec.reg_state = "process"

    def action_done(self):
        for rec in self:
            rec.reg_state = "done"

    @api.model
    def create(self, vals):
        context = self.env.context
        if context.get("process"):
            vals['reg_state'] = 'process'

        if vals.get('reg_no', _('New')) == _('New'):
            vals['reg_no'] = self.env['ir.sequence'].next_by_code('hotel.room.reg') or _('New')
        res = super(HotelRegistration, self).create(vals)
        return res


class HotelDocument(models.Model):
    _name = 'hotel.document'
    _description = 'Hotel Document'
    _rec_name = "name"

    name = fields.Char("Document Name", required=True)
    doc_date = fields.Date("Date")
    doc = fields.Binary("Document")
    reg_id = fields.Many2one("hotel.room.registration")


class HotelRegInquiry(models.TransientModel):
    _name = 'hotel.registration.inquiry.wizard'
    _description = "Inquiry Model"
    _rec_name = "customer_id"

    customer_id = fields.Many2one("res.partner", string="Inquiry")
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    room_type = fields.Many2one("hotel.room.type", string="Room Type")
    room_size = fields.Integer("Room Size")

    def search_available_room(self):
        inquiry_room_domain = self.env["hotel.room"].search([("room_type_id", "=", self.room_type.id), ("room_size", ">", self.room_size-1)])
        inquiry_reg_domain = self.env["hotel.room.registration"].search([('start_date', '<=', self.start_date),
                                                                         ('end_date', '>=', self.end_date)])
        print("\n\n\n\n\n\n\n\n search_available_room")
        print(len(inquiry_room_domain))
        print(len(inquiry_reg_domain))
        if inquiry_room_domain:
            return {
                'name': "Hotel Room Registration",
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'hotel.room',
                'view_id': self.env.ref('hotel_man.hotel_room_book').id,
                'target': 'new',
                # 'domain':  [("room_type_id", "=", self.room_type.id), ("room_size", ">", self.room_size-1),
                #             ("room_state", "=", "draft")],
                'context': {'process': 1},
            }
        else:
            raise exceptions.ValidationError(_('Sorry! No Room Available.'))


class RoomBooked(models.Model):
    _name = "hotel.room.booked"
    _description = "Hotel Room Booked"

    hotel_room_ids = fields.Many2many("hotel.room", string="Hotel Room")

    def room_book(self):
        print("\n\n\n->>>>>>>>>>>>>>>>>>>Booked")
        pass

