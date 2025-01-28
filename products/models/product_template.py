# -*- coding: utf-8 -*-

"""This module extends the `product.template` model in Odoo
 to include additional fields for managing product brands
and ownership types"""

from odoo import fields, models


class ProductTemplate(models.Model):
    """Extends the `product.template` model to add support
    for associating a product with a brand and defining its
    ownership type"""
    _inherit = 'product.template'

    brand_id = fields.Many2one('product.brand', string='Brand')
    ownership_type = fields.Selection(string='Ownership Type',
                                      selection=[('single', 'Single Product'),
                                                 ('brand', 'Branded Product')],
                                      default='single')
