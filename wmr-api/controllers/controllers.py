# -*- coding: utf-8 -*-

from odoo import http, models
from odoo.http import request
from werkzeug.exceptions import BadRequest
import html2text
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

        request.uid = user_id


class Wmrapi(http.Controller):

    # API to Create a sales record
    @http.route('/wmr-api/sales/create', auth='wmr_api_key', type='json')
    def _create_sales(self, **kw):
        return self.create_sales_record( kw)

    # API to Add Quotes to an existing sales record
    @http.route('/wmr-api/sales/update', auth='wmr_api_key', type='json')
    def _add_order_lines(self, **kw):
        return self.add_order_lines(kw)

    # API to Add Quotes to an existing sales record
    @http.route('/wmr-api/contacts/create', auth='wmr_api_key', type='json')
    def _add_order_lines(self, **kw):
        return self.create_contact(kw)

    

    def create_sales_record(self, kw):
        user =  kw.get('user')
        sale =  kw.get('sale')
        order_lines = sale['order_line']

        # Append all order lines in an array to add sales.order
        order_line = []
        for line in order_lines:
            product_id = line['product_id'] if(line['product_id']) else False
            name = line['name'] if(line['name']) else False
            product_uom_qty = line['product_uom_qty'] if(line['product_uom_qty']) else False
            price_unit = line['price_unit'] if(line['price_unit']) else False
            display_type = line['display_type'] if(line['display_type']) else False
            x_app_quote_id = line['x_app_quote_id'] if(line['x_app_quote_id']) else False
            x_app_group_id = line['x_app_group_id'] if(line['x_app_group_id']) else False
            # Appending orderline as per the format accepted in sales order
            order_line.append((0,0,{
                'product_id' : product_id,
                'name' : name,
                'product_uom_qty' : product_uom_qty,
                'price_unit' : price_unit,
                'display_type' : display_type,
                'x_app_quote_id' : x_app_quote_id,
                'x_app_group_id' : x_app_group_id
            }))

        # JSON object to be sent for adding Sales Record
        sale_data = {
            'partner_id' : sale['partner_id'],
            "x_studio_quote_id": sale['x_studio_quote_id'],
            'note' : sale['note'],
            'payment_term_id': sale['payment_term_id'],
            'order_line' : order_line
        }

        # Adding Sales Record
        res = request.env['sale.order'].with_user(
            user['id']
        ).create([sale_data])

        # Response
        return {
            'success': True,
            'sale': {
                'id': res.id
            }
        }
    
    def add_order_lines(self, kw):
        user = kw.get('user')
        sale = kw.get('sale')
        order_lines = sale["order_line"]
        order_id = sale["id"]

        sale_data = request.env['sale.order'].with_user(user['id']).search([('id', '=', order_id)])

        order_line =[]
        for line in order_lines:
            product_id = line['product_id'] if(line['product_id']) else False
            name = line['name'] if(line['name']) else False
            product_uom_qty = line['product_uom_qty'] if(line['product_uom_qty']) else False
            price_unit = line['price_unit'] if(line['price_unit']) else False
            display_type = line['display_type'] if(line['display_type']) else False
            x_app_quote_id = line['x_app_quote_id'] if(line['x_app_quote_id']) else False
            x_app_group_id = line['x_app_group_id'] if(line['x_app_group_id']) else False
            lines = {
                'product_id' : product_id,
                'name' : name,
                'product_uom_qty' : product_uom_qty,
                'price_unit' : price_unit,
                'display_type' : display_type,
                'x_app_quote_id' : x_app_quote_id,
                'x_app_group_id' : x_app_group_id,
                'order_id' : order_id
            }
            # Adding Order Line to the table
            new_order_line = request.env['sale.order.line'].with_user(user['id']).create(lines)
            sale_data.write({})
            order_line.append(new_order_line.id)

        x_studio_quote_id = sale_data.x_studio_quote_id
        x_studio_quote_id = x_studio_quote_id + ", " + sale['x_studio_quote_id']
        note = sale_data.note
        if(sale['note']):
            note = html2text.html2text(note) + ", " +sale['note']
        
        # Updating Quote and Note
        sale_data.write({
            'x_studio_quote_id' : x_studio_quote_id,
            'note' : note
        })

        # Response
        return {
            'success': True,
            'sale': {
                'sales_id': sale_data.id,
                'order_lines_id': order_line,
            }
        }

    def create_contact(self, kw):
        user =  kw.get('user')
        contact = kw.get('data')

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

        # Create the child contact records and link it to the parent contact
        for child_contact in contact['child_contacts']:
            child_contact = request.env['res.partner.contacts'].with_user(user['id']).create({
                'name': child_contact['name'],
                'partner_id': parent_contact.id,
                'telephone': child_contact['telephone'],
                'email':  child_contact['email']
            })
        
        # Response
        return {
            'success': True,
            'sale': {
                'contact': parent_contact.read(),
                'child_contact': parent_contact.contact_ids.read()
            }
        }