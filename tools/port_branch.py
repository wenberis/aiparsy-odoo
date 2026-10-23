"""Ports the module from the 17.0 branch to a newer Odoo series (18.0, 19.0).

Usage: python tools/port_branch.py <module dir of the worktree> <series, e.g. 18.0>
Since 18.0 a list view is «list», not «tree», the bills list has no «state» column, and ir.cron has no «numbercall».
"""

import re
import sys
from pathlib import Path


def main(module: Path, series: str):
    manifest = module / "__manifest__.py"
    text = manifest.read_text(encoding="utf-8")
    manifest.write_text(re.sub(r'"version": "[\d.]+"', f'"version": "{series}.1.0.0"', text), encoding="utf-8")

    upload = module / "wizard" / "aiparsy_upload.py"
    upload.write_text(upload.read_text(encoding="utf-8").replace('"view_mode": "tree,form"', '"view_mode": "list,form"'), encoding="utf-8")

    cron = module / "data" / "ir_cron.xml"
    cron.write_text(re.sub(r'\s*<field name="numbercall">-1</field>', "", cron.read_text(encoding="utf-8")), encoding="utf-8")

    views = module / "views" / "account_move_views.xml"
    text = views.read_text(encoding="utf-8").replace("account.move.in_invoice.tree.aiparsy", "account.move.in_invoice.list.aiparsy")
    # the bills list of 18.0+ has no «state» column: the AiParsy column goes at the end of the list
    text = text.replace("""<xpath expr="//field[@name='state']" position="before">""", """<xpath expr="//list" position="inside">""")
    views.write_text(text, encoding="utf-8")
    print(module, "->", series)


if __name__ == "__main__":
    main(Path(sys.argv[1]), sys.argv[2])
