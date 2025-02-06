# -*- coding: utf-8 -*-

"""Module for managing property rent  lease orders"""
from email.policy import default

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class PropertyRentLease(models.Model):
    """Represent a property rent or lease order"""
    _name = "property.rent.lease"
    _description = "Rent or Lease Management"
    _rec_name = 'sequence'
    _inherit = "mail.thread"

    sequence = fields.Char(string='Sequence', default=lambda self: "New", readonly=True)
    tenant_id = fields.Many2one(string='Tenant', comodel_name='res.partner', required=True)
    rent_lease = fields.Selection(string='Rent or Lease?', selection=[
        ('rent', 'Rent'), ('lease', 'Lease')], required=True, default='rent')
    company_id = fields.Many2one(string='Company', comodel_name='res.company',
                                 default=lambda self: self.env.company.id)
    currency_id = fields.Many2one(string='Currency', comodel_name='res.currency',
                                  default=lambda self: self.env.company.currency_id.id)
    start_date = fields.Datetime(string='Start Date', required=True, default=fields.Datetime.now)
    end_date = fields.Datetime(string='End Date', required=True)
    due_date = fields.Datetime(string='Due Date', required=True,default=fields.Datetime.now())
    days_count = fields.Float(string='Rent Period(Days)',compute='_compute_days_count')
    stages = fields.Selection(selection=[
        ('draft', 'Draft'), ('confirmed', 'Confirmed'), ('close', 'Close'),
        ('return', 'Return'), ('expired', 'Expired'),
    ], tracking=True, default='draft',copy=False)
    property_orderline_ids = fields.One2many(comodel_name='property.orderline',
                                             inverse_name='rent_lease_id',
                                             domain="[('property_id.status','=','draft')]",copy=True)
    grand_total = fields.Monetary(string='Grand Total', compute='_compute_grand_total')
    invoice_count = fields.Integer('Invoices', compute='_compute_invoice_count')
    invoice_status = fields.Selection(selection=[('not_invoiced', 'Not Invoiced'),
                                                 ('invoiced', 'Invoiced'),
                                                 ('partial', 'Partially Paid'),
                                                 ('full', 'Fully Paid')],
                                      readonly=True, compute='_compute_invoice_status')

    @api.depends('start_date', 'end_date')
    def _compute_days_count(self):
        """Compute days count"""
        for rec in self:
            if rec.start_date and rec.end_date:
                rec.days_count = (
                    abs(round(((rec.end_date - rec.start_date).total_seconds()) / 86400, 2))
                )
            else:
                rec.days_count = 0.0

    def _compute_invoice_count(self):
        """Compute invoice count"""
        self.invoice_count = (self.env['account.move'].
                              search_count([('rent_lease_order_id', '=', self.id)]))

    @api.depends('property_orderline_ids.total_amount', 'property_orderline_ids')
    def _compute_grand_total(self):
        """Compute grand total"""
        for rec in self:
            if rec.property_orderline_ids:
                rec.grand_total = sum(rec.property_orderline_ids.mapped('total_amount'))
            else:
                rec.grand_total = 0

    @api.depends('property_orderline_ids.quantity_invoiced')
    def _compute_invoice_status(self):
        """Compute invoice status"""
        for rec in self:
            if rec.property_orderline_ids and rec.stages != 'draft':
                invoiced_lines = (rec.property_orderline_ids.
                                  filtered(lambda r: r.invoice_line_ids))
                if invoiced_lines:
                    line_invoice_state = invoiced_lines.mapped('line_invoice_state')
                    if all(i == 'paid' for i in line_invoice_state):
                        if len(line_invoice_state) == len(rec.property_orderline_ids):
                            rec.invoice_status = 'full'
                        else:
                            rec.invoice_status = 'partial'
                    else:
                        if ('partial_paid' in line_invoice_state or
                                len(set(line_invoice_state)) != 1):
                            rec.invoice_status = 'partial'
                        else:
                            rec.invoice_status = 'invoiced'
                else:
                    rec.invoice_status = 'not_invoiced'
            else:
                rec.invoice_status = None

    @api.constrains('end_date', 'due_date')
    def _check_end_date(self):
        if self.start_date:
            if self.start_date > self.end_date:
                raise ValidationError('The End date cannot be later than the start date.')
            if self.start_date > self.due_date:
                raise ValidationError('The Due date cannot be later than the start date.')

    _sql_constraints = [
        ('check_amount', 'check(amount>0)', 'Amount should be greater than zero')]

    @api.onchange('end_date')
    def _onchange_due_date_validation(self):
        self.due_date = self.end_date

    @api.model
    def create(self, vals_list):
        """create record with sequence"""
        vals_list['sequence'] = self.env['ir.sequence'].next_by_code('property.rent.lease')
        return super().create(vals_list)

    def action_draft(self):
        """set the stage to draft"""
        self.write({'stages': 'draft'})
        self.property_orderline_ids.mapped('property_id').write({'status': 'draft'})

    def action_confirm(self):
        """set the stage to confirm"""
        if (self.env['ir.attachment'].
                search([('res_model', '=', 'property.rent.lease'),
                        ('res_id', '=', self.id)])):
            self.write({'stages': 'confirmed'})
            self.property_orderline_ids.property_id. \
                status = 'rented' if self.rent_lease == 'rent' else 'leased'
            template = self.env.ref('property.email_template_property_order_confirm')
            template.send_mail(self.id, force_send=True)
        else:
            raise ValidationError('Attachments needed to confirm')

    def action_close(self):
        """set the stage to close"""
        for rec in self:
            rec.property_orderline_ids.mapped('property_id').write({'status': 'draft'})
            rec.write({'stages': 'close'})
            template = self.env.ref('property.email_template_property_order_close')
            template.send_mail(rec.id, force_send=True)

    def action_return(self):
        """set the stage to return"""
        self.property_orderline_ids.mapped('property_id').write({'status': 'draft'})
        self.write({'stages': 'return'})

    def action_create_invoice(self):
        """Create or Manipulate Invoice"""
        for line in (self.property_orderline_ids.
                filtered(lambda r: r.quantity_invoiced != self.days_count)):
            invoices = (self.
                        property_orderline_ids.invoice_line_ids.mapped('move_id').
                        filtered(
                lambda r: r.state == 'draft').ids)
            if not line.invoice_line_ids:
                if not invoices:
                    self._invoice_line_creation(invoice=self.invoice_creation(),
                                                line=line, quantity=self.days_count)
                else:
                    self._invoice_line_creation(invoice=self.env['account.move'].
                                                browse(invoices[0]),
                                                line=line, quantity=self.days_count)
            else:
                quantity_invoiced = (line.invoice_line_ids.
                filtered(lambda r: r.move_id.state == 'posted').mapped(
                    'quantity'))
                draft_inv_line = (line.invoice_line_ids.
                                  filtered(lambda r: r.move_id.state == 'draft'))

                if sum(quantity_invoiced) < self.days_count:
                    if draft_inv_line:
                        draft_inv_line[0].write({
                            'quantity': self.days_count - line.quantity_invoiced
                        })
                    else:
                        if not invoices:
                            self._invoice_line_creation(invoice=self.invoice_creation(),
                                                        line=line,
                                                        quantity=self.days_count - sum(
                                                            quantity_invoiced))
                        else:
                            self._invoice_line_creation(invoice=self.env['account.move'].
                                                        browse(invoices[0]),
                                                        line=line,
                                                        quantity=self.days_count - sum(
                                                            quantity_invoiced))

    def action_cron_date_validation(self):
        for record in self.search([]):
            if record.end_date < fields.Datetime.now() and record.stages == 'confirmed':
                record.update({'stages':'expired'})
                template = record.env.ref('property.email_template_property_order_expired')
                template.send_mail(record.id, force_send=True)
            if (record.due_date < fields.Datetime.now()
                    and record.stages != 'draft'
                    and record.invoice_status != 'full'):
                template = record.env.ref('property.email_template_property_order_follow_up')
                template.send_mail(record.id, force_send=True)

    def action_get_invoices_record(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'view_mode': 'list,form',
            'res_model': 'account.move',
            'domain': [('rent_lease_order_id', '=', self.id)],
        }

    def _invoice_line_creation(self, line, invoice, quantity):
        invoice_lines = self.env['account.move.line'].create({
            'name': line.property_id.name,
            'quantity': quantity,
            'price_unit': line.amount,
            'move_id': invoice.id
        })
        line.write({
            'invoice_line_ids': [(fields.Command.link(invoice_lines.id))]
        })

    def invoice_creation(self):
        vals = {
            'move_type': 'out_invoice',
            'currency_id': self.currency_id.id,
            'partner_id': self.tenant_id.id,
            'invoice_origin': self.sequence,
            'invoice_user_id': self.env.user.id,
            'company_id': self.company_id.id,
            'rent_lease_order_id': self.id
        }
        record = self.env['account.move'].create(vals)
        log_message = _("%(name)s is generated in %(order)s",
                        name=(record.name if record.name else 'Draft Invoice'),
                        order=record._get_html_link(),
                        )
        self.message_post(body=log_message)
        return record
