# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    panel_count = fields.Integer()
    length_ft = fields.Integer(string="Length (ft)")
    length_in = fields.Integer(string="Length (in)")
