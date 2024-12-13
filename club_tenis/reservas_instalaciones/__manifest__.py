# -*- coding: utf-8 -*-
{
    'name': "reservas_instalaciones",

    'summary': """
        Gestión y reservas de instalaciones deportivas
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Carles Talens",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sport Management',
    'version': '0.1',
    'license': 'LGPL-3',
    'installable': True,
    'application': False,

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'instalaciones_deportivas',
        'calendar',
        'mail',
    ],

    # always loaded
    'data': [
        'security/reservas_groups.xml',
        'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
        'views/reservas_instalaciones_view.xml',
        'views/reservas_instalaciones_action.xml',
        'views/menu_reservas_instalaciones.xml',
        'data/cron_jobs.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
