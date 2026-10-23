"""Builds i18n/uk.po from the exported .pot: the module's own strings in Ukrainian.

Usage: python tools/make_uk_po.py   (run from the repository root, after exporting the .pot)
"""

import re
from pathlib import Path

I18N = Path(__file__).resolve().parent.parent / "aiparsy_connector" / "i18n"

UK = {
    '<span class="o_stat_text">AiParsy</span>': '<span class="o_stat_text">AiParsy</span>',
    "Add the scans to send.": "Додайте скани, які треба надіслати.",
    "AiParsy": "AiParsy",
    "AiParsy API key": "API-ключ AiParsy",
    "AiParsy accepted the API key.": "AiParsy прийняв API-ключ.",
    "AiParsy address": "Адреса AiParsy",
    "AiParsy answered with an error (%s): %s": "AiParsy відповів помилкою (%s): %s",
    "AiParsy did not accept the API key. Create a new key in AiParsy → API Keys.":
        "AiParsy не прийняв API-ключ. Створіть новий ключ в AiParsy → «API-ключі».",
    "AiParsy did not take the file %s.": "AiParsy не прийняв файл %s.",
    "AiParsy document": "Документ AiParsy",
    "AiParsy: refresh recognition status": "AiParsy: оновлення статусу розпізнавання",
    "Approved": "Затверджено",
    "Attach the scan of the document to the bill first.": "Спершу прикріпіть до рахунку скан документа.",
    "Bills back to Odoo": "Рахунки назад в Odoo",
    "Cancel": "Скасувати",
    "Check connection": "Перевірити підключення",
    "Could not connect to AiParsy (%s): %s": "Не вдалося підключитися до AiParsy (%s): %s",
    "Create a free AiParsy account": "Створити безкоштовний обліковий запис AiParsy",
    "Database": "База даних",
    "Each scan becomes a draft vendor bill. AiParsy recognizes it and, after approval, fills the bill: "
    "vendor, number, date, lines and VAT.":
        "Кожен скан стане чернеткою рахунку постачальника. AiParsy розпізнає його і після затвердження "
        "заповнить рахунок: постачальника, номер, дату, рядки й ПДВ.",
    "Enter the AiParsy API key in Accounting → Configuration → Settings → AiParsy.":
        "Вкажіть API-ключ AiParsy: Бухоблік → Налаштування → Налаштування → AiParsy.",
    "Enter these in AiParsy → Accounting systems → Odoo, with an Odoo user's login and API key.":
        "Вкажіть їх в AiParsy → «Облікові системи» → Odoo разом із логіном і ключем API користувача Odoo.",
    "Filled by AiParsy": "Заповнено AiParsy",
    "From AiParsy": "З AiParsy",
    "Not recognized": "Не розпізнано",
    "Odoo address": "Адреса Odoo",
    "Only a draft bill can be recognized.": "Розпізнати можна лише чернетку рахунку.",
    "Recognition of scans": "Розпізнавання сканів",
    "Recognize with AiParsy": "Розпізнати в AiParsy",
    "Recognized, to check": "Розпізнано, на перевірці",
    "Recognizing": "Розпізнається",
    "Scans": "Скани",
    "Send": "Надіслати",
    "Send at most %s files at a time.": "Надсилайте не більше %s файлів за раз.",
    "Send scans to AiParsy": "Надіслати скани в AiParsy",
    "Sent to AiParsy": "Надіслано в AiParsy",
    "Sent to AiParsy for recognition (document #%s).": "Надіслано в AiParsy на розпізнавання (документ #%s).",
    "Vendor bills, waybills and acts are recognized by AiParsy and come back as filled draft bills.":
        "Рахунки, видаткові накладні й акти розпізнає AiParsy, і вони повертаються заповненими чернетками рахунків.",
}

# Odoo's own technical labels: Odoo translates them itself
SKIP = {"Config Settings", "Created by", "Created on", "Display Name", "ID", "Journal Entry",
        "Last Updated by", "Last Updated on"}


def unquote(lines):
    return "".join(re.findall(r'"(.*)"', lines)).replace('\\"', '"')


def quote(text):
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main():
    pot = (I18N / "aiparsy_connector.pot").read_text(encoding="utf-8")
    blocks = pot.split("\n\n")
    header = blocks[0].replace('"Language: \\n"', '"Language: uk\\n"')
    out, missing = [header], []
    for block in blocks[1:]:
        match = re.search(r'msgid ((?:".*"\n?)+)msgstr ""', block)
        if not match:
            continue
        msgid = unquote(match.group(1))
        if msgid in SKIP:
            continue
        if msgid not in UK:
            missing.append(msgid)
            continue
        out.append(block[: match.start()] + f"msgid {quote(msgid)}\nmsgstr {quote(UK[msgid])}")
    (I18N / "uk.po").write_text("\n\n".join(out) + "\n", encoding="utf-8")
    if missing:
        raise SystemExit("No Ukrainian for: " + "; ".join(missing))


if __name__ == "__main__":
    main()
