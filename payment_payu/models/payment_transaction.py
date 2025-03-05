
from odoo import _, models
from werkzeug import urls
import ngrok
import urllib.parse
# from odoo.exceptions import ValidationError
from odoo.addons.payment_payu.controllers.main import PayuController
import hashlib
from odoo.exceptions import ValidationError

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'payu':
            return res
        payload = self._payu_prepare_payment_request_payload()
        # payment_data = self.provider_id._payu_make_request('/payments',data=payload)
        # Establish connectivity
        return {'api_url':'https://test.payu.in/_payment','url_params':payload}

    def _payu_prepare_payment_request_payload(self):
        # listener = ngrok.forward(8018, authtoken="2ttIGSR0KtrqEikJwigt19c4Vxh_6KLa7ArbnoXZnTSrSTHPt")
        base_url = 'https://b1d7-103-139-64-225.ngrok-free.app'
        redirect_url = urls.url_join(base_url, PayuController._return_url)
        key = self.provider_id.payu_api_key  # PayU Merchant Key
        txnid = self.reference  # Transaction ID
        productinfo = "apple"  # Product Name
        amount = self.amount  # Payment Amount
        email = self.partner_email  # Customer Email
        firstname = self.partner_name  # Customer First Name
        surl = redirect_url  # Success URL
        furl = '/localhost:8018'  # Failure URL
        phone = self.partner_phone  # Customer Phone Number
        salt = self.provider_id.payu_salt
        print(salt)
        print(key)
        # hash_string = f"{key}|{txnid}|{amount}|{productinfo}|{firstname}|{email}|{udf1}|{udf2}|{udf3}|{udf4}|{udf5}||||||{salt}"
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
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'payu' or len(tx) == 1:
            print('cat20')
            return tx
        print('cat21')
        tx = self.search(
            [('reference', '=', notification_data.get('txnid')), ('provider_code', '=', 'payu')]
        )
        print('cat22',tx)
        if not tx:
            raise ValidationError("PayU: " + _(
                "No transaction found matching reference %s.", notification_data.get('ref')
            ))
        return tx

    def _process_notification_data(self, notification_data):
        super()._process_notification_data(notification_data)
        if self.provider_code != 'payu':
            return
        print('cat101')
        if notification_data['status'] == 'success':
            self._set_done()
        elif notification_data.get('status') == 'failure':
            self._set_canceled("")




