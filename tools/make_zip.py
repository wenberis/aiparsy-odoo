"""The module as an Odoo addon archive (aiparsy_connector/ at its root): dist/aiparsy_connector-<version>.zip"""

import ast
import os
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULE = ROOT / "aiparsy_connector"


def main():
    version = ast.literal_eval((MODULE / "__manifest__.py").read_text(encoding="utf-8"))["version"]
    out = ROOT / "dist" / f"aiparsy_connector-{version}.zip"
    out.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as archive:
        for folder, dirs, files in os.walk(MODULE):
            dirs[:] = [d for d in dirs if d != "__pycache__"]
            for name in files:
                path = Path(folder) / name
                archive.write(path, path.relative_to(ROOT).as_posix())
    print(out, out.stat().st_size)


if __name__ == "__main__":
    main()
