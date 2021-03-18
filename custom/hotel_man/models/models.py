# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, exceptions
import datetime


class HotelRoom(models.Model):
    _name = 'hotel.room'
    _description = 'Hotel Room'
    _rec_name = "room_no"

    room_no = fields.Char("Room No.", readonly=True)
    room_type_id = fields.Many2one("hotel.room.type", string="Room Type")
    room_floor = fields.Selection([("1", "1"), ("2", "2"), ("3", "3")], string="Room Floor", default="1")
    room_size = fields.Integer("Room Size", default=2)
    room_state = fields.Selection([("draft", "Draft"), ("allocated", "Allocated")], string="Room State", default="draft")
    inquiry_ids = fields.Many2one("hotel.registration.inquiry", string="Inquiry")
    room_booked = fields.Boolean(string="Room Book")

    @api.model
    def create(self, vals):
        if vals.get('room_no', _('New')) == _('New'):
            vals['room_no'] = self.env['ir.sequence'].next_by_code('hotel.room.sequence') or _('New')
        res = super(HotelRoom, self).create(vals)
        return res

    @api.model
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s - %s' % (rec.room_no, rec.room_type_id.room_type)))
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


class RoomGuestLine(models.Model):
    _name = "hotel.room.guest.line"
    _description = "Hotel Room and Guests"

    reg_id = fields.Many2one("hotel.room.registration", string="Room No.")
    room_id = fields.Many2one("hotel.room", string="Room No.")
    guest_ids = fields.Many2many("res.partner", string="Guests")


class HotelRegistration(models.Model):
    _name = 'hotel.room.registration'
    _description = 'Hotel Room Registration'
    _rec_name = "reg_no"

    reg_no = fields.Char("Room Sequence", readonly=True, required=True, copy=False, default=lambda self: _('New'))
    customer_id = fields.Many2one("res.partner", string="Inquiry")
    mobile_no = fields.Char("Customer Phone No.")
    birthdate = fields.Date("Customer Birthdate")
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    document_id = fields.One2many("hotel.document", "reg_id", string="Customer Document")
    reg_state = fields.Selection([("draft", "Draft"), ("process", "Process"), ("done", "Done"), ("cancel", "Cancel")],
                                 string="Registration State", default="draft")
    guest_ids = fields.One2many("res.partner", "reg_id", string="Guest")
    room_guest_line_ids = fields.One2many("hotel.room.guest.line", "reg_id", string="Hotel Room No.")
    room_type_id = fields.Many2one("hotel.room.type", string="Room Type")

    # cron function
    def _reg_cancel(self):
        """
        Registration data that are in 'process' state are created before 3 days, should ne state='cancel' using cron
        Returns: state will change from 'process' to 'cancel'
        """
        previous_date = datetime.datetime.today() - datetime.timedelta(days=3)  # date before 3 days

        reg_id_to_cancelled = self.env["hotel.room.registration"].search([("reg_state", "=", "process"),
                                                                             ('create_date', '<=', previous_date)]) # find reg. ids that are created 3 days ago
        for reg in reg_id_to_cancelled:
            reg.reg_state = 'cancel'  # change state from 'process' to 'cancel'

    def action_process(self):
        for rec in self:
            rec.reg_state = "process"

    def action_done(self):
        for rec in self:
            rec.reg_state = "done"
            rec.room_guest_line_ids.room_id.room_state = 'allocated'

    @api.model
    def create(self, vals):
        if vals.get('reg_no', _('New')) == _('New'):
            vals['reg_no'] = self.env['ir.sequence'].next_by_code('hotel.room.reg') or _('New')

        val = {'room_state': 'allocated'}
        # room_to_allocate = []
        for room in vals["room_guest_line_ids"]:
            print(room[2].get("room_id"))
        print(vals["room_guest_line_ids"])
        # room_allocate = self.env['hotel.room'].search([('id', '=', vals["room_guest_line_ids"][0][2].get("room_id"))])  # first search record
        # for room in room_allocate:
        #     room.write(val)  # update record

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


class HotelRegInquiry(models.Model):
    _name = 'hotel.registration.inquiry'
    _description = "Inquiry Model"
    _rec_name = "customer_id"

    customer_id = fields.Many2one("res.partner", string="Inquiry")
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    room_type = fields.Many2one("hotel.room.type", string="Room Type")
    room_size = fields.Integer("Room Size")
    room_ids = fields.One2many("hotel.room", "inquiry_ids", string="Room No.", default=False)

    def search_room(self):
        print(self.room_type)
        filtered_rooms = self.env["hotel.room"].search([("room_state", "=", "draft"),
                                                        ("room_type_id", "=", self.room_type.id),
                                                        ("room_size", ">", self.room_size-1)])

        self.room_ids = [(6, 0, [])]
        self.write({'room_ids': filtered_rooms})
        return

    def submit_inquiry(self):
        selected_res = []
        for room in self.room_ids:
            for is_selected in room:
                if is_selected:
                    selected_res.append({"room_id": is_selected.id})

        return {
            'name': "Hotel Room Registration",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hotel.room.registration',
            'view_id': self.env.ref('hotel_man.hotel_room_registration_form').id,
            'context': {'process': 1,
                        'default_room_guest_line_ids': selected_res
                        }
        }

