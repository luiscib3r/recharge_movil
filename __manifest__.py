# -*- coding: utf-8 -*-
{
    'name': "Recarga Movil",

    'summary': """
        Herramienta para administración de clientes del servicio de recarga de saldo en los móviles
    """,

    'description': """
    """,

    'author': "Luis Correa (Soft4Cuba)",
    'website': "https://soft4cuba.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Application',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],
    'qweb': ['static/src/xml/datascience.xml'],
    # always loaded
    'data': [
        'security/group.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/recarga.xml',
        'views/oferta.xml',
        'views/cashline_wizard.xml',
        'views/cashline.xml',
        'views/provedor.xml',
        'views/datascience.xml',
        'views/templates.xml',
        'data/stage.xml',
        'security/rules.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
