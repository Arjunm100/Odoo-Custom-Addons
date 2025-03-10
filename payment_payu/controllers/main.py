# -*- coding: utf-8 -*-

"""Module for handling PayU payment return callbacks in Odoo"""

from odoo import http
from odoo.http import request

class PayuController(http.Controller):
    """Controller for handling PayU payment gateway return URLs."""
    _return_url = '/payment/payu/return'

    @http.route(
        _return_url, type='http', auth='public', methods=['GET', 'POST'], csrf=False,
        save_session=False
    )
    def payu_return_from_checkout(self, **data):
        """Handles the PayU payment return callback"""
        request.env['payment.transaction'].sudo()._handle_notification_data('payu', data)
        return request.redirect('/payment/status')
