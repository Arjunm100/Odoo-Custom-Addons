# -*- coding: utf-8 -*-

"""Module to extend ResConfigSettings in Odoo by adding fields for POS category discount and discount limit
configurations."""
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    """This class extends `res.config.settings` to add POS category discount settings."""
    _inherit = 'res.config.settings'

    pos_category_wise_discount_ids = fields.Many2many(comodel_name='pos.category',
                                                      string="Enable bill of materials in cart",
                                                      relation='custom_res_settings_categ_rel',
                                                      column1="res_config_id", column2='pos_config_id',
                                                      readonly=False, compute="_compute_pos_category_wise_discount_ids",
                                                      store=True)
    pos_discount_limit = fields.Float(string='Discount limit', related='pos_config_id.pos_discount_categ_limit',
                                      readonly=False)

    @api.depends('pos_config_id.pos_discount_wise_category_ids')
    def _compute_pos_category_wise_discount_ids(self):
        self.pos_category_wise_discount_ids = [
            fields.Command.set(self.pos_config_id.pos_discount_wise_category_ids.ids)]

    @api.constrains('pos_discount_limit')
    def _check_discount_limit(self):
        """Constraint to ensure the discount limit does not exceed 100%."""
        if self.pos_discount_limit > 1:
            self.pos_discount_limit = 1

    def set_values(self):
        """Saves the selected BOM products to system parameters."""
        set_value = super().set_values()
        self.pos_config_id.pos_discount_wise_category_ids = [
            fields.Command.set(self.pos_category_wise_discount_ids.ids)]
        return set_value
