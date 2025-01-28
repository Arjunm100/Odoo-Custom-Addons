# -*- coding: utf-8 -*-

"""This module customizes the stock rule behavior by adding the 'tolerance' field
from the related sale order line to the stock move values. The customization
ensures the additional field is included when creating stock moves from procurement."""

from odoo import models


class StockRule(models.Model):
    """Inherits the stock.rule model to add custom behavior for stock move creation."""
    _inherit = 'stock.rule'

    def _get_stock_move_values(self, product_id, product_qty,
                               product_uom, location_id, name,
                               origin, company_id, values):
        """Extends the base method to include the 'tolerance' field in stock move values."""
        data = super()._get_stock_move_values(product_id, product_qty,
                                              product_uom, location_id, name,
                                              origin, company_id, values)
        line = self.env['sale.order.line'].browse(data.get('sale_line_id'))
        data.update({'tolerance': line.tolerance})
        return data
