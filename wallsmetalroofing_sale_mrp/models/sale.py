# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    panel_count = fields.Integer()
    length_ft = fields.Integer(string="Length (ft)")
    length_in = fields.Integer(string="Length (in)")
    categ_name = fields.Char(string="Category", related='product_id.categ_id.name')

    @api.onchange('panel_count', 'length_ft', 'length_in')
    def _onchange_panel_count(self):
        self.product_uom_qty = self.panel_count * (self.length_ft + (self.length_in / 12))
