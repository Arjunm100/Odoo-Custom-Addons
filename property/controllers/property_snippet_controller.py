# -*- coding: utf-8 -*-

"""This module defines a controller for fetching and displaying dynamic property data in an Odoo-based web application.
 It provides endpoints to retrieve property records and render individual property pages."""

from odoo import http
from odoo.http import request


class DynamicSnippets(http.Controller):
    """This class is for the getting values for dynamic product snippets
      """

    @http.route('/latest-property', type='json', auth='public')
    def top_selling(self):
        """Function used to fetch property records and return to rpc request"""
        property = (request.env['property.management'].sudo().search_read([('status', '=', 'draft')],
                                                                          ['name', 'owner_id', 'rent_amount', 'price',
                                                                           'lease_amount'], order="id desc"))
        return property

    @http.route('/property-data/<int:property_id>', type='http', auth="public", website=True)
    def render_property_data(self, property_id):
        """Function used to render the property page"""
        property = request.env['property.management'].sudo().browse(property_id)
        return request.render('property.property_data_template', {'property': property})
