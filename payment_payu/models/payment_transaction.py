
from odoo import _, models
from werkzeug import urls
import urllib.parse
# from odoo.exceptions import ValidationError
from odoo.addons.payment_payu.controllers.main import PayuController
import hashlib

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'payu':
            return res
        payload = self._payu_prepare_payment_request_payload()
        # payment_data = self.provider_id._payu_make_request('/payments',data=payload)
        return {'api_url':'https://test.payu.in/_payment','url_params':payload}

    def _payu_prepare_payment_request_payload(self):
        base_url = self.provider_id.get_base_url().replace("http://", "")
        redirect_url = urls.url_join(base_url, PayuController._return_url)
        key = self.provider_id.payu_api_key  # PayU Merchant Key
        txnid = self.reference  # Transaction ID
        productinfo = "apple"  # Product Name
        amount = self.amount  # Payment Amount
        email = self.partner_email  # Customer Email
        firstname = self.partner_name  # Customer First Name
        surl = redirect_url  # Success URL
        furl = base_url  # Failure URL
        phone = self.partner_phone  # Customer Phone Number
        salt = self.provider_id.payu_salt
        print(salt)
        # hash_string = f"{key}|{txnid}|{amount}|{productinfo}|{firstname}|{email}|{udf1}|{udf2}|{udf3}|{udf4}|{udf5}||||||{salt}"
        hash_value = hashlib.sha512(f"{key}|{txnid}|{amount}|{productinfo}|{firstname}|{email}|||||||||||{salt}".encode('utf-8')).hexdigest()
        return {
            'key':key,
            'txnid':txnid,
            'productinfo':productinfo,
            'amount': amount,
            'email': email,
            'firstname':firstname,
            'surl': surl,
            'furl': furl,
            'phone':phone,
            'hash':hash_value
        }
        # return urllib.parse.urlencode({
        #     'key':key,
        #     'txnid':txnid,
        #     'productinfo':productinfo,
        #     'amount': amount,
        #     'email': email,
        #     'firstname':firstname,
        #     'surl': surl,
        #     'furl': furl,
        #     'phone':phone,
        #     'hash':hash_value
        # })

