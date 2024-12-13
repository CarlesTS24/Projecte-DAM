# -*- coding: utf-8 -*-
{
    'name': "instalaciones_deportivas",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Carles Talens",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sport',
    'version': '0.1',
    'license': 'LGPL-3',
    'installable': True,
    'application': False,

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'mail',
    ],

    # always loaded
    'data': [
        'security/instalaciones_groups.xml',
        #'security/ir.model.access.csv',
        'data/instalaciones_deportivas_data.xml',
        'views/instalaciones_deportivas_action.xml',
        'views/menu_instalaciones_deportivas.xml',
        'views/instalaciones_deportivas_view.xml',
        #'views/views.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
