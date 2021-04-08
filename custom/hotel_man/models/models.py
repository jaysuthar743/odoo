# -*- coding: utf-8 -*-

import base64
import datetime
import io
import time

import xlrd

from odoo import models, fields, api, _

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


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
    reg_count = fields.Integer(string="Registration Count", compute='count_registrations')

    def count_registrations(self):
        self.reg_count = self.env['hotel.room.registration'].search_count(
            [('room_guest_line_ids.room_id', '=', self.id)])

    def get_registrations(self):
        """
            Open Registrations Tree view if there is more than 1 room allocated to that reg.,
            Otherwise open form view of particular reg. form
        """
        self.ensure_one()
        reg_ids = self.env["hotel.room.registration"].search([('room_guest_line_ids.room_id', '=', self.id)])
        action = self.env["ir.actions.actions"]._for_xml_id("hotel_man.hotel_room_registration_action")
        if self.reg_count > 1:
            action['domain'] = [('room_guest_line_ids.room_id', '=', self.id)]
        elif self.reg_count == 1:
            form_view = [(self.env.ref('hotel_man.hotel_room_registration_form').id, 'form')]
            action['views'] = form_view
            action['res_id'] = reg_ids.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

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

    room_type = fields.Char("Room Type.", required=True)


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
        recipients = list(r['email'] for r in self.room_guest_line_ids.guest_ids)
        # recipients = "jay@gmail.com, "vijay@gmail.com"]
        return ",".join(recipients)

    def send_mail(self):
        '''  outgoing mail server configured to send mail '''

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

        # recipients = list(r['email'] for r in self.room_guest_line_ids.guest_ids)
        # print(recipients)

        ctx = {
            'default_model': 'hotel.room.registration',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
        }
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
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
                                                                         previous_date)])  # find reg. ids that are created 3 days ago and state is process
        for reg in reg_ids_to_cancel:
            reg.reg_state = 'cancel'  # change state from 'process' to 'cancel'

    # cron function
    def _room_draft(self):
        """
        cron function to change room state from 'allocated' to 'draft' when registration's end date is matched
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

    @staticmethod
    def _get_name(doc):
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


class ReportHotelManPrintRegExcel(models.TransientModel):
    _name = "hotel.room.registration.xlsx"
    _description = "Model for excel report"

    start_date = fields.Date(string="Start Date", default=time.strftime('%Y-%m-01'), required=True)
    end_date = fields.Date(string="End Date", default=datetime.datetime.now(), required=True)

    def generate_excel_report(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        format0 = workbook.add_format({'font_size': 14, 'align': 'center', 'bold': True})
        format1 = workbook.add_format({'font_size': 12, 'align': 'center'})
        sheet = workbook.add_worksheet('Customer Registration Details')
        sheet.write('A1', 'Registration Id', format0)
        sheet.write('B1', 'Start Date', format0)
        sheet.write('C1', 'End Date', format0)
        sheet.write('D1', 'Room No.', format0)
        sheet.write('E1', 'Guests', format0)
        sheet.write('F1', 'Bill Amount', format0)
        sheet.write('G1', 'Room Type', format0)
        sheet.set_column('A:D', 30)
        sheet.set_column('E:E', 50)
        sheet.set_column('F:G', 30)
        res = self.env["hotel.room.registration"].search([("start_date", ">=", self.start_date),
                                                          ("start_date", "<=", self.end_date)])
        data = []
        for record in res:
            rooms, guests, room_type = [], [], []
            for room in record.room_guest_line_ids.room_id:
                rooms.append(room.room_no)

            for guest in record.room_guest_line_ids.guest_ids:
                guests.append(guest.name)

            for rt in record.room_guest_line_ids.room_id:
                room_type.append(rt.room_type_id.room_type)

            vals = {
                'start_date': record.start_date,
                'end_date': record.end_date,
                'reg_no': record.reg_no,
                'room_no': rooms,
                'guests': guests,
                'total': record.total_price,
                'room_type': room_type
            }
            data.append(vals)
        row = 2
        col = 0
        for rec in data:
            sheet.write(row, col, rec.get('reg_no'), format1)
            sheet.write(row, col + 1, rec.get('start_date').strftime('%d/%m/%Y'), format1)
            sheet.write(row, col + 2, rec.get('end_date').strftime('%d/%m/%Y'), format1)
            sheet.write(row, col + 3, ", ".join(rec.get("room_no")), format1)
            sheet.write(row, col + 4, ", ".join(rec.get("guests")), format1)
            sheet.write(row, col + 5, rec.get("total"), format1)
            sheet.write(row, col + 6, ", ".join(rec.get("room_type")), format1)
            row += 1
        if data:
            sheet.write(row + 1, col + 5, '{=SUM(F3:F' + str(row) + ')}', format0)
        workbook.close()
        output.seek(0)
        attach = self.env['ir.attachment'].create({'name': 'Hotel_Registrations.xlsx',
                                                   'datas': base64.b64encode(output.read())})
        return {
            'type': 'ir.actions.act_url',
            'url': str(self.env['ir.config_parameter'].get_param('web.base.url')) + str(
                '/web/content/' + str(attach.id) + '?download=True'),
            'target': self
        }


class RoomImport(models.TransientModel):
    _name = "hotel.room.import"
    _description = "Model to Import Room From Excel File"

    room_details_file = fields.Binary(string="Upload Excel File")

    def create_room(self):
        wb = xlrd.open_workbook(file_contents=base64.decodebytes(self.room_details_file))  # Uploaded File
        for sheet in wb.sheets():
            for row in range(1, sheet.nrows):
                room_type_id = sheet.cell(row, 0).value
                room_floor = sheet.cell(row, 1).value
                room_size = sheet.cell(row, 2).value
                room_state = sheet.cell(row, 3).value
                room_price = sheet.cell(row, 4).value

                self.env['hotel.room'].create({
                    'room_no': 'New',
                    'room_type_id': int(room_type_id),
                    'room_floor': str(int(room_floor)),
                    'room_size': int(room_size),
                    'room_state': str(room_state),
                    'room_price': int(room_price)
                })

        return {
            'name': 'Message',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'custom.pop.message',
            'target': 'new',
            'view_id': self.env.ref('hotel_man.custom_pop_message_wizard_view_form').id,
            'context': {'default_name': "Successfully Inserted."}
        }


class CustomPopMessage(models.TransientModel):
    _name = "custom.pop.message"

    name = fields.Char(string='Message')


class ProductUploadWizard(models.TransientModel):
    _name = "product.upload.wizard"

    product_import_file = fields.Binary(string="Upload Excel File")

    def create_products(self):
        wb = xlrd.open_workbook(file_contents=base64.decodebytes(self.product_import_file))  # Uploaded File
        order_id = self.env.context.get("sale_id")
        for sheet in wb.sheets():
            for row in range(1, sheet.nrows):
                product_name = sheet.cell(row, 0).value
                product_description = sheet.cell(row, 1).value
                existing_product = self.env["product.product"].search([("name", "=", product_name)], limit=1)
                if len(existing_product.ids) >= 1:
                    prods = existing_product.id
                else:
                    prods = self.env['product.product'].create({
                        'name': str(product_name),
                        'description': str(product_description)
                    }).id
                self.env['sale.order.line'].create({'order_id': order_id,
                                                    'product_id': prods,
                                                    'name': str(product_description),
                                                    'product_uom': 1})


class SalesOrderImportProduct(models.AbstractModel):
    _inherit = "sale.order"

    def invoke_product_wizard(self):
        return {
            'name': 'Message',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'product.upload.wizard',
            'target': 'new',
            'view_id': self.env.ref('hotel_man.product_upload_wizard_view_form').id,
            'context': {'sale_id': self.id}
        }
