# -*- coding: utf-8 -*-
{
    "name": "wmr-api",
    "summary": """
        This Modules Contains All the APIs used for creating and updating the values of following:
        1.  Sales
        2.  Contacts""",
   "author": "Radhey",
    "sequence": -100,
    "website": "http://www.wallsmetalroofng.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Customization",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
    "license": "LGPL-3",
}
