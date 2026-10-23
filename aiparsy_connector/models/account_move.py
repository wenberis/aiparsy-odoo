import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from .aiparsy_client import AiParsyClient

_logger = logging.getLogger(__name__)

# Bills polled for their recognition status in one cron run
REFRESH_BATCH = 200


class AccountMove(models.Model):
    _inherit = "account.move"

    aiparsy_document_id = fields.Integer(string="AiParsy document", copy=False, readonly=True, index=True)
    aiparsy_status = fields.Selection(
        [
            ("sent", "Recognizing"),
            ("recognized", "Recognized, to check"),
            ("approved", "Approved"),
            ("filled", "Filled by AiParsy"),
            ("error", "Not recognized"),
        ],
        string="AiParsy",
        copy=False,
        readonly=True,
    )

    def action_aiparsy_send(self):
        client = AiParsyClient.from_env(self.env)
        for move in self:
            move._aiparsy_send(client, move._aiparsy_scan())
        return True

    def action_aiparsy_open(self):
        self.ensure_one()
        client = AiParsyClient.from_env(self.env)
        return {"type": "ir.actions.act_url", "url": client.document_url(self.aiparsy_document_id), "target": "new"}

    def _aiparsy_scan(self):
        self.ensure_one()
        scan = self.message_main_attachment_id or self.env["ir.attachment"].search(
            [("res_model", "=", "account.move"), ("res_id", "=", self.id)], order="id", limit=1
        )
        if not scan:
            raise UserError(_("Attach the scan of the document to the bill first."))
        return scan

    def _aiparsy_send(self, client, scan):
        self.ensure_one()
        if self.state != "draft":
            raise UserError(_("Only a draft bill can be recognized."))
        document_ids = client.upload(scan.name, scan.raw, scan.mimetype)
        if not document_ids:
            raise UserError(_("AiParsy did not take the file %s.", scan.name))
        self.write({"aiparsy_document_id": document_ids[0], "aiparsy_status": "sent"})
        self.message_post(body=_("Sent to AiParsy for recognition (document #%s).", document_ids[0]))

    @api.model
    def _cron_aiparsy_refresh(self):
        moves = self.search([("aiparsy_status", "in", ("sent", "recognized"))], limit=REFRESH_BATCH)
        if not moves:
            return
        try:
            statuses = AiParsyClient.from_env(self.env).statuses(moves.mapped("aiparsy_document_id"))
        except UserError as error:
            _logger.warning("AiParsy status refresh skipped: %s", error)
            return
        for move in moves:
            status = statuses.get(move.aiparsy_document_id)
            if status and status != move.aiparsy_status:
                move.aiparsy_status = status
