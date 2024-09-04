# Authenticate the api request using the odoo api keys
import re
from odoo.http import request
from werkzeug.exceptions import BadRequest
from odoo import models


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