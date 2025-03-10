# -*- coding: utf-8 -*-

"""Module for integrating PayU as a payment provider in Odoo."""

from odoo import _, fields, models


class PaymentProvider(models.Model):
    """ Extension of the payment provider model to support PayU"""
    _inherit = 'payment.provider'
    code = fields.Selection(
        selection_add=[('payu', 'payU')], ondelete={'payu': 'set default'}
    )
    payu_api_key = fields.Char(
        string="PayU API Key",
        help="The Test or Live API Key depending on the configuration of the provider",
        required_if_provider="payu", groups="base.group_system"
    )
    payu_salt = fields.Char(
        string="Salt Code",
        required_if_provider="payu", groups="base.group_system"
    )

    def _get_default_payment_method_codes(self):
        """Returns the default payment method codes."""
        default_codes = super()._get_default_payment_method_codes()
        if self.code != 'payu':
            return default_codes
        return {'payu'}
