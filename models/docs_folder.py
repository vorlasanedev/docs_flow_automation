from odoo import fields, models, api

class DocsFolder(models.Model):
    _name = 'docs.folder'
    _description = 'Document Folder'
    _order = 'name'

    name = fields.Char(string='Folder Name', required=True)
    department_id = fields.Many2one(
        'hr.department',
        string='Department',
        help='Department this folder belongs to'
    )
    document_count = fields.Integer(
        string='Documents',
        compute='_compute_document_count'
    )

    @api.depends('department_id')
    def _compute_document_count(self):
        for folder in self:
            folder.document_count = self.env['docs.document'].search_count([
                ('folder_id', '=', folder.id)
            ])

    def action_view_documents(self):
        """Open documents in this folder"""
        self.ensure_one()
        return {
            'name': f'{self.name} - Documents',
            'type': 'ir.actions.act_window',
            'res_model': 'docs.document',
            'view_mode': 'list,form,kanban',
            'domain': [('folder_id', '=', self.id)],
            'context': {'default_folder_id': self.id}
        }
