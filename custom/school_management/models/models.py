# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Recruitment(models.Model):
    _name = "school.recruitment"
    _description = "Recruitment Model"

    name = fields.Char("Name")
    age = fields.Integer("Age")
    experience = fields.Integer("Experience")
    state = fields.Selection([("draft", "Draft"),
                              ("process", "Process"),
                              ("demo", "Need Demo"),
                              ("done", "Done")], default="draft", string="Teacher State")
    joining_date = fields.Date("Joining Date")

    doc_id = fields.One2many("school.document", "recruitment_id", string="Upload Documents")
    teacher_id = fields.One2many("school.teacher", "recruitment_id", string="Teacher")

    def action_process(self):
        for rec in self:
            rec.state = "process"

    def action_demo(self):
        for rec in self:
            rec.state = "demo"

    def action_done(self):
        for rec in self:
            rec.state = "done"


class Teacher(models.Model):
    _name = 'school.teacher'
    _description = 'Teacher Model'

    recruitment_id = fields.Many2one("school.recruitment", string="Teacher", domain=[("state", "=", "done")])
    student_id = fields.Many2many("school.student", string="Student", domain=[("state", "=", "done")])


class Student(models.Model):
    _name = 'school.student'
    _description = 'Student Model'

    name = fields.Char("Student Name")
    age = fields.Integer("Student Age")
    state = fields.Selection([("draft", "Draft"),
                              ("process", "Process"),
                              ("done", "Done")], default="draft", string="Student State")
    image = fields.Binary("Student Image")
    teacher_id = fields.Many2many("school.teacher")

    def action_process(self):
        for rec in self:
            rec.state = "process"

    def action_done(self):
        for rec in self:
            rec.state = "done"


class Document(models.Model):
    _name = "school.document"
    _description = "Document Model"

    name = fields.Char("Document Name")
    doc_date = fields.Date("Date")
    doc = fields.Binary("Document")
    recruitment_id = fields.Many2one("school.recruitment")
