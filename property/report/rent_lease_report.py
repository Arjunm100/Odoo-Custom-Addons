# -*- coding: utf-8 -*-

"""This module defines an abstract model for generating Rent and Lease reports in the 'property' module. It provides
the necessary method to retrieve report data and associated documents for rendering the custom report templates."""

from odoo import api,models

class RentLeaseReport(models.AbstractModel):
    """Abstract model to handle the generation and rendering of Rent and Lease reports."""
    _name = "report.property.report_rent_lease"
    _description = "Rent or Lease order reports"

    @api.model
    def _get_report_values(self, docids, data=None):
        """Retrieves the data and documents required for generating the Rent and Lease report."""
        docs = self.env['property.rent.lease'].browse(docids)
        return {
            'docs': docs,
            'data': data['report'],
        }
