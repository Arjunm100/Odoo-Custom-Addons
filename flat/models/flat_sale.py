# -*- coding: utf-8 -*-

from odoo import fields,models

class FlatSale(models.Model):
    _name = "flat.sale"
    _description = "Manage flat sales"

    flat_ids = fields.One2many(comodel_name='flat.management',inverse_name='sale_id')