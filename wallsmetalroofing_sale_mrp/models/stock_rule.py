# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _prepare_mo_vals(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values, bom):
        stock_moves = values.get('move_dest_ids')
        values = super()._prepare_mo_vals(product_id, product_qty, product_uom,
                                          location_id, name, origin, company_id, values, bom)
        if stock_moves and len(stock_moves) == 1:
            line = stock_moves.sale_line_id
            values.update({
                'panel_count': line.panel_count,
                'length_ft': line.length_ft,
                'length_in': line.length_in,
            })
        return values
