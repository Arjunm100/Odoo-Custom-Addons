# -*- coding: utf-8 -*-

"""This models extends the 'purchase.order.line' model to include fields brand_id and tolerance"""

from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    """Extends the 'purchase.order.line' model to include fields brand_id and tolerance"""
    _inherit = 'purchase.order.line'

    brand_id = fields.Many2one('product.brand',
                               string='Brand', related='product_id.brand_id')
    tolerance = fields.Float('Tolerance', readonly=True)

    @api.model
    def _prepare_purchase_order_line_from_procurement(self, product_id, product_qty, product_uom, location_dest_id,
                                                      name, origin, company_id, values, po):
        """This method extends the base implementation to include additional fields in the purchase order line,
        specifically the 'tolerance' field, which is retrieved from the associated sale order line."""
        data = super()._prepare_purchase_order_line_from_procurement(product_id,product_qty,product_uom,
                                                                     location_dest_id,name, origin,
                                                                     company_id, values, po)
        data['tolerance'] = (self.env['sale.order.line'].
                             browse(values.get('sale_line_id')).tolerance)
        return data
