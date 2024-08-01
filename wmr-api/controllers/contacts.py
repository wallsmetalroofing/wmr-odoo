# -*- coding: utf-8 -*-

from odoo import http, models
from odoo.http import request
from werkzeug.exceptions import BadRequest
import re


# Authenticate the api request using the odoo api keys
class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _auth_method_wmr_api_key(cls):
        api_key = request.httprequest.headers.get("Authorization")
        if not api_key:
            raise BadRequest(
                "Authorization header with API key missing")

        # sanitize the bearer token to retrieve the api key
        api_key = re.sub(r'bearer\s', '', api_key, 1, re.IGNORECASE)
        user_id = request.env["res.users.apikeys"]._check_credentials(
            scope="rpc", key=api_key
        )

        # check that the user id is set
        if not user_id:
            raise BadRequest("API key invalid")

        # Validate the ip address and only allow request coming through the provided ip address
        ip_address = request.httprequest.environ.get('REMOTE_ADDR')
        allowed_ip = request.env['ir.config_parameter'].sudo().get_param('wmr_allowed.ip.addresses')
        access_granted =False

        array = allowed_ip.split(",")
        array = [item.strip() for item in array]

        for item in array:
            if item == ip_address:
                access_granted = True
                break

        if not access_granted:
            raise BadRequest("Cannot access the API through this device")
        
        request.update_env(user_id)


class Wmrapi(http.Controller):

    # API to Add Quotes to an existing sales record
    @http.route('/wmr-api/contacts', methods=['POST'], auth='wmr_api_key', type='json')
    def _create_contact(self, **kw):
        return self.create_contact(kw)
    
    # API to Add Quotes to an existing sales record
    @http.route('/wmr-api/contacts', methods=['PUT'], auth='wmr_api_key', type='json')
    def _update_contact(self, **kw):
        return self.update_contact(kw)


    def create_contact(self, kw):
        user =  kw.get('user')
        contact = kw.get('contact')

        # Create the parent contact record
        parent_contact = request.env['res.partner'].with_user(user['id']).create({
            'name': contact['name'],
            'is_company': contact['is_company'] if contact['is_company'] else False,
            "lang": "en_CA",
            'street': contact['street'],
            'street2': contact['street2'],
            'city': contact['city'],
            'state_id': request.env['res.country.state'].search([('name', '=', contact['state'])]).id,
            'zip': contact['zip'],
            'country_id': request.env['res.country'].search([('name', '=', contact['country'])]).id,
        })

        
        # Response
        return {
            'success': True,
            'sale': {
                'contact': parent_contact.read(),
            }
        }
    
    def update_contact(self, kw):
        user =  kw.get('user')
        contact = kw.get('contact')

        # Update the parent contact record
        parent_contact = request.env['res.partner'].with_user(user['id']).search([('id', '=', contact['id'])])
        parent_contact.write({
            'name': contact['name'],
            'is_company': contact['is_company'] if contact['is_company'] else False,
            "lang": "en_CA",
            'street': contact['street'],
            'street2': contact['street2'],
            'city': contact['city'],
            'state_id': request.env['res.country.state'].search([('name', '=', contact['state'])]).id,
            'zip': contact['zip'],
            'country_id': request.env['res.country'].search([('name', '=', contact['country'])]).id,
            
        })

        
        # Response
        return {
            'success': True,
            'sale': {
                'contact': parent_contact.read(),
            }
        }