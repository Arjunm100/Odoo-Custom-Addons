# -*- coding: utf-8 -*-
{
    'name':'Product Fields',
    'version':'18.0.0.0.0',
    'application': True,
    'depends':['mail','account','product','stock','sale_purchase'],
    'data' : [
        'security/ir.model.access.csv',
        'data/product_brand_data.xml',
        'views/product_template_views.xml',
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
        'views/res_partner_views.xml',
        'views/stock_picking_views.xml',
        'wizard/stock_picking_wizard_views.xml',
        'wizard/order_line_import_views.xml',
        'views/product_brand_views.xml'
    ]
}