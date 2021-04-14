# -*- coding: utf-8 -*-
{
    'name': "appointment_website",
    'summary': """
       appointment_website""",
    'description': """
        appointment_website
    """,
    'author': "brainvire",
    'website': "http://www.brainvire.com",
    'category': 'website',
    'version': '0.1',
    'depends': ['base', 'website', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/doctor_appointment_form.xml',
        'views/doctor_appointment_template_form.xml',
        'views/doctor_appointment_thank_you_page.xml'
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
