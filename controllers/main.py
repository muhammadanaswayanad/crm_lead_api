from odoo import http
from odoo.http import request
import logging
import json
import traceback

_logger = logging.getLogger(__name__)

class CRMLeadAPIController(http.Controller):
    
    @http.route('/api/debug', type='json', auth='public', methods=['POST'], csrf=False)
    def debug_endpoint(self, **post):
        """Simple endpoint to test API connectivity"""
        return {
            'status': 'success',
            'message': 'API connection successful',
            'odoo_version': request.env['ir.module.module'].sudo().search([('name', '=', 'base')]).installed_version
        }
    
    @http.route('/api/create_lead', type='http', auth='public', methods=['POST'], csrf=False)
    def create_lead(self, **post):
        """Create a new lead from API request"""
        try:
            # Get the JSON data
            data = json.loads(request.httprequest.data.decode('utf-8'))
            _logger.info("Received lead creation request with data: %s", data)
            
            # Validate required fields
            required_fields = ['type', 'contact_name', 'phone', 'email', 'source']
            missing_fields = [field for field in required_fields if not data.get(field)]
            
            if missing_fields:
                response = {
                    'status': 'error', 
                    'message': f"Missing fields: {', '.join(missing_fields)}"
                }
                return json.dumps(response)
            
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
                _logger.info("Creating new UTM source: %s", source_name)
                source = request.env['utm.source'].sudo().create({
                    'name': source_name
                })
            
            # Prepare lead values
            lead_values = {
                'type': lead_type,
                'name': f"Lead for {contact_name}",  # Descriptive lead name
                'contact_name': contact_name,        # Actual contact name
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
            
            _logger.info("Creating lead with values: %s", lead_values)
            
            # Create the lead with superuser privileges
            lead = request.env['crm.lead'].sudo().create(lead_values)
            _logger.info("Lead created successfully with ID: %s", lead.id)
            
            response = {
                'status': 'success',
                'lead_id': lead.id
            }
            return json.dumps(response)
            
        except Exception as e:
            tb = traceback.format_exc()
            _logger.error("Error creating lead via API: %s\n%s", str(e), tb)
            response = {
                'status': 'error',
                'message': f"Error: {str(e)}",
                'details': tb if request.env.user.has_group('base.group_system') else None
            }
            return json.dumps(response)
