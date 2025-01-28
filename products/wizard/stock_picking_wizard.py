# -*- coding: utf-8 -*-

"""Module for Stock Picking Wizard in Odoo.
Defines a transient model that allows users to validate or cancel stock picking operations."""

from odoo import fields, models


class StockPickingWizard(models.TransientModel):
    """A transient model for Stock Picking Wizard that facilitates
    specific actions on stock pickings, such as validation and cancellation."""
    _name = 'stock.picking.wizard'
    _description = 'Stock picking wizard'

    stock_picking_id = fields.Many2one('stock.picking')

    def action_continue(self):
        """Marks the associated stock picking as validated and triggers its validation button."""
        self.stock_picking_id.is_validated = True
        return self.stock_picking_id.button_validate()
