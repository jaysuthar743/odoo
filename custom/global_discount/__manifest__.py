# -*- coding: utf-8 -*-
{
    'name': "global_discount",
    'summary': """
       global_discount
       """,
    'description': """
        global_discount
    """,
    'author': "My Company",
    'website': "http://www.brainvire.com",
    'category': 'sale',
    'version': '0.1',
    'depends': ['base', 'sale', 'web', 'base', 'base_setup', 'website'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/global_discount_view.xml'
    ],
    'qweb': ['static/my_pivot_view.xml'],
    'demo': [
        # 'demo/demo.xml',
    ],
}

