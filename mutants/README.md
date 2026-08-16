# mutants/

Dix copies des fixtures CEN EN16931 1.3.16, **une mutation sémantique d'une ligne chacune**.

Ce n'est pas un corpus officiel. Les originaux restent dans `fixtures/` (SHA256 inchangés).

| Fichier | Classe | ids 1.3.16 |
|---|---|---|
| `CII_example1.xml` | TOTAL BT-112 | BR-CO-15, BR-CO-16 |
| `CII_example3.xml` | VAT BT-117 | BR-S-09, BR-CO-14 |
| `CII_example5.xml` | MANDATORY BT-1 | BR-02 |
| `CII_business_example_01.xml` | LINE-SUM BT-106 | BR-CO-10, BR-CO-13 |
| `CII_business_example_02.xml` | TYPE BT-3 | BR-CL-01 |
| `CII_business_example_Z.xml` | ID-TRUNC BT-31 | BR-CO-09 |
| `CII-BR-CO-10-RoundingIssue.xml` | MANDATORY BT-24 | BR-01 |
| `XRechnung-O.xml` | DATE BT-2 | CII-DT-097 |
| `ubl-tc434-creditnote1.xml` | TOTAL UBL BT-115 | BR-CO-16 |
| `huf_example_cii.xml` | VAT-RATE BT-119 | BR-CO-17, BR-S-08, BR-S-09 |

Reproduire :

```bash
.venv/bin/python scripts/validate.py --dir mutants --out-dir mutants/receipts --no-expected
```

Détail : `../MUTANTS.md`, diffs : `DIFFS.md`. Recettes : `receipts/`.
Date : 16 Aug 2026 PT.
