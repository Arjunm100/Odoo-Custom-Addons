# -*- coding: utf-8 -*-

from odoo import api,fields,models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    order_state = fields.Selection(selection=[('open','Open'),('close','Close')],compute='_compute_order_state',
                                   inverse='_inverse_order_state',store=True)

    @api.depends('delivery_status')
    def _compute_order_state(self):
        for rec in self:
            if rec.delivery_status == 'full':
                rec.order_state = 'close'
            else:
                rec.order_state = rec.order_state

    def _inverse_order_state(self):
        return True
