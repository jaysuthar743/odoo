# -*- coding: utf-8 -*-
{
    'name': "payment_cybersource",
    'summary': """
        payment_cybersource""",
    'description': """
        payment_cybersource
    """,
    'author': "brainvire",
    'website': "http://www.brainvire.com",
    'category': 'payment',
    'version': '0.1',
    'depends': ['base', 'payment_authorize'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/payment_views.xml',
        'views/payment_cybersource_templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
