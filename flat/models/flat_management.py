# -*- coding: utf-8 -*-

from odoo import fields,models

class FlatManagement(models.Model):
    _name = "flat.management"
    _description = "Create and Manage Flat"

    name = fields.Char(string="Name",required=True)
    company_id = fields.Many2one(string='Company', comodel_name='res.company',
                                 default=lambda self: self.env.company.id)
    currency_id = fields.Many2one(string='Currency', comodel_name='res.currency',
                                  default=lambda self: self.env.company.currency_id.id,
                                  required=True)
    price = fields.Monetary("Amount",currency_field="currency_id",required = True)
    description = fields.Text("Description")
    sale_id = fields.Many2one('flat.sale')