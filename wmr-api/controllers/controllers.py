# -*- coding: utf-8 -*-
from odoo import http


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
            # x_app_group_id = line['x_app_group_id'] if(line['x_app_group_id']) else False
            order_line.append((0,0,{
                'product_id' : product_id,
                'name' : name,
                'product_uom_qty' : product_uom_qty,
                'price_unit' : price_unit,
                'display_type' : display_type,
                # 'x_app_group_id' : x_app_group_id
            }))

        sale_data = {
            'partner_id' : sale['partner_id'],
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
    def index(self, request):
        print("Entered in Updating Sales")

        user = request.params['user']
        sale = request.params['sale']

        sale_data = request.env['sale.order'].search(['id','=',sale['id'])

        # res = request.env['sale.order'].with_user(
        #     user['id']
        # ).create([sale_data])
        # print(res)
        print("Leaving Creating Sales")

        return {
            'success': True,
            'sale': {
                'id': sale_data
            }
        }
    

#     @http.route('/wmr-api/wmr-api/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('wmr-api.listing', {
#             'root': '/wmr-api/wmr-api',
#             'objects': http.request.env['wmr-api.wmr-api'].search([]),
#         })

#     @http.route('/wmr-api/wmr-api/objects/<model("wmr-api.wmr-api"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wmr-api.object', {
#             'object': obj
#         })
