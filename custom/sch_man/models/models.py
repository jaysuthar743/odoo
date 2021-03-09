# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Teacher(models.Model):
    _name = "school.teacher"
    _description = "Teacher Model"

    name = fields.Char("Name", required=True)
    age = fields.Integer("Age", required=True)
    phone = fields.Char("Phone Number", required=True)
    email = fields.Char("Email", required=True)
    experience = fields.Integer("Experience", required=True)
    address = fields.Text("Address", required=True)
    state = fields.Selection([("draft", "Draft"),
                              ("process", "Process"),
                              ("demo", "Demo"),
                              ("done", "Done")], default="draft", string="Teacher State")
    joining_date = fields.Date("Joining Date")
    need_demo = fields.Boolean("Need Demo")
    doc_id = fields.One2many("school.document", "teacher_id", string="Upload Documents")
    student_ids = fields.One2many("school.student", 'teacher_id', string="Student")

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

    name = fields.Char("Name", required=True)
    age = fields.Integer("Age", required=True)
    gender = fields.Selection([("male", "Male"),
                               ("female", "Female")], default='male', required=True, string="Gender")

    state = fields.Selection([("draft", "Draft"),
                              ("process", "Process"),
                              ("done", "Done")], default="draft", string="State")
    address = fields.Text("Address", required=True)
    image = fields.Binary("Student Image", required=True)
    teacher_id = fields.Many2one("school.teacher", domain=[("state", "=", "done")], string='Teacher')
    standard_id = fields.Many2one("school.standard")

    def action_process(self):
        for rec in self:
            rec.state = "process"

    def action_done(self):
        for rec in self:
            rec.state = "done"

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        print("\n\n\n\n\n\n \n\n\n----------------------------------------", args)
        if name:
            domain = ['|', ('name', operator, name), ('teacher_id', operator, name)]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)


class Standard(models.Model):
    _name = 'school.standard'
    _description = 'Standard Model'

    teacher_id = fields.Many2many("school.teacher")
    std = fields.Integer("Standard", required=True)


class Document(models.Model):
    _name = "school.document"
    _description = "Document Model"

    name = fields.Char("Document Name")
    doc_date = fields.Date("Date")
    doc = fields.Binary("Document")
    teacher_id = fields.Many2one("school.teacher")
