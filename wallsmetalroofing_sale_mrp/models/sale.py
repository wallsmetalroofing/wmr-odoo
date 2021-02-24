# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    panel_count = fields.Float()
    length_ft = fields.Float(string="Length (ft)")
    length_in = fields.Float(string="Length (in)")

    @api.onchange('panel_count', 'length_ft', 'length_in')
    def _onchange_panel_count(self):
        self.product_uom_qty = self.panel_count * (self.length_ft + (self.length_in / 12))

    # def _prepare_procurement_values(self, group_id=False):
    #     values = super()._prepare_procurement_values()
    #     values.update({
    #         'panel_count': self.panel_count,
    #         'length_ft': self.length_ft,
    #         'length_in': self.length_in,
    #     })
    #     return values


# class StockRule(models.Model):
#     _inherit = 'stock.rule'

#     @api.model
#     def _run_manufacture(self, procurements):
#         res = super()._run_manufacture(procurements)
#         return res
