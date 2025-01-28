# -*- coding: utf-8 -*-

"""This module extends the `stock.picking` model in Odoo to include additional validation logic
based on tolerance levels for products associated with purchase or sale lines."""

from odoo import fields, models


class StockPicking(models.Model):
    """Extends the `stock.picking` model to add custom
    validation logic for product movements based
    on associated purchase or sale line tolerances."""

    _inherit = 'stock.picking'

    is_validated = fields.Boolean(copy=False)
    tolerance = fields.Float(string="Tolerance",
                             compute='_compute_tolerance', inverse='_inverse_tolerance')

    def button_validate(self):
        """Overrides the `button_validate` method to
        introduce custom validation logic for stock pickings."""
        if all(line.product_uom_qty - line.tolerance <=
               line.quantity <=
               line.product_uom_qty + line.tolerance
               for line in self.move_ids) or self.is_validated:
            return super().button_validate()
        else:
            return {'type': 'ir.actions.act_window',
                    'res_model': 'stock.picking.wizard',
                    'target': 'new',
                    'name': ('Alert Message'),
                    'view_mode': 'form',
                    'view_type': 'form',
                    'context': {'default_stock_picking_id': self.id}
                    }


class StockMove(models.Model):
    """Extends the 'stock.move' model to add additional field tolerance"""
    _inherit = 'stock.move'

    tolerance = fields.Float(string="Tolerance")
