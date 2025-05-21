{
    'name': 'CRM Lead API',
    'version': '1.0',
    'summary': 'REST API endpoint to create leads from external software',
    'description': """
        This module exposes a REST API endpoint to create leads from external software.
        - Endpoint: /api/create_lead
        - Method: POST
        - Authentication: Public
        - Required fields: type, contact_name, phone, email, source
        - Optional fields: preferred_course, preferred_branch
        
        For testing:
        - Debug endpoint: /api/debug
        - Form endpoint: /api/create_lead/form (for form-encoded data)
    """,
    'category': 'CRM',
    'author': 'Your Company',
    'website': 'https://yourcompany.com',
    'depends': ['base', 'crm', 'utm'],
    'data': [
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
