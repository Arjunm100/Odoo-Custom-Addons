# -*- coding: utf-8 -*-

"""Extends the 'res.partner' model to include a smart button with to access property"""

from odoo import fields, models


class ResPartner(models.Model):
    """Extends the 'res.partner' model to integrate a smart button with to access property"""
    _inherit = 'res.partner'

    property_count = fields.Integer(compute='_compute_property_count')

    def _compute_property_count(self):
        self.property_count = (self.env['property.management'].
                               search_count([('owner_id', '=', self.id)]))

    def action_open_property(self):
        """Open the property record related to the current Partner"""
        self.ensure_one()
        list_view_id = self.env.ref('property.property_management_view_list_owner').id
        form_view_id = self.env.ref('property.property_management_view_form').id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Properties',
            'view_mode': 'list,form',
            'res_model': 'property.management',
            'views': [(list_view_id, 'list'), (form_view_id, 'form')],
            'domain': [('owner_id', '=', self.id)]
        }
