# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class Wmrapi(http.Controller):

    # API to get list of contacts as per search criteria
    @http.route('/wmr-api/contacts/list', methods=['GET'], auth='wmr_api_key', type='json')
    def _get_contact_list(self, **kw):
        return self.get_contact_list(kw)
    
    # API to details of all the contacts
    @http.route('/wmr-api/contacts', methods=['GET'], auth='wmr_api_key', type='json')
    def _get_contact(self, **kw):
        return self.get_contact(kw)
    
    # API to add a new contact
    @http.route('/wmr-api/contacts', methods=['POST'], auth='wmr_api_key', type='json')
    def _create_contact(self, **kw):
        return self.create_contact(kw)
    
    # API to update an existing contact
    @http.route('/wmr-api/contacts', methods=['PUT'], auth='wmr_api_key', type='json')
    def _update_contact(self, **kw):
        return self.update_contact(kw)
    
    def get_contact_list(self, kw):
        offset = kw.get('offset') if kw.get('offset') else 0
        limit = kw.get('limit') if kw.get('limit') else 0
        search = kw.get('search') if kw.get('search') else False
        properties = kw.get('properties') if kw.get('properties') else False
        
        
        if search:
            domain = [('name', 'ilike', search)]
        else:
            domain = []        

        contacts = request.env['res.partner'].search(domain,offset=offset, limit=limit).read()

        # Return only the requested properties if requested
        if properties and len(properties) > 0:
            contacts = [
                {key: obj[key] for key in properties if key in obj}
                for obj in contacts
            ]

        return contacts
        

    def get_contact(self, kw):
        contact_id = kw.get('contact_id') if kw.get('contact_id') else False
        email = kw.get('email') if kw.get('email') else False
        properties = kw.get('properties') if kw.get('properties') else False

        if contact_id:
            domain = [('id', '=', contact_id)]
        elif email:
            domain = [('email', '=', email)]

        # Get the parent contact record
        contact = request.env['res.partner'].search(domain).read()[0]

        # Return only the requested properties if requested
        if properties and len(properties) > 0:
            user = {key: user[key] for key in contact}

        # Response
        return contact

    def create_contact(self, kw):
        user =  kw.get('user')
        contact = kw.get('contact')

        # Create the parent contact record
        new_contact = request.env['res.partner'].with_user(user['id']).create({
            'name': contact['name'],
            'email': contact['email'] if contact['email'] else False,
            'phone': contact['phone'] if contact['phone'] else False,
            "lang": "en_CA",
            # 'is_company': contact['is_company'] if contact['is_company'] else False,
            # 'street': contact['street'] if contact['street'] else False,
            # 'street2': contact['street2'] if contact['street2'] else False,
            # 'city': contact['city'] if contact['city'] else False,
            # 'state_id': request.env['res.country.state'].search([('name', '=', contact['state'])]).id if contact['state'] else False,
            # 'zip': contact['zip'] if contact['zip'] else False,
            # 'country_id': request.env['res.country'].search([('name', '=', contact['country'])]).id if contact['country'] else False,
        })

        
        # Response
        return {
            'success': True,
            'contact': new_contact.read()[0],
            
        }
    
    def update_contact(self, kw):
        user =  kw.get('user')
        contact = kw.get('contact')

        # Update the parent contact record
        updated_contact = request.env['res.partner'].with_user(user['id']).search([('id', '=', contact['id'])])
        updated_contact.write({
            'name': contact['name'],
            'email': contact['email'] if contact['email'] else False,
            'phone': contact['phone'] if contact['phone'] else False,
            "lang": "en_CA",
            # 'is_company': contact['is_company'] if contact['is_company'] else False,
            # 'street': contact['street'] if contact['street'] else False,
            # 'street2': contact['street2'] if contact['street2'] else False,
            # 'city': contact['city'] if contact['city'] else False,
            # 'state_id': request.env['res.country.state'].search([('name', '=', contact['state'])]).id if contact['state'] else False,
            # 'zip': contact['zip'] if contact['zip'] else False,
            # 'country_id': request.env['res.country'].search([('name', '=', contact['country'])]).id if contact['country'] else False,
        })

        
        # Response
        return {
            'success': True,
            'contact': updated_contact.read()[0],
        }