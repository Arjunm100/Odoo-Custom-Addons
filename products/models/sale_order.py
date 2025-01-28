# -*- coding: utf-8 -*-

"""This module extends the `sale.order` and `sale.order.line`
models in Odoo to include additional fields and functionalities
related to prime customers and product brand management"""

from odoo import api, fields, models


class SaleOrder(models.Model):
    """Extends the `sale.order` model to include additional
    fields for prime customer tracking."""
    _inherit = 'sale.order'

    prime_customer = fields.Boolean(string='Prime Customer',
                                    related='partner_id.prime_customer')

    def action_import(self):
        """Opens a wizard for importing order lines."""
        return {'type': 'ir.actions.act_window',
                'res_model': 'order.line.import',
                'target': 'new',
                'name': ('Import Order Lines'),
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_order_id': self.id}
                }

class SaleOrderLine(models.Model):
    """Extends the `sale.order.line` model to add brand
    association and tolerance management."""
    _inherit = 'sale.order.line'
    brand_id = fields.Many2one('product.brand', string='Brand', related='product_template_id.brand_id')
    tolerance = fields.Float('Tolerance', compute='_compute_tolerance', store=True,
                             inverse='_inverse_tolerance')

    @api.depends('order_id.partner_id.tolerance')
    def _compute_tolerance(self):
        """compute the field tolerance"""
        for rec in self:
            rec.tolerance = rec.order_id.partner_id.tolerance if rec.order_id.partner_id else 0

    def _inverse_tolerance(self):
        """inverse function for tolerance"""
        return True


