# -*- coding: utf-8 -*-

"""Module for extending ResConfigSettings to add a configuration option to enable specific bill of materials (BOM)
products in the shopping cart by storing and retrieving them from system parameters."""

from odoo import api,fields, models

class ResConfigSettings(models.TransientModel):
   """Extends ResConfigSettings to allow selection of BOM products for the cart."""
   _inherit = 'res.config.settings'

   product_ids = fields.Many2many(comodel_name='product.product',string="Enable bill of materials in cart",
                                  domain=[('bom_ids','!=',False)])

   def set_values(self):
      """Saves the selected BOM products to system parameters."""
      set_value = super().set_values()
      self.env['ir.config_parameter'].set_param(
         'cart_bom_products', str([i.id for i in self.product_ids]))
      return set_value

   @api.model
   def get_values(self):
      """Saves the selected BOM products to system parameters."""
      res = super().get_values()
      params = self.env['ir.config_parameter'].sudo()
      cart_bom_products = params.get_param('cart_bom_products')
      res.update(product_ids=[fields.Command.link(id) for id in eval(cart_bom_products)])
      return res