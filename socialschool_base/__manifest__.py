# -*- coding: utf-8 -*-

{
    'name': 'Escola Social Base',
    'version': '12.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 1,
    'summary': '...',
    'author': 'Jhonatan Eduardo',
    'website': '#',
    'depends': ['hr'],
    'data': [
        'security/socialschool_security.xml',
        'security/ir.model.access.csv',
        'views/student_view.xml',
        'views/faculty_view.xml',
        'views/group_view.xml',
        'views/course_view.xml',
        'views/category_view.xml',
        "menu/socialschool_base_menu.xml",
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
