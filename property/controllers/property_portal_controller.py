# -*- coding: utf-8 -*-

"""
This module extends the Odoo Customer Portal to provide additional functionalities for managing property rental and
lease orders."""

from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class PropertyCustomerPortal(CustomerPortal):
    """Customer portal extension for managing property rental and lease orders.This class extends the Odoo
    CustomerPortal to add functionalities related to property rental management."""

    def _prepare_home_portal_values(self, counters):
        """Prepare and return the portal home values including the count of rental properties"""
        values = super()._prepare_home_portal_values(counters)
        if 'portal_property' in counters:
            user_id = request.session.uid
            tenant_id = request.env['res.users'].browse(user_id).partner_id.id
            values['portal_property'] = (request.env['property.rent.lease'].sudo().
                                         search_count([('tenant_id', '=', tenant_id)]))
        return values

    @http.route(['/my/property'], type='http', auth="user", website=True)
    def portal_property_orders(self):
        """Render the portal page displaying the logged-in user's property rental orders.
          :return: Rendered template for displaying property rental orders."""
        user_id = request.session.uid
        tenant_id = request.env['res.users'].browse(user_id).partner_id.id
        orders = request.env['property.rent.lease'].sudo().search([('tenant_id', '=', tenant_id)])
        return request.render('property.portal_my_home_property_views', {'orders': orders, 'page_name': 'property'})

    @http.route(['/my/property/<int:order_id>'], type='http', auth="public", website=True)
    def portal_my_order(self, order_id=None):
        """Display the details of a specific property rental order."""
        order = request.env['property.rent.lease'].sudo().browse(order_id)
        return request.render('property.property_order_portal_content', {'order': order, 'page_name': 'property_order'})

    @http.route('/thank-you/<int:order_id>', auth="public", website=True)
    def page_thank_you(self, order_id):
        """Display the thank-you page"""
        order = request.env['property.rent.lease'].sudo().browse(order_id)
        return request.render('property.thank_you_template', {'order': [order.id, order.sequence]})
