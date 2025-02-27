# -*- coding: utf-8 -*-
# import logging
# import pprint
#
# import requests
# from werkzeug import urls

from odoo import _, fields, models

# _logger = logging.getLogger(__name__)

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('payu', 'payU')], ondelete={'payu': 'set default'}
    )
    payu_api_key = fields.Char(
        string="PayU API Key",
        help="The Test or Live API Key depending on the configuration of the provider",
        required_if_provider="payu", groups="base.group_system"
    )

    def _get_default_payment_method_codes(self):
        """ Override of `payment` to return the default payment method codes. """
        default_codes = super()._get_default_payment_method_codes()
        if self.code != 'payu':
            return default_codes
        return {'ideal', 'amex', 'card', 'discover', 'visa', 'mastercard'}