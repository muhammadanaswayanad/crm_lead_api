from odoo import http
from odoo.http import request
import logging
import json

_logger = logging.getLogger(__name__)

class CRMLeadAPIController(http.Controller):
    
    @http.route('/api/create_lead', type='json', auth='public', methods=['POST'], csrf=False)
    def create_lead(self, **post):
        """Create a new lead from API request"""
        try:
            # Get the JSON data
            data = request.jsonrequest
            
            # Validate required fields
            required_fields = ['type', 'contact_name', 'phone', 'email', 'source']
            missing_fields = [field for field in required_fields if not data.get(field)]
            
            if missing_fields:
                return {
                    'status': 'error', 
                    'message': f"Missing fields: {', '.join(missing_fields)}"
                }
            
            # Extract values
            lead_type = data.get('type', 'lead')
            contact_name = data.get('contact_name')
            phone = data.get('phone')
            email = data.get('email')
            source_name = data.get('source')
            preferred_course = data.get('preferred_course', False)
            preferred_branch = data.get('preferred_branch', False)
            
            # Find or create utm.source
            source = request.env['utm.source'].sudo().search(
                [('name', '=', source_name)], limit=1
            )
            if not source:
                source = request.env['utm.source'].sudo().create({
                    'name': source_name
                })
            
            # Prepare lead values
            lead_values = {
                'type': lead_type,
                'name': contact_name,
                'phone': phone,
                'email_from': email,
                'source_id': source.id,
                'team_id': False,  # Unassigned Sales Team
            }
            
            # Add optional fields if provided
            if preferred_course:
                lead_values['preferred_course'] = preferred_course
            if preferred_branch:
                lead_values['preferred_branch'] = preferred_branch
            
            # Create the lead
            lead = request.env['crm.lead'].sudo().create(lead_values)
            
            return {
                'status': 'success',
                'lead_id': lead.id
            }
            
        except Exception as e:
            _logger.error("Error creating lead via API: %s", str(e))
            return {
                'status': 'error',
                'message': "Something went wrong"
            }
