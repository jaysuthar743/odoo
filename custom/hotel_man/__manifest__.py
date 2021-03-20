# -*- coding: utf-8 -*-
{
    'name': "hotel_man",

    'summary': """
       Hotel Management""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/ir.cron_data.xml',
        'views/hotel_room_view.xml',
        'views/hotel_room_reg_view.xml',
        'views/hotel_reg_inquiry.xml',
        'views/hotel_room_type_view.xml',
        'report/registration_template.xml',
        'report/registration_report.xml',
        'data/mail_template.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
