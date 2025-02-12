# -*- coding: utf-8 -*-

"""This module customizes the shopping cart behavior by adding BOM (Bill of Materials)
products to the cart's context based on a system parameter."""

from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSaleInherit(WebsiteSale):
    """Inherits the WebsiteSale controller to include additional BOM products in the response context."""
    @http.route(['/shop/cart'], type='http', auth="public", website=True, sitemap=False)
    def cart(self, access_token=None, revive='', **post):
        """Overrides the cart method to include BOM products in the cart context."""
        res= super().cart(access_token,revive,**post)
        select_products = http.request.env['ir.config_parameter'].sudo().get_param('cart_bom_products')
        res.qcontext.update({'bom_cart_products':eval(select_products)})
        return res