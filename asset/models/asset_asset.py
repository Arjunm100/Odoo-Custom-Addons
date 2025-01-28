# -*- coding: utf-8 -*-

from odoo import fields,models,api

class AssetAsset(models.Model):
    _name = 'asset.asset'
    _description = 'Asset'

    name = fields.Char(required= True)
    type = fields.Selection(string='Asset type',selection=[
        ('lap','Laptop'),('phone','Phone'),('vehicle','Vehicle'),('others','Others')
    ],required=True)
    purchase_date = fields.Date(required=True)
    value = fields.Float('Asset Value',compute="_computex")

    # @api.depends('name')
    def _computex(self):
        print("triggered")
        for rec in self:
            rec.value = 1 if rec.name == "a" else 5