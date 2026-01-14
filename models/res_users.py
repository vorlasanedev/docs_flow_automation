from odoo import fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    docs_position = fields.Selection([
        ('employee', 'Employee'),
        ('head', 'Head of Department'),
        ('reception', 'Reception'),
    ], string='Duty / Position', help='Position/Duty for Document Automation')
