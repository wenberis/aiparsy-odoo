from odoo import _, fields, models

from .aiparsy_client import DEFAULT_URL, AiParsyClient


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    aiparsy_url = fields.Char(string="AiParsy address", config_parameter="aiparsy.url", default=DEFAULT_URL)
    aiparsy_api_key = fields.Char(string="AiParsy API key", config_parameter="aiparsy.api_key")
    # What to enter in AiParsy so that it can create the recognized bills here
    aiparsy_odoo_url = fields.Char(string="Odoo address", readonly=True, default=lambda self: self._aiparsy_base_url())
    aiparsy_odoo_db = fields.Char(string="Database", readonly=True, default=lambda self: self.env.cr.dbname)

    def _aiparsy_base_url(self):
        return self.env["ir.config_parameter"].sudo().get_param("web.base.url")

    def action_aiparsy_check(self):
        self.ensure_one()
        AiParsyClient(self.aiparsy_url, self.aiparsy_api_key).check()
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {"type": "success", "message": _("AiParsy accepted the API key.")},
        }
