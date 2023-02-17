# -*- coding: utf-8 -*-

from odoo import http, SUPERUSER_ID, models
from odoo.http import request
from werkzeug.exceptions import BadRequest
import html2text


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
    @http.route('/wmr-api/wmr-api/sales/create', auth='public', type='json')
    def index(self, request):
        print("Entered in Creating Sales")
        
        user = request.params['user']
        sale = request.params['sale']
        order_lines = sale['order_line']


        order_line = []
        for line in order_lines:
            product_id = line['product_id'] if(line['product_id']) else False
            is_configurable_product = line['is_configurable_product'] if(line['is_configurable_product']) else False
            name = line['name'] if(line['name']) else False
            product_uom_qty = line['product_uom_qty'] if(line['product_uom_qty']) else False
            price_unit = line['price_unit'] if(line['price_unit']) else False
            display_type = line['display_type'] if(line['display_type']) else False
            x_app_group_id = line['x_app_group_id'] if(line['x_app_group_id']) else False
            order_line.append((0,0,{
                'product_id' : product_id,
                'name' : name,
                'product_uom_qty' : product_uom_qty,
                'price_unit' : price_unit,
                'display_type' : display_type,
                'x_app_group_id' : x_app_group_id
            }))

        sale_data = {
            'partner_id' : sale['partner_id'],
            "x_studio_quote_id": sale['x_studio_quote_id'],
            'note' : sale['note'],
            'payment_term_id': sale['payment_term_id'],
            'order_line' : order_line
        }



        res = request.env['sale.order'].with_user(
            user['id']
        ).create([sale_data])
        print(res)

        return {
            'success': True,
            'sale': {
                'id': res.id
            }
        }
    


    @http.route('/wmr-api/wmr-api/sales/update', auth='public', type='json')
    def list(self, **kw):
        print("Entered in Updating Sales")
        user = kw.get('user')
        sale = kw.get('sale')
        order_lines = sale["order_line"]
        order_id = sale["id"]

        sale_data = request.env['sale.order'].with_user(2).search([('id', '=', order_id)])

        order_line = []
        for line in order_lines:
            product_id = line['product_id'] if(line['product_id']) else False
            name = line['name'] if(line['name']) else False
            product_uom_qty = line['product_uom_qty'] if(line['product_uom_qty']) else False
            price_unit = line['price_unit'] if(line['price_unit']) else False
            display_type = line['display_type'] if(line['display_type']) else False
            x_app_group_id = line['x_app_group_id'] if(line['x_app_group_id']) else False
            lines = {
                'product_id' : product_id,
                'name' : name,
                'product_uom_qty' : product_uom_qty,
                'price_unit' : price_unit,
                'display_type' : display_type,
                'x_app_group_id' : x_app_group_id,
                'order_id' : order_id
            }
            order = request.env['sale.order'].with_user(2).search([('id', '=', order_id)])
            new_order_line = request.env['sale.order.line'].with_user(2).create(lines)
            sale_data.write({})
            order_line.append(new_order_line)
        x_studio_quote_id = sale_data.x_studio_quote_id
        x_studio_quote_id = x_studio_quote_id + ", " + sale['x_studio_quote_id']
        note = sale_data.note
        # if(sale['note']):
        #     note = html2text.html2text(note) + ", " +sale['note']
        #     note = note.replace('\n', ' ').replace('\r', '')
        sale_data.write({
            'x_studio_quote_id' : x_studio_quote_id,
            'note' : note
        })
        sale_data1 = request.env['sale.order'].with_user(2).search([('id', '=', order_id)])



        # res = request.env['sale.order'].with_user(
        #     user['id']
        # ).create([sale_data])
        # print(res)
        print("Leaving Creating Sales")

        return {
            'success': True,
            'sale': {
                'id': sale_data1.id,
                'x_studio_quote_id': sale_data1.x_studio_quote_id,
                'note': html2text.html2text(sale_data1.note),
                'payment_term_id': sale_data1.payment_term_id,
                'order_line': sale_data1.order_line,
            }
        }

#     @http.route('/wmr-api/wmr-api/objects/<model("wmr-api.wmr-api"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wmr-api.object', {
#             'object': obj
#         })