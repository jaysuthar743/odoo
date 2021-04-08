# -*- coding: utf-8 -*-
{
    'name': "sales_product_photo",
    'summary': """
      sales_product_photo """,
    'description': """
       sales_product_photo
    """,
    'author': "Brainvire",
    'website': "http://www.Brainvire.com",
    'category': 'sale',
    'version': '0.1',
    'depends': ['base', 'sale', 'stock'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/sales_product_image.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
