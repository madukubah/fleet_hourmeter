# -*- coding: utf-8 -*-

{
    'name': 'Fleet Hourmeter',
    'version': '1.0',
    'author': 'Technoindo.com',
    'category': 'Fleet Management',
    'depends': [
        'fleet',
    ],
    'data': [
        "views/fleet_vehicle_hourmeter.xml",
        'views/menu.xml',

        "security/ir.model.access.csv",
    ],
    'qweb': [
        # 'static/src/xml/cashback_templates.xml',
    ],
    'demo': [
        # 'demo/sale_agent_demo.xml',
    ],
    "installable": True,
	"auto_instal": False,
	"application": False,
}
