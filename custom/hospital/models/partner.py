from odoo import  fields, models


class Partnet(models.Model):
    _inherit = 'product.template'

    description = fields.Text("Description", default=False)

