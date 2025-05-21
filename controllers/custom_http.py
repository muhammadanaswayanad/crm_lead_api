from odoo import http
from odoo.http import request
import json
import logging

_logger = logging.getLogger(__name__)

class CRMLeadAPIControllerNonJSON(http.Controller):
    @http.route('/api/create_lead/form', type='http', auth='public', methods=['POST'], csrf=False)
    def create_lead_form(self, **post):
        """Create lead from form-encoded data (for easier testing)"""
        try:
            # Access the main controller
            controller = request.env['ir.http']._find_handler('/api/create_lead')
            if not controller:
                return json.dumps({
                    'status': 'error',
                    'message': 'API endpoint not found'
                })
                
            # Call the JSON endpoint with our form data
            request.context = dict(request.context)
            request.jsonrequest = post
            result = controller.method(http, **post)
            
            return json.dumps(result)
        except Exception as e:
            _logger.error("Error in form endpoint: %s", str(e))
            return json.dumps({
                'status': 'error', 
                'message': str(e)
            })
