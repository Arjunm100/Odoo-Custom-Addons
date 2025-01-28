# -*- coding: utf-8 -*-

"""Module for managing properties"""

from odoo import fields, models


class PropertyManagement(models.Model):
    """Represents a property"""
    _name = 'property.management'
    _description = 'Property Management'
    _inherit = 'mail.thread'

    name = fields.Char(string="Property Name", required=True)
    image = fields.Image(string=" ")
    can_sold = fields.Boolean(string='Can Be Sold')
    first_street = fields.Char(string='First Street')
    second_street = fields.Char(string='Second Street')
    active = fields.Boolean(default=True)
    city = fields.Char(string='City')
    state_id = fields.Many2one(string='State', comodel_name='res.country.state', required=True)
    pincode = fields.Char(string="Pincode")
    country_id = fields.Many2one(string='Country', comodel_name='res.country', required=True)
    facility_ids = fields.Many2many(string='Facility', comodel_name='property.facility')
    company_id = fields.Many2one(string='Company', comodel_name='res.company',
                                 default=lambda self: self.env.company.id)
    currency_id = fields.Many2one(string='Currency', comodel_name='res.currency',
                                  default=lambda self: self.env.company.currency_id.id,
                                  required=True)
    owner_id = fields.Many2one(string='Owner', comodel_name='res.partner', required=True)
    built_date = fields.Datetime(string="Build Date", required=True, default=fields.Datetime.now)
    price = fields.Monetary(string='Price', currency_field='currency_id')
    rent_amount = fields.Monetary(string='Rent', currency_field='currency_id')
    lease_amount = fields.Monetary(currency_field='currency_id')
    status = fields.Selection(selection=[
        ('draft', 'Draft'), ('rented', 'Rented'), ('leased', 'Leased'), ('sold', 'Sold')
    ], readonly=False, tracking=True, default='draft')
    description = fields.Text(string='Description')
    offer_count = fields.Integer(string='Offers', compute='_compute_offer_count')

    def _compute_offer_count(self):
        """Compute the offer count"""
        for rec in self:
            rec.offer_count = (self.env['property.rent.lease'].
            search_count(
                [('property_orderline_ids.property_id.id', '=', self.id)])
            )

    _sql_constraints = [
        ('check_price', 'check(price > 0)', 'price should be a positive value'),
        ('check_rent', 'check(rent > 0)', 'rent should be a positive value')
    ]

    def unlink(self):
        """Overrides the unlink method to handle property-specific cleanup"""
        for rec in self:
            property_lines = self.env['property.orderline'].search([('property_id', '=', rec.id)])
            for property_line in property_lines:
                data = property_line.rent_lease_id.property_orderline_ids
                if len(data) == 1:
                    temp = property_line.rent_lease_id
                    property_line.unlink()
                    temp.unlink()
                else:
                    property_line.unlink()
        return super().unlink()

    def action_get_rentorlease_record(self):
        """Fetch the rent or lease records"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Rent or lease',
            'view_mode': 'list,form',
            'res_model': 'property.rent.lease',
            'domain': [('property_orderline_ids.property_id.id', '=', self.id)],
        }
