from dateutil.utils import today
from odoo.exceptions import ValidationError
from odoo.tools import date_utils

from odoo import fields,models,api

class Property(models.Model):
    _name = 'estate.property'
    _description = 'property details'

    name = fields.Char(required=True,string="Name of the Property",help="Name of the property")
    description = fields.Text(string="Description")
    postcode = fields.Char(string='postcode')
    date = fields.Date(required=True,string='Date',default=date_utils.add(today(),months=3),copy=False)
    expectedprice = fields.Float(string='Expected price')

    sellingprice = fields.Float(readonly=True,string='selling price',copy=False)
    bedrooms = fields.Integer(string='number of bedrooms',default=2)
    livingarea = fields.Integer(string='living area')
    facades = fields.Integer(string='facades')
    garage = fields.Boolean(string='garage')
    gardenarea = fields.Integer(string='Garden Area')
    gardenorientation = fields.Selection(string='orientation',selection=[
        ('west','West'),('east','East'),('south','South'),('north','North')
    ])
    status = fields.Selection(string='status',selection=[
        ('new','New'),
        ('offer_recieved','Offer recieved'),
        ('offer_accepted','Offer accepted'),
        ('sold','Sold'),
        ('cancelled','Cancelled')],
        copy=False,default='new',readonly=True)
    propertytype = fields.Many2one("estate.property.type", string="Property type")
    buyer = fields.Many2one('res.partner',copy=False,readonly=True)
    salesperson = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True, default=lambda self: self.env.user)
    tag = fields.Many2many(comodel_name='estate.property.tag',string='Tags')
    offer = fields.One2many(string='offers',comodel_name='estate.property.offer',inverse_name='propertyId')
    totalarea = fields.Float(compute='_computetotalarea')
    garden = fields.Boolean(string='Garden')
    bestoffer = fields.Float(string="Best offer",compute="_computebestoffer")
    sellingpricebackup = fields.Float(string="hi")
    _sql_constraints = [('check_expectedprice','check(expectedprice > 0)','selling price should be a positive value'),
                        ('check_uniquename','unique(name)','Name should be unique')]


    @api.depends("gardenarea","livingarea")
    def _computetotalarea(self):
        for record in self:
            record.totalarea = record.gardenarea + record.livingarea
    @api.onchange('garden')
    def _gardenonchange(self):
        if self.garden:
            self.gardenarea,self.gardenorientation = 10,'east'
        else:
            self.gardenorientation = self.gardenarea = None

    @api.depends("offer")
    def _computebestoffer(self):
        for record in self:
            record.bestoffer = max(record.offer.mapped('price')) if record.offer else 0

    def propertysold(self):
        for record in self:
            print(record)
            if record.status != 'cancelled':
                if not record.offer:
                    raise ValidationError("No Active offers for this property")
                else:
                    if 'accepted' not in record.offer.mapped('status'):
                        raise ValidationError("No offers were accepted for this property")
                    else:
                        record.status = 'sold'
            elif record.status == 'cancelled':
                raise ValidationError("Property already cancelled")


    def propertycancelled(self):
        for record in self:
            if record.status != 'sold':
                record.status = 'cancelled'
            elif record.status == 'sold':
                raise ValidationError("Property already Sold")

    def propertyreset(self):
        for record in self:
            record.status = 'new'

    @api.constrains("sellingpricebackup")
    def _selling_price_check(self):
        for record in self:
            if (record.sellingpricebackup/record.expectedprice) < 0.90:
                raise ValidationError(f'Selling price({record.sellingpricebackup}) should be greater than 90% of expected price({record.expectedprice})')



















