# -*- coding: utf-8 -*-

"""Module extending the 'product.product' model to add a POS rating field."""

from odoo import fields, models


class ProductProduct(models.Model):
    """class extends the `product.product` model to introduce a new field `rating` which allows a point-of-sale (POS)
    rating selection from 0 to 5."""

    _inherit = 'product.product'

    pos_rating = fields.Selection(string="Pos Rating", selection=[
        ('0', ''), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], default='0', required=1)

    def _load_pos_data_fields(self, config_id):
        """Extend POS data fields to include the rating field."""
        data = super()._load_pos_data_fields(config_id)
        data.append('pos_rating')
        return data
