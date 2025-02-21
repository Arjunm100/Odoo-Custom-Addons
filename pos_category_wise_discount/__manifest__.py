# -*- coding: utf-8 -*-

{
    'name':'POS category wise discount',
    'version':'18.0.3.0.0',
    'application': True,
    'description': """This module allows to set category wise discount limit for product in POS""",
    'author': "Arjun M",
    'auto_install':False,
    'license':'LGPL-3',
    'installable':True,
    'depends':['product','point_of_sale'],
    'data':[
        'views/res_config_settings_views.xml'
    ],
    'assets': {
           'point_of_sale._assets_pos': [
                'pos_category_wise_discount/static/src/js/pos_store.js',]}
}