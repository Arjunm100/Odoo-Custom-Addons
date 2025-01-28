from email.policy import default

from odoo import api,fields,models

class ClinicConsultation(models.Model):
    _name = 'clinic.consultation'
    _description = 'Consultation'
    _rec_name = 'consultation_no'

    op_ticket_id = fields.Many2one(comodel_name='clinic.op.reg',string="Op ticket id")
    op_patient = fields.Many2one(string="Patient Name",related = 'op_ticket_id.patient_name')
    op_doctor = fields.Many2one(string="Doctor",related = 'op_ticket_id.doctor')
    op_patient_age = fields.Integer(string="Patient Age",related = 'op_patient.age')
    op_patient_gender = fields.Selection(string="Patient Age",related = 'op_patient.gender')
    op_patient_blood = fields.Selection(string="blood group",related = 'op_patient.bloodgroup')
    consultation_time = fields.Date(string='Consultation time',default = fields.Datetime.now)
    consultation_no = fields.Char(string='Serial No',default=lambda self: ("new"),readonly=True,copy=False)
    weight = fields.Integer(string='Weight')
    spo2 = fields.Integer(string='SPO2')
    bp = fields.Char(string="Blood pressure")
    temperature = fields.Integer(string="Temperature")
    diognosys = fields.Text(string="Diognosys")
    medcine = fields.One2many(string="Medcine",comodel_name="clinic.priscription",inverse_name="consult_id")

    @api.model
    def create(self,vals_list):
        vals_list['consultation_no'] = self.env['ir.sequence'].next_by_code('clinic.consultation')
        return super().create(vals_list)

