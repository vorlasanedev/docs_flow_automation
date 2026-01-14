{
    'name': 'Document Flow Automation',
    'version': '18.0.1.0.0',
    'category': 'Productivity/Documents',
    'summary': 'Manage incoming and outgoing documents with tracking and automated notifications',
    'description': """
        Document Flow Automation
        ========================
        
        Comprehensive document management system with:
        
        * Track incoming and outgoing documents
        * Department-based access control
        * Document assignment workflow
        * Automated email notifications
        * Activity tracking and chatter integration
        * Folder organization by department
        
        Access Rights:
        --------------
        * Administrator: Full access to all documents and folders
        * Employee: View only their department's documents
        * Reception: View all documents, assign to departments/users, cannot delete
        * Head of Department: View all documents, cannot delete
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'hr',
    ],
    'data': [
        # Security
        'security/security.xml',
        'security/ir.model.access.csv',
        
        # Data
        'data/sequences.xml',
        'data/mail_templates.xml',
        
        # Views
        'views/docs_folder_views.xml',
        'views/docs_document_views.xml',
        'views/res_users_cleanup.xml',

        'views/menus.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
