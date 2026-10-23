from odoo import _, fields, models
from odoo.exceptions import UserError

from ..models.aiparsy_client import AiParsyClient

# The AiParsy API takes up to 30 uploads a minute
MAX_FILES = 20


class AiParsyUpload(models.TransientModel):
    """Several scans at once: each becomes a draft vendor bill that AiParsy fills after recognition."""

    _name = "aiparsy.upload"
    _description = "Send scans to AiParsy"

    attachment_ids = fields.Many2many("ir.attachment", string="Scans")

    def action_send(self):
        self.ensure_one()
        if not self.attachment_ids:
            raise UserError(_("Add the scans to send."))
        if len(self.attachment_ids) > MAX_FILES:
            raise UserError(_("Send at most %s files at a time.", MAX_FILES))
        client = AiParsyClient.from_env(self.env)
        moves = self.env["account.move"]
        for scan in self.attachment_ids:
            moves |= self._bill_for(client, scan)
        return {
            "type": "ir.actions.act_window",
            "name": _("Sent to AiParsy"),
            "res_model": "account.move",
            "view_mode": "list,form",
            "domain": [("id", "in", moves.ids)],
            "context": {"default_move_type": "in_invoice"},
        }

    def _bill_for(self, client, scan):
        move = self.env["account.move"].create({"move_type": "in_invoice"})
        scan.write({"res_model": "account.move", "res_id": move.id})
        move.message_main_attachment_id = scan
        move._aiparsy_send(client, scan)
        return move
