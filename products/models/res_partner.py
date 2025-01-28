# -*- coding: utf-8 -*-

"""This model extends the 'res.partner' model to include
additional fields prime_customer and tolerance"""

from odoo import fields, models


class ResPartner(models.Model):
    """extends the 'res.partner' model to include
    additional fields prime_customer and tolerance"""

    _inherit = 'res.partner'

    prime_customer = fields.Boolean(string='Prime Customer')
    tolerance = fields.Float('Transfer Tolerance')
