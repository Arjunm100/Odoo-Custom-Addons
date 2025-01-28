from email.policy import default

from dateutil.relativedelta import relativedelta

from odoo import fields,models,api
from dateutil.utils import today
from odoo.exceptions import ValidationError
from odoo.tools import date_utils



class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property offers'

    price = fields.Float(string="Price",required=True)
    status = fields.Selection(string='Offer status',
                              selection=[('accepted','Accepted'),('refused','Refused')],
                              copy=False,
                              readonly = True
                              )
    partnerId = fields.Many2one('res.partner',required=True,string='Buyer')
    propertyId = fields.Many2one(comodel_name='estate.property',required=True,string='Property')
    validity = fields.Integer(string='Validity')
    deadline = fields.Date(compute="_computeDeadline", inverse="_inversedeadline")
    createdDate = fields.Date(default=today())
    _sql_constraints = [('check_sellingprice','check(price > 0)','price should be a positive value')]


    @api.depends('validity', 'createdDate')
    def _computeDeadline(self):
        for record in self:
            record.deadline = date_utils.add(today(),days=record.validity)

    def _inversedeadline(self):
        for record in self:
            record.validity = (record.deadline - record.createdDate).days

    def offerAccept(self):
        for offer in self:
            if not offer.status:
                print(self.mapped('status'))
                if 'accepted' not in self.propertyId.offer.mapped('status'):
                    offer.status = 'accepted'
                    offer.propertyId.buyer = offer.partnerId
                    offer.propertyId.sellingprice = offer.price
                    offer.propertyId.sellingpricebackup = offer.price
                    self.propertystate()
                else:
                    raise ValidationError("Already a offer has been accepted")
            else:
                raise ValidationError("Offer already refused")

    def offerRefuse(self):
        for offer in self:
            if offer.status != 'accepted':
                offer.status = 'refused'
                self.propertystate()
            elif offer.status == 'accepted':
                raise ValidationError('Offer already accepted')


    def resettodraft(self):
        self.propertystate()
        for offer in self:
            offer.propertyId.sellingprice = offer.propertyId.buyer = offer.status = None


    def propertystate(self):
        for record in self:
            if record.propertyId.offer.mapped('status'):
                record.propertyId.status = 'offer_recieved'
                if 'accepted' in record.propertyId.offer.mapped('status'):
                    record.propertyId.status = 'offer_accepted'





