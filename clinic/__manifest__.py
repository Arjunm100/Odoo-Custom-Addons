{
    'name':'clinic',
    'version':'1.0',
    'application': True,
    'depends': ['base','hr','hr_hourly_cost'],
    'data':[
        'security/ir.model.access.csv',
        'views/clinic_op_reg_view.xml',
        'views/contact_view.xml',
        'data/ir_sequence_data.xml',
        'views/consultation_view.xml',
        'views/clinic_priscription.xml',
        'views/clinic_menu.xml'
    ]
}