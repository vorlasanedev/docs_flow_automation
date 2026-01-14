# Document Flow Automation

Odoo 18 module for managing incoming and outgoing documents with department-based access control, assignment workflows, and automated notifications.

## Features

### Document Management
- Track incoming and outgoing documents
- Auto-generated document reference numbers (DOC/00001)
- Document status workflow: Draft → In Progress → Completed → Archived
- File attachments support
- Activity tracking and chatter integration

### Access Control
- **Administrator**: Full access to all documents and folders
- **Employee**: View only their department's documents
- **Reception**: View all documents, assign to users, cannot delete
- **Head of Department**: View all documents, cannot delete

### Assignment Workflow
- Assign documents to specific users
- Automatic activity creation for assigned users
- Email notifications on assignment
- Track assignment dates

### Organization
- Department-based folders
- Filter documents by type, department, status
- Kanban view grouped by status
- My Documents view for assigned items

### Notifications
- Email notifications on document assignment
- Email templates for status changes
- Contact information fields (email, WhatsApp)
- Integration-ready for WhatsApp API

## Installation

1. Copy this module to your Odoo addons directory
2. Update the apps list: `Settings → Apps → Update Apps List`
3. Search for "Document Flow Automation"
4. Click Install

## Usage

### For Reception
1. Go to `Docs Automation → Incoming Documents`
2. Create new document with department and details
3. Assign to specific user
4. User receives email notification and activity

### For Employees
1. Go to `Docs Automation → My Documents`
2. View documents assigned to you
3. Mark as completed when done

### For Administrators
1. Manage folders in `Configuration → Folders`
2. Create department-specific folders
3. Full access to all documents

## Configuration

### Assign User Positions

The easiest way to assign roles is using the Document Position field:

1. Go to `Settings → Users & Companies → Users`
2. Edit a user
3. Go to the `Access Rights` tab
4. Under "Document Automation" section, select the **Document Position**:
   - **Employee**: View only their department's documents
   - **Head of Department**: View all documents, cannot delete
   - **Reception**: View all documents, assign to users, cannot delete

The security groups will be automatically updated based on the selected position.

### Alternative: Manual Group Assignment
You can also manually assign users to security groups in the same Access Rights tab:
- Document Automation / Employee
- Document Automation / Reception
- Document Automation / Head of Department

### Email Templates
Customize email templates in `Settings → Technical → Email Templates`:
- Document Assignment Notification
- Document Status Change Notification

## Technical Details

### Models
- `docs.document`: Main document model with tracking
- `docs.folder`: Folder organization by department

### Dependencies
- base
- mail
- hr

## Support

For issues or questions, contact your system administrator.
