# -*- coding: utf-8 -*-

{
    'name': 'Payment Provider: payU',
    'version': '1.0',
    'category': 'Accounting/Payment Providers',
    'summary': "PayU is a global payment service provider offering online payment solutions in emerging markets",
    'description': " ",
    'author': 'Arjun M',
    'website': 'https://payu.in',
    'license': 'LGPL-3',
    'images': ['static/description/icon.png'],
    'depends': ['payment'],
    'data': [
        'data/payment_provider_data.xml',
        'views/payment_provider_views.xml'
    ]
}