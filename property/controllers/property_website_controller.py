# -*- coding: utf-8 -*-

"""This module defines a web controller for managing property rentals on the Odoo website.It provides endpoints for
rendering available properties and submitting property rental orders."""

from odoo.http import request, Controller, route
from odoo import fields


class PropertyWebContoller(Controller):
    """A web controller for handling property rental forms on the Odoo website.

    This class provides routes for:
    - Rendering a property listing page.
    - Submitting a property rental or lease request."""

    @route('/property', auth='public', website=True)
    def render_property_page(self, **kwargs):
        """Render the property order page"""
        properties_data = request.env['property.management'].sudo().search([('status', '=', 'draft')])
        properties = {}
        [properties.update({rec.id: [rec.id, rec.name, rec.rent_amount, rec.lease_amount]}) for rec in properties_data]
        values = {'properties': properties}
        return request.render('property.web_form_template', values)

    @route('/property/submit', type='json', auth='public', website=True, methods=['POST'], csrf=False)
    def property_order_submit(self, actions):
        """Create property order on backend when submission of order through webpage"""
        order = request.env['property.rent.lease'].sudo().create({
            'tenant_id': request.env['res.users'].browse(request.session.uid).partner_id.id,
            'start_date': fields.Datetime.to_datetime(actions.get('start_date')),
            'end_date': fields.Datetime.to_datetime(actions.get('end_date')),
            'rent_lease': actions.get('order_type'),
            'due_date': fields.Datetime.to_datetime(actions.get('start_date')),
            'property_orderline_ids': [fields.Command.create({
                'property_id': property
            }) for property in actions['properties']]})
        return order.id
