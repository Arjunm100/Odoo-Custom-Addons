from odoo import fields,models,api

class ClinicPriscription(models.Model):
    _name = 'clinic.priscription'
    _description = 'Priscription'

    consult_id = fields.Many2one(comodel_name='clinic.consultation',string='Consultation refference')
    op_id = fields.Many2one(string="Op refference",related='consult_id.op_ticket_id')
    patient = fields.Many2one(string="Patient Name",related='consult_id.op_patient')
    doctor = fields.Many2one(string='Doctor Name',related='consult_id.op_doctor')
    medcine = fields.Many2one(string='Medcine',comodel_name='product.template')
    quantity = fields.Float(string='Quantity')
    dose = fields.Char(string='Dosage')
    priscription_id = fields.Char(string='ID',default=lambda self: ("new"))

    @api.model
    def create(self, vals_list):
        vals_list['priscription_id'] = self.env['ir.sequence'].next_by_code('clinic.priscription')
        return super().create(vals_list)



