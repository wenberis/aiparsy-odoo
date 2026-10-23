{
    "name": "AiParsy — Recognize Vendor Bills from Scans",
    "summary": "Ukrainian vendor bills, waybills and acts: send a scan to AiParsy, "
    "get a filled draft bill with partner, lines and VAT",
    "version": "18.0.1.0.0",
    "category": "Accounting/Accounting",
    "author": "AiParsy",
    "website": "https://aiparsy.com/blog/odoo",
    "license": "LGPL-3",
    "depends": ["account"],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_cron.xml",
        "views/res_config_settings_views.xml",
        "views/account_move_views.xml",
        "wizard/aiparsy_upload_views.xml",
    ],
    "images": ["static/description/banner.png"],
    "installable": True,
    "application": False,
}
