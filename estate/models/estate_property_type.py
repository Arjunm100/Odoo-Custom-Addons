from odoo import models,fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = 'Create various type for properties'
    _rec_name = 'Type'

    Type = fields.Text(string='Property type',required=True)