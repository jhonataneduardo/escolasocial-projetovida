# -*- coding: utf-8 -*-

{
    'name': 'Social School Parent',
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
        'views/student_view.xml',
        'views/parent_view.xml',
        # 'menu/socialschool_parent_menu.xml',
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
