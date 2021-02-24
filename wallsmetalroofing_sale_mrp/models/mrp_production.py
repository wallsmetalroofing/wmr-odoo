# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    panel_count = fields.Float()
    length_ft = fields.Float(string="Length (ft)")
    length_in = fields.Float(string="Length (in)")
