# -*- coding: utf-8 -*-

"""This module extends the POS Configuration (`pos.config`) model in Odoo.It adds fields to enable discount categories
 and set discount limits in the POS system."""

from odoo import fields,models

class PosConfig(models.Model):
    """Extends the `pos.config` model to include discount-related settings."""
    _inherit = 'pos.config'

    discount_categ_id = fields.Many2one(comodel_name='pos.category', string="Enable bill of materials in cart")
    discount_categ_limit = fields.Float(string='Discount limit')
