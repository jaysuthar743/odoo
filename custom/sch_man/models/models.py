# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, exceptions
from odoo.osv import expression


class Teacher(models.Model):
    _name = "school.teacher"
    _description = "Teacher Model"

    seq_teacher = fields.Char(string='Teacher Code', readonly=True, required=True, index=True, copy=False,
                              default=lambda self: _('New'))
    name = fields.Char("Name", required=True)
    age = fields.Integer("Age", required=True, default=25)
    phone = fields.Char("Phone Number", required=True, default='9875526888')
    email = fields.Char("Email", required=True, default='j@gmail.com')
    experience = fields.Integer("Experience", required=True, default=3)
    address = fields.Text("Address", required=True, default='xyz')
    state = fields.Selection([("draft", "Draft"),
                              ("process", "Process"),
                              ("demo", "Demo"),
                              ("done", "Done")], default="draft", string="Teacher State")
    joining_date = fields.Date("Joining Date")
    need_demo = fields.Boolean("Need Demo")
    doc_id = fields.One2many("school.document", "teacher_id", string="Upload Documents")
    student_ids = fields.One2many("school.student", 'teacher_id', string="Student")
    standard_ids = fields.Many2many("school.standard", string="Standard")

    @api.model
    def create(self, vals):
        if vals.get('seq_teacher', _('New')) == _('New'):
            vals['seq_teacher'] = self.env['ir.sequence'].next_by_code('school.teacher.sequence') or _('New')
        res = super(Teacher, self).create(vals)
        return res

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        context = self.env.context
        if args is None:
            args = []
        else:
            if context.get('std'):
                std_ids = self.env['school.standard']._search([('id', operator, context.get('std'))], limit=limit, access_rights_uid=name_get_uid)
                print(std_ids)
                domain = [('standard_ids', "=", std_ids)]
            else:
                domain = []
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

    def search_demo(self):
        print("\n\n\n\n\n\n\n\n\n\n***************")
        print("ids: ", self.ids)
        print(self.search_count([('state', '=', 'done')]))
        print(self.search([('state', '=', 'done')]))
        print(self.browse([(8, 12)]))
        print(self.ensure_one())
        print(self.copy())
        print(self.env)
        print("default get:", self.default_get(['state']))
        print("write:", self.write({'name': 'jai'}))
        print("read group:", self.read_group([], ['state', 'name'], ['joining_date']))
        print("fields get:", self.fields_get(['name']))
        print("fields view get:", self.fields_get(['school_teacher_tree']))
        # print("unlink:", self.unlink())
        print("name get:", self.name_get())
        print("get meta data:", self.get_metadata())

        if self.exists():
            print("Record Exists")

    def action_process(self):
        for rec in self:
            rec.state = "process"

    def action_demo(self):
        for rec in self:
            rec.state = "demo"

    def action_done(self):
        for rec in self:
            rec.state = "done"


class Student(models.Model):
    _name = 'school.student'
    _description = 'Student Model'

    seq_student = fields.Char("Student Code", readonly=True, required=True, copy=False, default=lambda self: _('New'))
    name = fields.Char("Name", required=True)
    age = fields.Integer("Age", required=True, default=18)
    gender = fields.Selection([("male", "Male"),
                               ("female", "Female")], default='male', required=True, string="Gender")

    state = fields.Selection([("draft", "Draft"),
                              ("process", "Process"),
                              ("done", "Done")], default="draft", string="State")
    address = fields.Text("Address", required=True, default='xyz')
    image = fields.Binary("Student Image", required=True)
    teacher_id = fields.Many2one("school.teacher", domain=[("state", "=", "done")], string='Teacher')
    standard_id = fields.Many2one("school.standard")

    @api.onchange('standard_id')
    def reset_teacher(self):
        self.teacher_id = None

    @api.model
    def create(self, vals):
        print("\n\n\n\n\n\n\n\n", vals)
        if vals.get('seq_student', _('New')) == _('New'):
            vals['seq_student'] = self.env['ir.sequence'].next_by_code('school.student.sequence') or _('New')
        res = super(Student, self).create(vals)
        return res

    @api.model
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s - %s' % (rec.name, rec.seq_student)))
        return res

    def action_process(self):
        for rec in self:
            rec.state = "process"

    def action_done(self):
        for rec in self:
            rec.state = "done"


class Standard(models.Model):
    _name = 'school.standard'
    _description = 'Standard Model'
    _rec_name = 'std'

    @api.model
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, 'Standard - %s' % (rec.std)))
        return res

    std = fields.Selection([('1', '1'),
                            ('2', '2'),
                            ('3', '3'),
                            ('4', '4'),
                            ('5', '5'),
                            ('6', '6'),
                            ('7', '7'),
                            ('8', '8'),
                            ('9', '9'),
                            ('10', '10')], "Standard", required=True)


class Document(models.Model):
    _name = "school.document"
    _description = "Document Model"

    name = fields.Char("Document Name")
    doc_date = fields.Date("Date")
    doc = fields.Binary("Document")
    teacher_id = fields.Many2one("school.teacher")


class StudentWizard(models.TransientModel):
    _name = 'school.student.wizard'

    def _get_default_students(self):
        return self.env['school.student'].browse(self.env.context.get("active_ids"))

    student_ids = fields.Many2many("school.student", String="Students")
    level = fields.Char("Level", required=True)

    def set_student_level(self):
        for rec in self:
            if rec.student_ids:
                rec.level = self.level


