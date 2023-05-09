# -*- coding: utf-8 -*-
{
    'name': "wmr-api",

    'summary': """
        This Modules Contains All the APIs used for creating and updating the values of following:
        1.Sales""",

    'description': """
        1. Sales
            a. Create API (URL: /wmr-api/sales/create): This API creates the sales order and add the first quote to it.
                Note: The user ID must be passed in the request so that any data changes are made would be registered on the name of that user.
                Sample Request:
                {
                    "params": {
                        "user": {
                            "id": 6
                        },
                        "sale":{
                            "partner_id":3,
                            "x_studio_quote_id": "Lorem Ipsum",
                            "note":"Lorem Ipsum",
                            "payment_term_id": 3,
                            "order_line":[{
                                "product_id": false,
                                "name": "Lorem Ipsum",
                                "product_uom_qty": 0,
                                "price_unit": 0,
                                "display_type":  "line_section",
                                "x_app_quote_id": "Lorem Ipsum",
                                "x_app_group_id": "Lorem Ipsum"
                            },{
                                "product_id": 634,
                                "name": "Lorem Ipsum",
                                "product_uom_qty": 1,
                                "price_unit": 100,
                                "display_type": false,
                                "x_app_quote_id": "Lorem Ipsum",
                                "x_app_group_id": "Lorem Ipsum"
                            }]
                        }
                    }
                }
            
            b. Update API (URL: /wmr-api/sales/update): This API request adds the quote to the existing sales order. 
                Note: The user ID and the sales.order id should be passed to add to that sales order and register changes on the name of the user.
                Sample Request:
                {
                    "params": {
                        "user": {
                            "id": 6
                        },
                        "sale":{
                            "id":123,
                            "x_studio_quote_id": "Lorem Ipsum",
                            "note":"Lorem Ipsum",
                            "payment_term_id": 3,
                            "order_line":[{
                                "product_id": false,
                                "name": "Lorem Ipsum",
                                "product_uom_qty": 0,
                                "price_unit": 0,
                                "display_type":  "line_section",
                                "x_app_quote_id": false,
                                "x_app_group_id": "Lorem Ipsum"
                            },{
                                "product_id": 23,
                                "name": "Lorem Ipsum",
                                "product_uom_qty": 1,
                                "price_unit": 100,
                                "display_type": false,
                                "x_app_quote_id": false,
                                "x_app_group_id": "Lorem Ipsum"
                            }]
                        }
                    }
                }
    """,

    'author': "Radhey",
    'website': "http://www.wallsmetalroofng.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customization',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],
    'data': ['views/contact_view.xml',],
    'installable': True,
    'auto_install': False
}
