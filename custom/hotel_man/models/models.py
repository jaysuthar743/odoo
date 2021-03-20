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
    room_state = fields.Selection([("draft", "Draft"), ("allocated", "Allocated")], string="Room State",
                                  default="draft")
    inquiry_ids = fields.Many2one("hotel.registration.inquiry", string="Inquiry")
    room_booked = fields.Boolean(string="Room Book")
    room_price = fields.Integer("Room Price")

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
    room_price = fields.Integer(related='room_id.room_price')


class HotelRegistration(models.Model):
    _name = 'hotel.room.registration'
    _description = 'Hotel Room Registration'
    _rec_name = "reg_no"

    reg_no = fields.Char("Room Sequence", readonly=True, required=True, copy=False, default=lambda self: _('New'))
    customer_id = fields.Many2one("res.partner", string="Inquiry")
    mobile_no = fields.Char("Customer Phone No.")
    birthdate = fields.Date("Customer Birthdate")
    start_date = fields.Date("Start Date", default=datetime.datetime.today())
    end_date = fields.Date("End Date")
    document_id = fields.One2many("hotel.document", "reg_id", string="Customer Document")
    reg_state = fields.Selection([("draft", "Draft"), ("process", "Process"), ("done", "Done"), ("cancel", "Cancel"),
                                  ("send_mail", "Send Email")],
                                 string="Registration State", default="draft")
    guest_ids = fields.One2many("res.partner", "reg_id", string="Guest")
    room_guest_line_ids = fields.One2many("hotel.room.guest.line", "reg_id", string="Hotel Room No.")
    room_type_id = fields.Many2one("hotel.room.type", string="Room Type")
    total_price = fields.Integer("Total Amount to Pay", readonly=True)

    @api.model
    def get_email_to(self):
        print("\n\n\n\n\n called")
        recipients = list(r['email'] for r in self.room_guest_line_ids.guest_ids)
        # recipients = "jay@gmail.com, "vijay@gmail.com"]
        print(recipients)
        return ",".join(recipients)

    def send_mail(self):
        ''' Opens a wizard to compose an email, with relevant mail template loaded by default '''

        # #send email to current guest
        # mail_template = self.env.ref('hotel_man.reg_email_template')
        # mail_template.send_mail(self.id, force_send=True)

        self.ensure_one()
        ir_model_data = self.env['ir.model.data']

        try:
            template_id = self.env['ir.model.data'].xmlid_to_res_id('hotel_man.reg_email_template',
                                                                    raise_if_not_found=False)
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False

        recipients = list(r['email'] for r in self.room_guest_line_ids.guest_ids)
        print(recipients)
        print("\n\n\n\n reccc")
        # for guest in self.room_guest_line_ids.guest_ids:
        #     recipients.add(guest.email)

        # print(recipients)
        # print(self.ids)
        ctx = {
            'default_model': 'hotel.room.registration',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            # 'default_partner_ids': list(recipients),
            # 'email': list(recipients),
            # 'default_email_to': ','.join(recipients),
            'default_email_to': 'jay@gmail.com',
            'default_composition_mode': 'comment',
        }
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    # cron function
    def _reg_cancel(self):
        """ Registration data that are in 'process' state are created before 3 days, should be state='cancel' using cron
        Returns: state will change from 'process' to 'cancel' """

        previous_date = datetime.datetime.today() - datetime.timedelta(days=3)  # date before 3 days

        reg_ids_to_cancel = self.env["hotel.room.registration"].search([("reg_state", "=", "process"),
                                                                        ('create_date', '<=',
                                                                         previous_date)])  # find reg. ids that are created 3 days ago
        for reg in reg_ids_to_cancel:
            reg.reg_state = 'cancel'  # change state from 'process' to 'cancel'

    # cron function
    def _room_draft(self):
        """
        cron function to change room state from 'allocated' to 'draft' when registration's end date is matched
        Returns
        -------

        """
        room_ids_to_draft = self.env["hotel.room.registration"].search(
            [('end_date', '=', ((datetime.date.today()).strftime('%Y-%m-%d')))])
        for room in room_ids_to_draft:
            room.room_guest_line_ids.room_id.room_state = 'draft'

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
    total_price = fields.Integer("Total Amount to Pay", readonly=True, compute="calculate_price")

    @api.onchange("room_ids")
    def calculate_price(self):
        total = 0
        for price in self.room_ids:
            if price.room_booked:
                total += price.room_price
        self.write({
            'total_price': total
        })

    def search_room(self):
        self.calculate_price()
        filtered_rooms = self.env["hotel.room"].search([("room_state", "=", "draft"),
                                                        ("room_type_id", "=", self.room_type.id),
                                                        ("room_size", ">", self.room_size - 1)])

        self.room_ids = [(6, 0, [])]
        self.write({'room_ids': filtered_rooms})
        return

    def submit_inquiry(self):
        """ """
        selected_res = []  # list of ids that are selected.
        for room in self.room_ids:
            for is_selected in room:
                if is_selected.room_booked:
                    selected_res.append({"room_id": is_selected.id})

        return {
            'name': "Hotel Room Registration",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hotel.room.registration',
            'view_id': self.env.ref('hotel_man.hotel_room_registration_form').id,
            'context': {'default_room_guest_line_ids': selected_res}
        }


class ReportHotelManPrintReg(models.AbstractModel):
    _name = "report.hotel_man.print_reg"
    _description = "model for Abstract Class"

    def _get_name(self, doc):
        return "jay"

    @api.model
    def _get_report_values(self, docids, data=None):
        doc = self.env['hotel.room.registration'].browse(docids)
        return {
            'doc_ids': doc.ids,
            'doc_model': 'hotel.room.registration',
            'docs': doc,
            'get_name': self._get_name
        }
