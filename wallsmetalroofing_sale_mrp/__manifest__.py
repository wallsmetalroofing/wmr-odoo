# -*- coding: utf-8 -*-
{
    'name': "Walls Metal Roofing: Auto-calculated panel price",

    'summary': 'SO and MO customisation',
    'description': """

    - Requirement 1 –  3 Extra fields on SO lines
    1. Panel Count: this is an integer field where they will enter the numberof panels
    2. Length (ft): This is a decimal field where they will enter the panel length in feet
    3. Length (in): This is a decimal field where they will enter the panel length in inches
    - For example,  14 panels of 6’10”
    - Panel count: 14
    - Length (ft): 6
    - Length (in): 10

    - Requirement 2 - Calculated field for Quantity
    - When the product on the SO line is part of the category “Panels”,
the quantity field will be calculated as the following: 
    - Panel count * Length (ft+in) = quantity (length in feet)
    - When the product is part of another category, Panel count = quantity
    - Length fields will be required when the product belongs to “Panels”
category but non-required when belonging to another one. 

    - Requirement 3 - Push the 3 new fields on MO
    - Those 3 extra fields need to be pushed onto the MO generated by the SO.
    """,

    'author': "Odoo Inc.",
    'website': "https://www.odoo.com",

    'category': 'Customizations',
    'version': '1.0',
    'depends': ["sale_mrp", "purchase"],
    'data': [
        'views/mrp_production_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
}
