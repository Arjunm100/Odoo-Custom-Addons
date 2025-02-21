# -*- coding: utf-8 -*-

"""Module to extend ResConfigSettings in Odoo by adding fields for POS category discount and discount limit
configurations."""

from odoo import api,fields, models

class ResConfigSettings(models.TransientModel):
    """This class extends `res.config.settings` to add POS category discount settings."""
    _inherit = 'res.config.settings'

    pos_categ_discount_id = fields.Many2one(comodel_name='pos.category',string="Enable bill of materials in cart",
                                           related='pos_config_id.discount_categ_id',readonly=False)
    pos_discount_limit = fields.Float(string='Discount limit',related='pos_config_id.discount_categ_limit',
                                      readonly=False)

    @api.constrains('pos_discount_limit')
    def _check_discount_limit(self):
        """Constraint to ensure the discount limit does not exceed 100%."""
        print(self.pos_discount_limit)
        if self.pos_discount_limit > 1:
            self.pos_discount_limit = 1
