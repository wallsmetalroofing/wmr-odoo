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


class WmrApiSales(http.Controller):

    # API to get a sales record
    @http.route('/wmr-api/sales', methods=['GET'], auth='wmr_api_key', type='json')
    def _get_sales(self, **kw):
        return self.get_sales(kw)

    # API to Create a sales record
    @http.route('/wmr-api/sales', methods=['POST'], auth='wmr_api_key', type='json')
    def _create_sales(self, **kw):
        return self.create_sales_record( kw)

    # API to update the Quote
    @http.route('/wmr-api/sales', methods=['PUT'], auth='wmr_api_key', type='json')
    def _update_sales__order(self, **kw):
        return self.update_sales_order(kw)

    # API to Add Quotes to an existing sales record
    @http.route('/wmr-api/sales/add', methods=['PUT'], auth='wmr_api_key', type='json')
    def _add_order_lines(self, **kw):
        return self.add_order_lines(kw)
    
    # API to confirm orders
    @http.route('/wmr-api/sales/confirm', methods=['PUT'], auth='wmr_api_key', type='json')
    def _confirm_sales_order(self, **kw):
        return self.confirm_sales_order(kw)
    
        
    def get_sales(self, kw):
        user = kw.get('user')
        sale = kw.get('sale')
        order_id = sale["id"]

        sale_data = request.env['sale.order'].with_user(user['id']).search([('id', '=', order_id)])

        return {
            'success': True,
            'sale': sale_data.read()[0],
            'order_line':sale_data[0]['order_line'].read()
        }
    
    # Create a quote
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
            'partner_invoice_id': sale['partner_invoice_id'],
            'partner_shipping_id': sale['partner_shipping_id'],
            "x_studio_quote_id": sale['x_studio_quote_id'],
            'note' : sale['note'],
            'payment_term_id': sale['payment_term_id'],
            'type_name': 'Quotation',
            'state': 'sale',                       
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
    
    # Confirms the quote to order
    def confirm_sales_order(self, kw):
        user =  kw.get('user')
        sale =  kw.get('sale')
        order_id = sale["id"]
        # Update details before confirming th order
        self.update_sales_order( kw)
        
        sale_data = request.env['sale.order'].with_user(user['id']).search([('id', '=', order_id)])
        sale_data.write({
            'state': 'sale'
            })

        res = request.env['sale.order'].with_user(user['id']).search([('id', '=', order_id)])

        # Response
        return {
            'success': True,
            'sale': res.read()
        }
    
    # Update the Quote
    def update_sales_order(self, kw):
        user =  kw.get('user')
        sale =  kw.get('sale')
        order_lines = sale['order_line']
        order_id = sale["id"]


        sale_data = request.env['sale.order'].with_user(user['id']).search([('id', '=', order_id)])

        # Append all order lines in an array to add sales.order
        order_line_ids = []
        for order_line in order_lines:
            product_id = order_line['product_id'] if(order_line['product_id']) else False
            name = order_line['name'] if(order_line['name']) else False
            product_uom_qty = order_line['product_uom_qty'] if(order_line['product_uom_qty']) else False
            price_unit = order_line['price_unit'] if(order_line['price_unit']) else False
            display_type = order_line['display_type'] if(order_line['display_type']) else False
            x_app_quote_id = order_line['x_app_quote_id'] if(order_line['x_app_quote_id']) else False
            x_app_group_id = order_line['x_app_group_id'] if(order_line['x_app_group_id']) else False
            # Appending orderline as per the format accepted in sales order
            line = {
                'product_id' : product_id,
                'name' : name,
                'product_uom_qty' : product_uom_qty,
                'price_unit' : price_unit,
                'display_type' : display_type,
                'x_app_quote_id' : x_app_quote_id,
                'x_app_group_id' : x_app_group_id,
                'type_name': 'Quotation',
                'state': 'sale',
                'order_id':order_id
            }

            # check if the order_line was already existing and edit it if it exist.
            if 'id' in order_line:
                line_data = request.env['sale.order.line'].with_user(user['id']).search([('id', '=', order_line['id'])])
                line_data.write(line)
                order_line_ids.append(order_line['id'])
            else:
                # If the order_line was not existing, create a new one
                new_order_line = request.env['sale.order.line'].with_user(user['id']).create(line)
                order_line_ids.append(new_order_line.id)
            sale_data.write({})

        # Remove the old entries which are not present in the   
        for order_line in sale_data['order_line']:
            if order_line['id'] not in order_line_ids:
                order_line.unlink()
                sale_data.write({})
        
        
        # JSON object to be sent for adding Sales Record
        sale_data.write( {
            'partner_id' : sale['partner_id'],
            'partner_invoice_id': sale['partner_invoice_id'],
            'partner_shipping_id': sale['partner_shipping_id'],
            'x_studio_quote_id': sale['x_studio_quote_id'],
            'note' : sale['note'],
            'payment_term_id': sale['payment_term_id']
        })

        res = request.env['sale.order'].with_user(user['id']).search([('id', '=', order_id)])

        # Response
        return {
            'success': True,
            'sale': res.read()
        }

    # Adds the order_lines,quoteIds and notes to the order 
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