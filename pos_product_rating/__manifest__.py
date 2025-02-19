# -*- coding: utf-8 -*-

{
    'name':'POS Product Rating',
    'version':'18.0.3.0.0',
    'application': True,
    'description': """This module allows to rate product and display rating in POS""",
    'author': "Arjun M",
    'auto_install':False,
    'license':'LGPL-3',
    'installable':True,
    'depends':['product','point_of_sale'],
    'data':[
        'views/product_product_views.xml'
    ],
    'assets': {
       'point_of_sale._assets_pos': [
            'pos_product_rating/static/src/js/order_line.js',
            'pos_product_rating/static/src/js/pos_order_line.js',
            'pos_product_rating/static/src/xml/pos_product.xml',
            'pos_product_rating/static/src/xml/pos_orderline.xml'
       ]
    },
}