# -*- coding: utf-8 -*-

"""Extends the 'account.move' model to include a relationship with rent/lease orders"""

from odoo import fields, models


class AccountMove(models.Model):
    """Extends the 'account.move' model to integrate property rent/lease orders"""
    _inherit = 'account.move'

    rent_lease_order_id = fields.Many2one(string="Rent Lease order",
                                          comodel_name='property.rent.lease')
