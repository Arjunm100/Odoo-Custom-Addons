# -*- coding: utf-8 -*-

"""This module defines the `ProductBrand` model,
which represents a brand associated with products"""

from odoo import fields, models


class ProductBrand(models.Model):
    """Represents a brand associated with products"""
    _name = 'product.brand'
    _description = 'Product Brand'

    name = fields.Char(required=True)
