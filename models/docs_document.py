from odoo import fields, models, api, _
from odoo.exceptions import UserError

class DocsDocument(models.Model):
    _name = 'docs.document'
    _description = 'Document'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    # Basic Information
    name = fields.Char(string='Reference', required=True, copy=False, default='New', tracking=True)
    subject = fields.Char(string='Subject', required=True, tracking=True)
    description = fields.Text(string='Description')
    attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Attachments'
    )

    # Document Type
    document_type = fields.Selection([
        ('incoming', 'Incoming'),
        ('outgoing', 'Outgoing')
    ], string='Type', required=True, default='incoming', tracking=True)

    # Department & Folder
    department_id = fields.Many2one(
        'hr.department',
        string='Department',
        required=True,
        tracking=True,
        help='Department this document belongs to'
    )
    folder_id = fields.Many2one(
        'docs.folder',
        string='Folder',
        tracking=True
    )

    # Assignment
    assigned_user_id = fields.Many2one(
        'res.users',
        string='Assigned To',
        tracking=True,
        help='User responsible for this document'
    )
    assigned_date = fields.Datetime(string='Assigned Date', readonly=True)

    # Tracking & Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('archived', 'Archived')
    ], string='Status', default='draft', required=True, tracking=True)

    received_date = fields.Date(string='Received Date', default=fields.Date.today, tracking=True)
    completed_date = fields.Date(string='Completed Date', readonly=True)

    # Contact Information for Notifications
    contact_email = fields.Char(string='Contact Email')
    contact_whatsapp = fields.Char(string='WhatsApp Number', help='Format: +856XXXXXXXXX')

    # Computed Fields
    is_assigned_to_me = fields.Boolean(
        string='Assigned to Me',
        compute='_compute_is_assigned_to_me',
        search='_search_is_assigned_to_me'
    )

    @api.depends('assigned_user_id')
    def _compute_is_assigned_to_me(self):
        for doc in self:
            doc.is_assigned_to_me = doc.assigned_user_id == self.env.user

    def _search_is_assigned_to_me(self, operator, value):
        if operator == '=' and value:
            return [('assigned_user_id', '=', self.env.user.id)]
        elif operator == '=' and not value:
            return [('assigned_user_id', '!=', self.env.user.id)]
        elif operator == '=' and not value:
            return [('assigned_user_id', '!=', self.env.user.id)]
        return []

    @api.onchange('assigned_user_id')
    def _onchange_assigned_user_id(self):
        if not self.assigned_user_id:
            return
            
        # Search for employee linked to the user (current company first)
        employee = self.env['hr.employee'].search([
            ('user_id', '=', self.assigned_user_id.id),
            ('company_id', '=', self.env.company.id)
        ], limit=1)
        
        # Fallback to any company
        if not employee:
            employee = self.env['hr.employee'].search([
                ('user_id', '=', self.assigned_user_id.id)
            ], limit=1)
            
        if employee and employee.department_id:
            self.department_id = employee.department_id

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('docs.document') or 'New'
        
        doc = super(DocsDocument, self).create(vals)
        
        # Notify Department Manager if department is set
        if doc.department_id:
            doc._notify_department_new_document(doc.department_id)
            
        return doc

    def _notify_department_new_document(self, department_id):
        """Notify department manager about new incoming document"""
        if not department_id.manager_id:
            return

        manager = department_id.manager_id
        self.activity_schedule(
            'mail.mail_activity_data_todo',
            user_id=manager.id,
            summary=_('New Document for Department: %s') % self.subject,
            note=_('A new document %s has been created for your department.') % self.name
        )

    def action_send_whatsapp(self):
        """Open WhatsApp Web to send notification"""
        self.ensure_one()
        if not self.contact_whatsapp:
            raise UserError(_("Please configure a WhatsApp number for this document."))
            
        # Basic cleaning of numbers (remove spaces, etc)
        phone = ''.join(filter(str.isdigit, self.contact_whatsapp))
        
        message = _("Hello, there is an update regarding document %s: %s. Current status: %s") % (self.name, self.subject, self.state)
        url = "https://web.whatsapp.com/send?phone=%s&text=%s" % (phone, message)
        
        # Log in chatter
        self.message_post(
            body=_('WhatsApp notification link generated for %s') % self.contact_whatsapp,
            subject=_('WhatsApp Notification'),
            message_type='notification'
        )
        
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }

    def action_assign(self):
        """Assign document to a user"""
        self.ensure_one()
        if not self.assigned_user_id:
            raise UserError(_('Please select a user to assign this document to.'))
        
        self.write({
            'assigned_date': fields.Datetime.now(),
            'state': 'in_progress'
        })

        # Create activity for assigned user
        self.activity_schedule(
            'mail.mail_activity_data_todo',
            user_id=self.assigned_user_id.id,
            summary=_('Document Assigned: %s') % self.subject,
            note=_('You have been assigned a new document: %s') % self.name
        )

        # Send email notification
        self._send_assignment_notification()

        # Post message in chatter
        self.message_post(
            body=_('Document assigned to %s') % self.assigned_user_id.name,
            subject=_('Document Assignment'),
            message_type='notification',
            subtype_xmlid='mail.mt_note'
        )

        return True

    def action_complete(self):
        """Mark document as completed"""
        self.write({
            'state': 'completed',
            'completed_date': fields.Date.today()
        })
        self.message_post(
            body=_('Document marked as completed'),
            subject=_('Document Completed'),
            message_type='notification'
        )

    def action_archive_document(self):
        """Archive the document"""
        self.write({'state': 'archived'})
        self.message_post(
            body=_('Document archived'),
            message_type='notification'
        )

    def action_reset_to_draft(self):
        """Reset document to draft"""
        self.write({'state': 'draft'})

    def _send_assignment_notification(self):
        """Send email notification when document is assigned"""
        template = self.env.ref('docs_flow_automation.email_template_document_assignment', raise_if_not_found=False)
        if template and self.assigned_user_id:
            template.send_mail(self.id, force_send=True)
