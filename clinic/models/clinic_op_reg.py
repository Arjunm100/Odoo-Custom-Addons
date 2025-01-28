from email.policy import default

from odoo import fields,models,api
from odoo.exceptions import ValidationError

class ClinicOpReg(models.Model):
    _name = 'clinic.op.reg'
    _description = 'Op Registration'
    _rec_name = 'serial_no'

    serial_no = fields.Char(string="Serial No",required=True,default=lambda self: ("New"),copy=False,readonly=True)
    patient_name = fields.Many2one(comodel_name='clinic.test',required = True,string = "Patient Name")
    patient_age = fields.Integer(string="Patient Age",related = 'patient_name.age')
    patient_gender = fields.Selection(string="Patient Gender",related = 'patient_name.gender')
    doctor = fields.Many2one(comodel_name='hr.employee',string="Doctor")
    op_date = fields.Datetime(string="Date",default = fields.Datetime.now)
    op_fee = fields.Monetary(string="Consultation fee",related = 'doctor.hourly_cost',currency_field = 'currency_id')
    token_no = fields.Integer(string = "token Number")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one(comodel_name='res.currency', default=lambda self:self.env.user.company_id.currency_id.id)
    _sql_constraints = [('check_serial_no','unique(serial_no)','serial number must be unique'),
                        ('check_token_no','unique(token_no)','token number should be unique')]

    @api.constrains("op_fee")
    def _check_fee(self):
        for record in self:
            if record.op_fee < 0:
                raise ValidationError('Fee should be a postive value')

    @api.depends_context('company')
    @api.depends('company_id')
    def _compute_currency_id(self):
        for record in self:
            record.currency_id = record.company_id.currency_id or self.env.company.currency_id

    @api.model
    def create(self,vals_list):
        vals_list['serial_no'] = self.env['ir.sequence'].next_by_code('clinic.op.reg')
        return super().create(vals_list)





