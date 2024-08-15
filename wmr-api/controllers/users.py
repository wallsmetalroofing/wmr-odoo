# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class Wmrapi(http.Controller):

    # API to get list of users as per search criteria
    @http.route('/wmr-api/users/list', methods=['GET'], auth='wmr_api_key', type='json')
    def _get_user_list(self, **kw):
        return self.get_user_list(kw)
    
    # API to details of all the users
    @http.route('/wmr-api/users', methods=['GET'], auth='wmr_api_key', type='json')
    def _get_user(self, **kw):
        return self.get_user(kw)
    
    def get_user_list(self, kw):
        offset = kw.get('offset') if kw.get('offset') else 0
        limit = kw.get('limit') if kw.get('limit') else 0
        search = kw.get('search') if kw.get('search') else False
        properties = kw.get('properties') if kw.get('properties') else False

        
        if search:
            domain = [('name', 'ilike', search)]
        else:
            domain = []        

        users = request.env['res.users'].search(domain,offset=offset, limit=limit).read()

        # Return only the requested properties if requested
        if properties and len(properties) > 0:
            users = [
                {key: obj[key] for key in properties if key in obj}
                for obj in users
            ]

        return users
        


    def get_user(self, kw):
        user_id = kw.get('user_id') if kw.get('user_id') else False
        email = kw.get('email') if kw.get('email') else False
        properties = kw.get('properties') if kw.get('properties') else False

        if user_id:
            domain = [('id', '=', user_id)]
        elif email:
            domain = [('email', '=', email)]

        # Get the parent user record
        user = request.env['res.users'].search(domain).read()[0]

        # Return only the requested properties if requested
        if properties and len(properties) > 0:
            user = {key: user[key] for key in properties}

        # Response
        return user

        user =  kw.get('user')
        user = kw.get('user')

        # Update the parent user record
        updated_user = request.env['res.partner'].with_user(user['id']).search([('id', '=', user['id'])])
        updated_user.write({
            'name': user['name'],
            'email': user['email'] if user['email'] else False,
            'phone': user['phone'] if user['phone'] else False,
            "lang": "en_CA",
            # 'is_company': user['is_company'] if user['is_company'] else False,
            # 'street': user['street'] if user['street'] else False,
            # 'street2': user['street2'] if user['street2'] else False,
            # 'city': user['city'] if user['city'] else False,
            # 'state_id': request.env['res.country.state'].search([('name', '=', user['state'])]).id if user['state'] else False,
            # 'zip': user['zip'] if user['zip'] else False,
            # 'country_id': request.env['res.country'].search([('name', '=', user['country'])]).id if user['country'] else False,
        })

        
        # Response
        return {
            'success': True,
            'user': updated_user.read()[0],
        }