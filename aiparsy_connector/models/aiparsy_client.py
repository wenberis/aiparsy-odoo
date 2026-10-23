"""A small client of the AiParsy REST API: send scans, read their recognition status."""

import requests

from odoo import _
from odoo.exceptions import UserError

DEFAULT_URL = "https://aiparsy.com"
TIMEOUT = 60

# AiParsy document status -> status shown on the Odoo bill
STATUSES = {
    "pending": "sent",
    "queued": "sent",
    "processing": "sent",
    "processed": "recognized",
    "approved": "approved",
    "error": "error",
    "failed": "error",
}


class AiParsyClient:
    def __init__(self, url, api_key):
        if not api_key:
            raise UserError(_("Enter the AiParsy API key in Accounting → Configuration → Settings → AiParsy."))
        self.url = (url or DEFAULT_URL).rstrip("/")
        self.api_key = api_key

    @classmethod
    def from_env(cls, env):
        params = env["ir.config_parameter"].sudo()
        return cls(params.get_param("aiparsy.url"), params.get_param("aiparsy.api_key"))

    def document_url(self, document_id):
        return f"{self.url}/documents/results/{document_id}"

    def check(self):
        self._request("GET", "/api/documents", params={"limit": 1})

    def upload(self, name, content, mimetype):
        """Sends one file; answers with the AiParsy document ids it became (a zip may become several)."""
        files = [("documents[]", (name, content, mimetype or "application/octet-stream"))]
        answer = self._request("POST", "/api/documents", files=files)
        return (answer.get("data") or {}).get("document_ids") or []

    def statuses(self, document_ids):
        """{AiParsy document id: Odoo status} for the given documents."""
        params = {"ids": ",".join(str(i) for i in document_ids), "limit": len(document_ids)}
        answer = self._request("GET", "/api/documents", params=params)
        return {
            row["document_id"]: STATUSES.get(row.get("status"), "sent")
            for row in answer.get("data") or []
        }

    def _request(self, method, path, **kwargs):
        headers = {"X-API-Key": self.api_key, "Accept": "application/json"}
        try:
            response = requests.request(method, self.url + path, headers=headers, timeout=TIMEOUT, **kwargs)
        except requests.RequestException as error:
            raise UserError(_("Could not connect to AiParsy (%s): %s", self.url, error)) from error
        return self._answer(response)

    def _answer(self, response):
        try:
            answer = response.json()
        except ValueError:
            answer = {}
        if response.status_code == 401:
            raise UserError(_("AiParsy did not accept the API key. Create a new key in AiParsy → API Keys."))
        if response.status_code >= 400:
            message = answer.get("message") or response.reason
            raise UserError(_("AiParsy answered with an error (%s): %s", response.status_code, message))
        return answer
