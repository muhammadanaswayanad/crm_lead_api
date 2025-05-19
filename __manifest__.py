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
    """,
    'category': 'CRM',
    'author': 'Your Company',
    'website': 'https://yourcompany.com',
    'depends': ['base', 'crm', 'utm'],
    'data': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
