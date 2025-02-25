# -*- coding: utf-8 -*-

"""This module extends the POS Configuration (`pos.config`) model in Odoo.It adds fields to enable discount categories
 and set discount limits in the POS system."""

from odoo import fields, models


class PosConfig(models.Model):
    """Extends the `pos.config` model to include discount-related settings."""
    _inherit = 'pos.config'

    pos_discount_wise_category_ids = fields.Many2many(comodel_name='pos.category', relation='custom_pos_config_rel',
                                                      column1="pos_config_id", column2='res_cofig_id',
                                                      string="Enable bill of materials in cart")
    pos_discount_categ_limit = fields.Float(string='Discount limit')
