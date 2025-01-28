# -*- coding: utf-8 -*-

"""Module for managing property facilities"""

from odoo import fields, models


class PropertyFacility(models.Model):
    """Represents a facility associated with a property"""
    _name = 'property.facility'
    _description = 'Property Facility'

    name = fields.Char(string="Facility Name", required=True)
