# -*- coding: utf-8 -*-
{
    'name':'Property',
    'version':'18.0.3.0.0',
    'application': True,
    'depends':['mail','account', 'website'],
    'data':
    [
        'security/property_security.xml',
        'security/property_groups.xml',
        'security/ir.model.access.csv',

        'report/report_paperformat.xml',
        'report/ir_actions_report.xml',
        'report/ir_actions_report_templates.xml',

        'data/ir_cron_data.xml',
        'data/ir_sequence_data.xml',
        'data/property_email_templates.xml',
        'data/property_management_data.xml',
        'data/property_facility_data.xml',

        'wizard/order_report_wizard_views.xml',

        'views/property_portal_templates.xml',
        'views/property_website_views.xml',
        'views/property_management_views.xml',
        'views/property_rent_lease_views.xml',
        'views/property_facility_views.xml',
        'views/account_move_views.xml',
        'views/res_partner_views.xml',
        'views/property_snippet_views.xml',
        'views/property_information_views.xml',
        'views/property_management_menus.xml',
    ],
    'assets' : {
        'web.assets_backend':[
            'property/static/src/js/property_xlsx_report.js',
        ],
        'web.assets_frontend':[
            'property/static/src/css/property.css',
            'property/static/src/js/property_management.js',
            'property/static/src/xml/property_snippet_template.xml',
            'property/static/src/js/property_snippet.js'
        ]
    }
}