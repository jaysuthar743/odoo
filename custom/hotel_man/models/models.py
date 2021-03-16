# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, exceptions
import time

from odoo.osv import expression


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

    # @api.model
    # def name_get(self):
    #     res = []
    #     for rec in self:
    #         res.append((rec.id, '%s - %s' % (rec.room_no, rec.room_type_id.room_type)))
    #     return res

    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        context = self.env.context
        print("\n\n\n\n\n room")
        print(context)
        if args is None:
            args = []
        else:
            if context.get('room_type_id'):
                room_type_ids = self.env['hotel.room']._search(
                    [('room_type_id', "=", context.get('room_type_id'))], limit=limit, access_rights_uid=name_get_uid)
                domain = [('id', "in", room_type_ids), ("room_state", "=", "draft")]
            else:
                domain = []
            return self._search(domain, limit=limit, access_rights_uid=name_get_uid)
        return super(HotelRoom, self)._name_search(name, args=args, operator=operator, limit=limit,
                                                       name_get_uid=name_get_uid)


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
    customer_id = fields.Many2one("res.partner", string="Inquiry")
    mobile_no = fields.Char("Customer Phone No.")
    birthdate = fields.Date("Customer Birthdate")
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    document_id = fields.One2many("hotel.document", "reg_id", string="Customer Document")
    reg_state = fields.Selection([("draft", "Draft"), ("process", "Process"), ("done", "Done")],
                                 string="Registration State", default="draft")
    guest_id = fields.One2many("res.partner", "reg_id", string="Guest")
    room_no = fields.Many2many("hotel.room", string="Hotel Room No.", domain=[("room_state", "=", "draft")])
    room_type_id = fields.Many2one("hotel.room.type", string="Room Type")

    def action_process(self):
        for rec in self:
            rec.reg_state = "process"

    def action_done(self):
        for rec in self:
            rec.reg_state = "done"
            rec.room_no.room_state = 'draft'

    @api.model
    def create(self, vals):
        print(vals)
        context = self.env.context
        print("\n\n\n\n\n context")
        print(context)
        if context.get("process"):
            vals['reg_state'] = 'process'

            val = {'room_state': 'allocated'}
            room_allocate = self.env['hotel.room'].search([('id', '=', vals["room_no"])])  # first search record
            for room in room_allocate:
                room.write(val)  # update record

        if vals.get('reg_no', _('New')) == _('New'):
            vals['reg_no'] = self.env['ir.sequence'].next_by_code('hotel.room.reg') or _('New')
        res = super(HotelRegistration, self).create(vals)
        return res

    @api.model
    def default_get(self, fields_list):
        res = super(HotelRegistration, self).default_get(fields_list)
        print("\n\n\n\n")
        print("default")

        # print(self.env.context)
        room_book_ids = self.env.context.get("room_no") or False
        # for i in room_book_ids:
        #     self.room_no.write({
        #         'room_no': [(4, i)]
        #     })
        get_room_ids = self.env["hotel.room"].browse(room_book_ids)
        # print(get_room_ids)

        for i in room_book_ids:
            self.room_no.write([(4, i)])
        # self.room_no = [(6, 0, get_room_ids)]
        # self.write({
        #     'room_no': get_room_ids
        # })


        # res.update({
        #     'start_date': self.env.context.get("start_date") or False,
        #     'end_date': self.env.context.get("end_date") or False,
        # })
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
        # room_types = self.env["hotel.room.type"].search([])
        filtered_rooms = self.env["hotel.room"].search([("room_state", "=", "draft"),
                                                        ("room_type_id", "=", self.room_type.id),
                                                        ("room_size", ">", self.room_size-1)])
        print(filtered_rooms)

        # room_list = []
        # for rec in filtered_rooms:
        #     room_list.append([0, 0, {'room_no': rec.room_no}])
        # print("\n\n\n\n\n list")
        # print(room_list)

        self.room_ids = [(6, 0, [])]
        self.write({'room_ids': filtered_rooms})
        return

    def submit_inquiry(self):
        res = []
        for i in self:
            for j in i.room_ids:
                if j.room_booked == True:
                    res.append(j.id)

        print("\n\n\n\n Room booked")
        print(self.room_type)
        return {
            'name': "Hotel Room Registration",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hotel.room.registration',
            'view_id': self.env.ref('hotel_man.hotel_room_registration_form').id,
            'context': {'process': 1,
                        'room_no': res}
        }


    # def search_available_room(self):
    #     inquiry_room_domain = self.env["hotel.room"].search([("room_type_id", "=", self.room_type.id), ("room_size", ">",self.room_size-1)])
    #     inquiry_reg_domain = self.env["hotel.room.registration"].search([('start_date', '<=', self.start_date),
    #                                                                      ('end_date', '>=', self.end_date)])
    #     print("\n\n\n\n\n\n\n\n search_available_room")
    #     print(self.env.context)
    #     if inquiry_room_domain:
    #         return {
    #             'name': "Hotel Room Registration",
    #             'type': 'ir.actions.act_window',
    #             'view_type': 'form',
    #             'view_mode': 'form',
    #             'res_model': 'hotel.room.registration',
    #             'view_id': self.env.ref('hotel_man.hotel_room_registration_form').id,
    #             'target': 'new',
    #             'context': {'process': 1,
    #                         'room_size': self.env.context.get("room_size"),
    #                         'start_date': self.start_date,
    #                         'end_date': self.end_date,
    #                         'room_type_id:': self.room_type
    #                         }
    #         }
    #     else:
    #         raise exceptions.ValidationError(_('Sorry! No Room Available.'))
    #
