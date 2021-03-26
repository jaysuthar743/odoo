# -*- coding: utf-8 -*-
{
    'name': "hotel_man",

    'summary': """
       Hotel Management""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Brainvire",
    'website': "http://www.brainvire.com",

    'category': 'hotel',
    'version': '0.1',

    'depends': ['base', 'mail', 'sale'],

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
        'data/mail_template.xml',
        'views/report_reg_excel.xml',
        'views/hotel_room_import.xml',
        'views/custom_popup_message.xml',
        'data/hotel.room.csv',
        'views/sales_order_import_product.xml',
        'views/product_upload_wizard_view.xml',
        # 'security/hotel_access_rights.xml'
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
