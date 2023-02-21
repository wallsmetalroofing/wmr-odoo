import json
import re

from odoo import SUPERUSER_ID, http, models
from odoo.http import request
from werkzeug.exceptions import BadRequest


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


# Create the primary api entry point
class ApiController(http.Controller):

    # Listen for product create requests
    @http.route("/wmr/product/create", auth="wmr_api_key", type="json")
    def product_create(self, request):
        print("Create Product")

        user = request.params['user']
        product = request.params['product']

        res = request.env['product.product'].with_user(
            user['id']
        ).create([product])
        print(res)

        return {
            'success': True,
            'product': {
                'id': res.id
            }
        }

    # Listen for product create requests
    @http.route("/wmr/product/update", auth="wmr_api_key", type="json")
    def product_update(self, request):
        print("Update Product")

        user = request.params['user']
        product = request.params['product']
        product_id = product['id']
        del product['id']

        # Get and update the record details
        record = request.env['product.product'].browse([product_id])
        record.with_user(
            user['id']
        ).update(product)

        return {
            'success': True,
            'product': {
                'id': product_id
            }
        }

    # Listen for product create requests
    @http.route("/wmr/product/template/create", auth="wmr_api_key", type="json")
    def product_template_create(self, request):
        print("Create Product")

        user = request.params['user']
        product = request.params['product']

        res = request.env['product.template'].with_user(
            user['id']
        ).create([product])
        print(res)

        return {
            'success': True,
            'product': {
                'id': res.id
            }
        }

    # Listen for product create requests
    @http.route("/wmr/product/template/update", auth="wmr_api_key", type="json")
    def product_template_update(self, request):
        print("Update Product")

        user = request.params['user']
        product = request.params['product']
        product_id = product['id']
        del product['id']

        # Get and update the record details
        record = request.env['product.template'].browse([product_id])
        record.with_user(
            user['id']
        ).update(product)

        return {
            'success': True,
            'product': {
                'id': product_id
            }
        }

    # Listen for Sales create requests
    @http.route("/wmr/sales/order/create", auth="wmr_api_key", type="json")
    def sale_order_create(self, request):
        print("Create Sales")

        user = request.params['user']
        sale = request.params['sale']

        res = request.env['sale.order'].with_user(
            user['id']
        ).create([sale])
        print(res)

        return {
            'success': True,
            'sale': {
                'id': res.id
            }
        }
        
    # Listen for Sales update requests
    @http.route("/wmr/sales/order/update", auth="wmr_api_key", type="json")
    def sale_order_create(self, request):
        print("Create Sales")

        user = request.params['user']
        sale = request.params['sale']

        res = request.env['sale.order'].with_user(
            user['id']
        ).create([sale])
        print(res)

        return {
            'success': True,
            'sale': {
                'id': res.id
            }
        }


