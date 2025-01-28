# -*- coding: utf-8 -*-

"""Module for managing order lines"""
from odoo import api, fields, models


class PropertyOrderline(models.Model):
    """Represent a order line associated with rent or lease orders"""
    _name = 'property.orderline'
    _description = 'Property Orderlines'

    property_id = fields.Many2one(string='Property',
                                  comodel_name='property.management', required=True)
    rent_lease_id = fields.Many2one(string='Rent or lease reference',
                                    comodel_name='property.rent.lease',
                                    required=True,copy=False)
    currency_id = fields.Many2one(comodel_name='res.currency',
                                  default=lambda self: self.env.company.currency_id.id,
                                  copy=False)
    amount = fields.Monetary(string='amount', compute='_compute_amount',
                             inverse='_inverse_amount', store=True,
                             copy=False)
    total_amount = fields.Monetary(string='Total', compute='_compute_total_amount',
                                   copy=False)
    invoice_line_ids = fields.Many2many(string='Invoice lines',
                                        comodel_name='account.move.line',
                                        relation='oderline_line_invoice_rel',
                                        column1='orderline_id', column2='invoiceline_id',
                                        copy=False)
    quantity_invoiced = fields.Float(string='Invoiced Quantity',
                                     compute='_compute_invoiced_lines',
                                     copy=False)
    line_invoice_state = fields.Selection(selection=[
        ('partial_paid', 'Partial_paid'), ('paid', 'Paid'), ('not_invoiced', 'Not Invoiced')
    ], default='not_invoiced', compute='_compute_line_inv_stat',copy=False)

    @api.depends('quantity_invoiced')
    def _compute_line_inv_stat(self):
        for record in self:
            paid_line = (record.invoice_line_ids.
                         filtered(lambda r: r.move_id.status_in_payment == 'paid').
                         mapped('quantity'))
            if paid_line:
                if sum(paid_line) != record.rent_lease_id.days_count:
                    record.line_invoice_state = 'partial_paid'
                else:
                    record.line_invoice_state = 'paid'
            else:
                record.line_invoice_state = 'not_invoiced'

    @api.depends('rent_lease_id.rent_lease', 'property_id')
    def _compute_amount(self):
        """Compute the amount in a order line"""
        for rec in self:
            if rec.rent_lease_id and rec.property_id:
                if rec.rent_lease_id.rent_lease == 'rent':
                    rec.amount = rec.property_id.rent_amount
                else:
                    rec.amount = rec.property_id.lease_amount
            else:
                rec.amount = 0

    def _inverse_amount(self):
        """inverse function for _compute_amount"""
        for rec in self:
            if rec.amount and rec.property_id:
                if rec.rent_lease_id.rent_lease == 'rent':
                    rec.property_id.rent_amount = rec.amount
                else:
                    rec.property_id.lease_amount = rec.amount

    def _compute_invoiced_lines(self):
        """Compute the invoiced lines"""
        for record in self:
            record.quantity_invoiced = sum(record.invoice_line_ids.
                                           filtered(lambda r: r.move_id.state == 'posted').
                                           mapped('quantity'))

    @api.depends('amount', 'rent_lease_id.days_count')
    def _compute_total_amount(self):
        """Compute the total amount in invoiced lines"""
        for rec in self:
            rec.total_amount = rec.amount * abs(rec.rent_lease_id.days_count)
