# -*- coding: utf-8 -*-

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

class PayuController(http.Controller):
    _return_url = '/payment/payu/return'

    @http.route(
        _return_url, type='http', auth='public', methods=['GET', 'POST'], csrf=False,
        save_session=False
    )
    def payu_return_from_checkout(self, **data):
        print('cat5')
        # request.env['payment.transaction'].sudo()._handle_notification_data('payu', data)
        return request.redirect('/payment/status')
