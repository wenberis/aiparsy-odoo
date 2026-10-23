# AiParsy for Odoo

Odoo module `aiparsy_connector`: send scans of Ukrainian vendor bills, waybills and acts from Odoo to
[AiParsy](https://aiparsy.com) for recognition; after approval AiParsy fills the same draft vendor bill
(vendor by ЄДРПОУ, number, date, lines, VAT).

- Branches `17.0`, `18.0`, `19.0` — Odoo 17, 18, 19 (`tools/port_branch.py` ports 17.0 to a newer series).
- `tools/make_uk_po.py` — Ukrainian translation from the exported `.pot`.
- `tools/make_images.py` — icon and cover for apps.odoo.com.
- `tools/make_zip.py` — the module as an archive (`dist/`), the one AiParsy offers for download.

License: LGPL-3.
