# -*- coding: utf-8 -*-

"""Module for extending ResConfigSettings to add a configuration option to enable specific bill of materials (BOM)
products in the shopping cart by storing and retrieving them from system parameters."""

from odoo import api,fields, models

class ResConfigSettings(models.TransientModel):
   """Extends ResConfigSettings to allow selection of BOM products for the cart."""
   _inherit = 'res.config.settings'

   pos_categ_discount_id = fields.Many2one(comodel_name='pos.category',string="Enable bill of materials in cart")
   categ_discount_limit = fields.Float(string='Discount limit')
