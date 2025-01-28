from odoo import fields,models

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Create tags for the property'
    _rec_name = 'tag'

    tag = fields.Text(string="Name of the tag",required=True)
    _sql_constraints = [('check_uniquetag', 'UNIQUE(tag)', 'Tag should be unique')]