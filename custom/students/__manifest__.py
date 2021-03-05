{
	'name': "Student",

	'summary': "Student Detail",

	'author': "Jay Suthar",

	'version':'1.0',

    'sequence': -10,

    'website': 'abc@gmail.com',

	'depends': ['base', 'mail'],

    'data': [
        'security/ir.model.access.csv',
        'views/student_view.xml',
        'views/department_view.xml'
    ],

    'demo' : [ ],
 

    'installable': True,

    'application': True,

    'active': True,

}