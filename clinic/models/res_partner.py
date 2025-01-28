from email.policy import default

from odoo import fields,models,api
from odoo.exceptions import ValidationError
from odoo.tools import date_utils


class ResPartner(models.Model):
    _name = 'clinic.test'
    _inherits = {'res.partner':'partner_id'}

    partner_id = fields.Many2one('res.partner')
    age = fields.Integer(string='Age',compute='_computeage',readonly=False,store=True)
    date_of_birth = fields.Date(string='Date of Birth',default=fields.date.today())
    gender = fields.Selection(string="Gender",selection=[
        ('male','Male'),('female','Female')
    ])
    seq_id = fields.Char(string="ID",required=True,readonly=True,default = lambda self: ("new"))
    bloodgroup = fields.Selection(string='Blood Group',selection=[
        ('a+ve','A+ve'),('a-ve','A-ve'),('b+ve','B+ve'),('ab+ve','AB+ve'),('ab-ve','AB-ve'),('o+ve','O+ve'),('o-ve','O-ve')
    ])

    _sql_constraints = [('check_id','unique(seq_id)','Id should be unique')]

    @api.depends('date_of_birth')
    def _computeage(self):
        for record in self:
            if fields.date.today() and record.date_of_birth:
                age = (fields.date.today() - record.date_of_birth).days
                record.age = int(age/365)
            else:
                record.age = False

    @api.model
    def create(self, vals_list):
        vals_list['seq_id'] = self.env['ir.sequence'].next_by_code('clinic.test')
        return super().create(vals_list)

    @api.onchange("gender")
    def onchange_x(self):
        print(self.email)


