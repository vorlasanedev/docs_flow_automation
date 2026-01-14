from odoo import fields, models

class DocsOrigin(models.Model):
    _name = 'docs.origin'
    _description = 'Document Origin'
    _order = 'name asc'

    name = fields.Char(string='Origin Name', required=True, translate=True)
    description = fields.Text(string='Description')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The origin name must be unique!')
    ]
