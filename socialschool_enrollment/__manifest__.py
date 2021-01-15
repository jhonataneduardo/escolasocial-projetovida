# -*- coding: utf-8 -*-

{
    'name': 'Social School Enrollment',
    'version': '1.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 1,
    'summary': '...',
    'author': 'Jhonatan Eduardo',
    'website': '#',
    'depends': ['socialschool_base'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/student_view.xml',
        'views/enrollment_view.xml',
        'menu/socialschool_enrollment_menu.xml',
    ],
    'demo': [
        # 'demo/batch_demo.xml',
    ],
    'css': [
        # 'static/src/scss/base.scss'
    ],
    'qweb': [
        # 'static/src/xml/base.xml',
    ],
    'js': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
