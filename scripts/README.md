# scripts/

Runner reproductible des 10 fixtures CEN sous le XSLT officiel
EN16931 1.3.16.

## Une commande

À la racine du dépôt (cette arborescence) :

```bash
python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt && .venv/bin/python scripts/validate.py
```

`requirements.txt` épingle `saxonche==13.0.0` (SaxonC-HE 13.0).

## Bi-mode

| Mode | Comportement |
|---|---|
| `--mode reference` (défaut) | XSLT vendored `vendor/en16931-1.3.16/xslt/`. Verdict **normatif**. Échec si vendor/ manque ou si le SHA256 XSLT diverge. |
| `--mode cross-platform` | Mêmes octets XSLT. Si vendor/ est absent (ou SHA inattendu), télécharge les deux ZIP officiels dans `.cache/en16931-1.3.16/`, vérifie le SHA256 des ZIP (épinglé dans `validate.py`), n'extrait que les deux XSLT, puis valide. **Pas de saut silencieux** : réseau impossible → exit ≠ 0. |

ZIP épinglés :

- CII `1cd53cb8a84d38aedc82c0caede217da983a7934dd663f793a092fd66443c561`
- UBL `bafada015efbc5248bf5e05ad2191e1d9833ef96e9dd5f4bce420a747342da85`

URL : release
[validation-1.3.16](https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/tag/validation-1.3.16).

## Contrôles

1. Intégrité des fixtures contre `fixtures/SHA256SUMS` (avant toute
   validation).
2. Transformation XSLT → SVRL (CII ou UBL selon le nom du fichier).
3. Écriture `oracles/receipts/<stem>.svrl.xml` + `<stem>.receipt.md`.
4. Écriture `oracles/receipts/RESULTS.json` (JSON canonique :
   `sort_keys=True`, `separators=(',', ':')`, tableau trié par
   `file`, **sans horodatage**) et `RESULTS.sha256`.
5. Comparaison à `expected.json`. Exit 0 seulement si
   `failed_assert == 0` pour les 10 **et** `fired_rule` identique
   (sauf `--allow-fired-drift`).

`SOURCE_DATE_EPOCH=1771286400` (2026-02-17 00:00:00 UTC) est posé
dans l'environnement du processus.

Le script n'imprime pas les octets des factures. Il n'appelle aucun
validateur commercial.

## Fichiers

| Fichier | Rôle |
|---|---|
| `validate.py` | runner |
| `requirements.txt` | `saxonche==13.0.0` |
| `expected.json` | `fired-rule` / `failed-assert` verrouillés (nuit du 16 août 2026) |

## Options ajoutées (16 Aug 2026 PT)

Le comportement par défaut (sans option) est **inchangé** : `fixtures/` + `expected.json` + `oracles/receipts/RESULTS.json` byte-stable (`dffb88780654fb4861df84bbd6df18aae5d89b0a5b8f4fd12ce5fb5f9a7f0dab`).

| Option | Rôle |
|---|---|
| `--dir PATH` | XML à valider (défaut `fixtures/`) |
| `--out-dir PATH` | Recettes SVRL + RESULTS (défaut `oracles/receipts`) |
| `--no-expected` | Ignore `expected.json` (requis pour `mutants/`) |
| `--hash-probe` | 9 originaux + 1 mutant en temp ; prouve que `RESULTS.sha256` change puis revient. N'écrit pas dans `fixtures/`. |
| `--probe-mutant NAME` | Mutant pour `--hash-probe` (défaut `CII_example1.xml`) |

Le résumé imprime les `id` des `svrl:failed-assert`. Ces ids **ne sont pas** dans `RESULTS.json` (hash fixtures inchangé).

Mutants :

```bash
.venv/bin/python scripts/validate.py --dir mutants --out-dir mutants/receipts --no-expected
```
