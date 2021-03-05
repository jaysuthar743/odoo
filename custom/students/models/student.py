from odoo import api, fields, models, _, exceptions
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


class Student(models.Model):
	_name = 'student'
	_inherit = ['mail.thread','mail.activity.mixin']
	_description = 'Basic Student Model'

	@api.depends('dob')
	def compute_age(self):
		for rec in self:
			age = relativedelta(datetime.now().date(), fields.Datetime.from_string(rec.dob)).years
			rec.age = age

	@api.depends('age')
	def set_age_group(self):
		for rec in self:
			if rec.age:
				if rec.age < 18:
					rec.age_group = 'minor'
				else:
					rec.age_group = 'major'
			else:
				rec.age_group = 'unable'

	@api.constrains('age')
	def validate_age(self):
		for rec in self:
			if rec.age and rec.age < 18:
				raise exceptions.ValidationError(_('Age must be greater than 18'))

	name = fields.Char(string='Name', required=True, help='Student Name')
	code = fields.Integer(string='Student Code', required=True, help='Student Code')
	gender = fields.Selection([('male', 'Male'), ('female', 'Female')], default='male',  string='Gender', required=True, help='Student Gender')
	dob = fields.Date(string="Date of Birth", help='Student Date of Birth')
	age_group  = fields.Selection([
		('major','Major'),
		('unable','unable'),
	], string='Age Group', compute='set_age_group', store=True, help='Student Age Group')
	age = fields.Integer(compute='compute_age', store=True, help='Student Age')
	address = fields.Text(help='Student Address')
	image = fields.Image(string='Image', help='Student Image')

	street = fields.Char(string='Street')
	street2 = fields.Char(string='Street2')
	zip = fields.Char(string='Zip', change_default=True)
	city = fields.Char(string='City')
	state = fields.Char(string='State')
	country = fields.Char(string='Country')




