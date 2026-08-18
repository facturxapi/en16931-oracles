# Runner

```bash
python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt
.venv/bin/python scripts/validate.py --dir fixtures --out-dir receipts/v1.4.0.03/fixtures --tag 03
.venv/bin/python scripts/validate.py --dir mutants --out-dir mutants/receipts/v1.4.0.03 --tag 03
.venv/bin/python scripts/validate.py --dir objective-a --out-dir receipts/v1.4.0.02/objective-a --tag 02
.venv/bin/python scripts/validate.py --dir objective-a --out-dir receipts/v1.4.0.03/objective-a --tag 03
```

Le script refuse d’exécuter un XSLT dont le SHA256 n’est pas celui mesuré
sur le zipball GitHub du tag (voir `EXPECTED_XSLT_SHA` dans `validate.py`).
Aucun validateur commercial. Les octets des factures ne sont pas journalisés.
