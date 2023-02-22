
# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

{
    'name': 'Falcon Material Backend Theme',
    'description': '''Customizable Backend Theme Based on Material Design
odoo falcon backend material theme
openerp falcon backend material theme
odoo material store backend theme
odoo material backend theme
odoo customizable material backend theme
responsive odoo material backend theme
customizable backend theme for odoo material store
odoo material design theme
material design backend
responsive odoo material design backend theme
material design admin theme
odoo material design admin theme
material design dashboard theme
odoo material design dashboard theme
material design admin template
odoo material design admin template
material design dashboard template
odoo material design dashboard template
material design based bootstrap themes
material design based bootstrap theme for odoo
odoo theme for material store backend
Material theme
Material
Material store
odoo Material store
odoo Material theme
retail store
retail theme
html5 theme
responsive theme
ecommerce store
ecommerce theme
html5 ecommerce store
html5 ecommerce theme
custom theme
mobile custom theme
bootstrap theme
furnishing industry
odoo 10 theme
odoo 11 theme
custom odoo theme
odoo backend theme
backend theme
    ''',
    'summary': 'Customizable Backend Theme Based on Material Design',
    'category': 'Theme/Backend',
    'version': '13.0.1.0.0',
    'license': 'OPL-1',
    'author': 'AppJetty',
    'website': 'https://www.appjetty.com',
    'support': 'support@appjetty.com',
    'depends': ['base_setup', 'web_editor'],
    'data': [
        'views/template.xml',
        'data/data.xml',
        'views/base_config_view.xml',
        'views/ir_ui_menu_view.xml',
    ],
    'installable': True,
    'qweb': ['static/src/xml/base.xml',
             'static/src/xml/new_menu.xml',
             'static/src/xml/widget_color.xml',
             ],
    'application': True,
    'live_test_url': 'https://theme-falcon-material-v13.appjetty.com/web/login',
    'images': [
        'static/description/splash-screen.png',
        'static/description/splash-screen_screenshot.gif',
    ],
    'price': 191.00,
    'currency': 'EUR',
}
