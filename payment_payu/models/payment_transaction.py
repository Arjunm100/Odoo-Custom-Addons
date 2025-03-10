# -*- coding: utf-8 -*-

"""Module for handling PayU payment transactions in Odoo"""

from odoo import _, models
from werkzeug import urls
from odoo.addons.payment_payu.controllers.main import PayuController
import hashlib
from odoo.exceptions import ValidationError
import datetime
import random
import subprocess

class PaymentTransaction(models.Model):
    """Extension of the payment transaction model to support PayU payments."""
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        """Retrieves the specific rendering values required for PayU transactions"""
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'payu':
            return res
        payload = self._payu_prepare_payment_request_payload()
        return {'api_url':'https://test.payu.in/_payment','url_params':payload}

    def _payu_prepare_payment_request_payload(self):
        """Prepares the payload for the PayU payment request"""
        base_url = subprocess.check_output(
            "curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url'",
            shell=True,
            text=True
        ).strip()
        redirect_url = urls.url_join(base_url, PayuController._return_url)
        key = self.provider_id.payu_api_key
        txnid = self.generate_transaction_id()
        productinfo = self.reference
        amount = self.amount
        email = self.partner_email
        firstname = self.partner_name
        phone = self.partner_phone
        salt = self.provider_id.payu_salt
        hash_value = hashlib.sha512(f"{key}|{txnid}|{amount}|{productinfo}|{firstname}|{email}|||||||||||{salt}".encode('utf-8')).hexdigest()
        return {
            'key':key,
            'txnid':txnid,
            'productinfo':productinfo,
            'amount': amount,
            'email': email,
            'firstname':firstname,
            'surl': redirect_url,
            'furl': redirect_url,
            'phone':phone,
            'hash':hash_value
        }

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """Retrieves the transaction based on notification data received from PayU"""
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'payu' or len(tx) == 1:
            return tx
        tx = self.search(
            [('reference', '=', notification_data.get('productinfo')), ('provider_code', '=', 'payu')]
        )
        if not tx:
            raise ValidationError("PayU: " + _(
                "No transaction found matching reference %s.", notification_data.get('ref')
            ))
        return tx

    def _process_notification_data(self, notification_data):
        """Processes the notification data received from PayU"""
        super()._process_notification_data(notification_data)
        if self.provider_code != 'payu':
            return
        if notification_data['status'] == 'success':
            self._set_done()
            self.provider_reference = notification_data.get('mihpayid')
        elif notification_data.get('status') == 'failure':
            self._set_canceled(f"PayU : {notification_data.get('error_Message')}")

    def generate_transaction_id(self):
        """Generates a unique transaction ID"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        random_number = random.randint(10000, 99999)
        transaction_id = f"SO{timestamp}{random_number}"
        return transaction_id




