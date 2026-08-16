# Mutants EN16931 1.3.16 — preuve que le runner détecte les faux documents

**Date :** 16 août 2026 (Europe/Paris) — 16 Aug 2026 PT  
**Moteur :** SaxonC-HE 13.0 (`saxonche==13.0.0`)  
**XSLT :** `vendor/en16931-1.3.16/xslt/EN16931-CII-validation.xslt` / `EN16931-UBL-validation.xslt`  
**Statut :** préparation, pas une publication. Aucun `git init`. Aucun lot privé / FNFE / FeRD.

## Discipline

- Une ligne sémantique par mutant (même basename que la fixture).
- Originaux dans `fixtures/` **non modifiés**. Jamais écrasés, même temporairement.
- Classes variées : TOTAL, VAT, MANDATORY, LINE-SUM, TYPE, ID-TRUNC, DATE, TOTAL-UBL, VAT-RATE.
- Les `id` de `svrl:failed-assert` viennent de l'attribut `id` du SVRL officiel, pas d'une invention.
- Les octets des factures ne sont pas journalisés.

## Table des 10 mutants

| Mutant | Fixture source | Classe | Diff (une ligne) | fail | ids SVRL | SVRL |
|---|---|---|---|---:|---|---|
| `mutants/CII_example1.xml` | `CII_example1.xml` | TOTAL (BT-112) | L640 `SpecifiedTradeSettlementHeaderMonetarySummation/GrandTotalAmount` : `250.33` → `250.34` | 2 | `BR-CO-15`, `BR-CO-16` | `mutants/receipts/CII_example1.svrl.xml` |
| `mutants/CII_example3.xml` | `CII_example3.xml` | VAT (BT-117 ≠ BT-110) | L111 `ApplicableTradeTax/CalculatedAmount` : `225` → `226` (TaxTotalAmount reste 225) | 2 | `BR-S-09`, `BR-CO-14` | `mutants/receipts/CII_example3.svrl.xml` |
| `mutants/CII_example5.xml` | `CII_example5.xml` | MANDATORY (BT-1) | L22 `rsm:ExchangedDocument/ram:ID` (BT-1, **pas** BT-24) : `TOSL110` → vide | 1 | `BR-02` | `mutants/receipts/CII_example5.svrl.xml` |
| `mutants/CII_business_example_01.xml` | `CII_business_example_01.xml` | LINE-SUM (BT-106) | L473 header `LineTotalAmount` : `1436.5` → `1436.51` (Σ BT-131 inchangée) | 2 | `BR-CO-10`, `BR-CO-13` | `mutants/receipts/CII_business_example_01.svrl.xml` |
| `mutants/CII_business_example_02.xml` | `CII_business_example_02.xml` | TYPE (BT-3) | L20 `rsm:ExchangedDocument/ram:TypeCode` : `380` → `999` | 1 | `BR-CL-01` | `mutants/receipts/CII_business_example_02.svrl.xml` |
| `mutants/CII_business_example_Z.xml` | `CII_business_example_Z.xml` | ID-TRUNC (BT-31) | L139 `SellerTradeParty/SpecifiedTaxRegistration/ID[@schemeID='VA']` : `DE37/302/30168` → `37` | 1 | `BR-CO-09` | `mutants/receipts/CII_business_example_Z.svrl.xml` |
| `mutants/CII-BR-CO-10-RoundingIssue.xml` | `CII-BR-CO-10-RoundingIssue.xml` | MANDATORY (BT-24) | L10 `GuidelineSpecifiedDocumentContextParameter/ram:ID` (BT-24, **pas** BT-1) : `urn:ferd:…:1p0:comfort` → vide | 1 | `BR-01` | `mutants/receipts/CII-BR-CO-10-RoundingIssue.svrl.xml` |
| `mutants/XRechnung-O.xml` | `XRechnung-O.xml` | DATE (BT-2) | L23 `ExchangedDocument/IssueDateTime/DateTimeString` : `20210114` → `20151399` | 1 | `CII-DT-097` | `mutants/receipts/XRechnung-O.svrl.xml` |
| `mutants/ubl-tc434-creditnote1.xml` | `ubl-tc434-creditnote1.xml` | TOTAL UBL (BT-115) | L108 `cac:LegalMonetaryTotal/cbc:PayableAmount` : `100.11` → `101.11` | 1 | `BR-CO-16` | `mutants/receipts/ubl-tc434-creditnote1.svrl.xml` |
| `mutants/huf_example_cii.xml` | `huf_example_cii.xml` | VAT-RATE (BT-119) | L325 header `ApplicableTradeTax/RateApplicablePercent` : `27.00` → `19.00` (CalculatedAmount 18679.00 inchangé) | 3 | `BR-CO-17`, `BR-S-08`, `BR-S-09` | `mutants/receipts/huf_example_cii.svrl.xml` |

Diffs complets : `mutants/DIFFS.md`. Recettes une ligne : `mutants/receipts/<stem>.oneline.txt`.

**Résultat mutants :** 10 fichiers, **10 × ≥1 `svrl:failed-assert`**, 0 vert.  
`mutants/RESULTS.sha256` = `babed63a0a4f304466d23ba7f1a1a781730e8c489eb9b775464910b1a43c5e55`

## FINDING MAJEUR (observé, puis remplacé)

**Tentative 1 sur `CII_business_example_Z` :** troncature BT-31 `DE37/302/30168` → `DE37` (élément conservé, préfixe pays ISO intact).

- Verdict XSLT 1.3.16 : **0 `svrl:failed-assert`** (vert).
- Analyse **(a)** — trou Schematron officiel, pas une mutation cosmétique.
  - `BR-CO-09` lit BT-31 mais ne teste que `substring(.,1,2)` ∈ codes pays ISO. Le corps de l'identifiant (longueur, format, clé) n'est pas testé.
  - Aucune règle CII 1.3.16 ne vérifie un SIRET/VAT « trop court » si le préfixe reste `DE`.
  - Règle qui *aurait dû* tirer pour une troncature sémantique d'identifiant : un contrôle de format/longueur BT-31 (absent du XSLT 1.3.16). `BR-CO-09` est le seul voisin ; il est silencieux tant que les 2 premiers caractères sont un pays.
- Analyse **(b)** écartée : le champ est bien lu (même `schemeID="VA"`).

Conformément à la carte suggérée (« si vert, changer »), le mutant **n'a pas été laissé vert**. Mutation retenue : `DE37/302/30168` → `37` (préfixe pays retiré). Alors `BR-CO-09` tire. La troncature `→ DE37` reste un trou réel du XSLT officiel ; elle n'est plus le fichier livré dans `mutants/`.

Note (pas un FINDING) : `20151399` sur BT-2 ne tire **pas** `BR-03` (présence seulement : `normalize-space(DateTimeString[@format='102']) != ''`). C'est `CII-DT-097` (regex `YYYYMMDD`) qui tire. Mutation conservée, 1 failed-assert.

## Journal hash-probe — 16 Aug 2026 PT

Les fixtures n'ont **jamais** été écrasées. `--hash-probe` copie 9 originaux + 1 mutant dans un répertoire temporaire, hashe cet ensemble, puis re-hashe les 10 originaux.

| Étape | Ensemble | `RESULTS.sha256` (full) |
|---|---|---|
| 1. avant | 10 fixtures officielles | `dffb88780654fb4861df84bbd6df18aae5d89b0a5b8f4fd12ce5fb5f9a7f0dab` |
| 2. sonde | 9 originaux + `mutants/CII_example1.xml` (même basename) | `d3e201c0313de6f6bb588ad7ec5213637fb6ef5a9365f42df81a7e0fa5259079` |
| 3. après | 10 fixtures officielles (inchangées) | `dffb88780654fb4861df84bbd6df18aae5d89b0a5b8f4fd12ce5fb5f9a7f0dab` |

- Étape 2 **diffère** de l'étape 1 (le runner hashe `failed_assert` + `sha256` de chaque fichier).
- Étape 3 **revient** à l'épingle. Les originaux n'ont pas été restaurés depuis une copie cassée : ils n'ont pas été touchés.
- Restore « depuis l'extrait officiel » : non nécessaire (pas d'écriture dans `fixtures/`). Contrôle d'intégrité : `check_fixtures()` + `sha256sum -c fixtures/SHA256SUMS` (tous OK).

Sonde étape 2 : `CII_example1.xml` → 2 failed-assert `BR-CO-15,BR-CO-16` ; les 9 autres restent 0.

## `sha256sum -c fixtures/SHA256SUMS` (après tout travail)

Exécuté depuis `fixtures/` le 16 Aug 2026 PT :

```
CII-BR-CO-10-RoundingIssue.xml: OK
CII_business_example_01.xml: OK
CII_business_example_02.xml: OK
CII_business_example_Z.xml: OK
CII_example1.xml: OK
CII_example3.xml: OK
CII_example5.xml: OK
XRechnung-O.xml: OK
huf_example_cii.xml: OK
ubl-tc434-creditnote1.xml: OK
```

SHA256 des 10 fichiers = table du brief (inchangés).

## Reproduire

À la racine de `repo-v1/` :

```bash
# mutants (10 XML, imprime les ids failed-assert, ignore expected.json)
.venv/bin/python scripts/validate.py --dir mutants --out-dir mutants/receipts --no-expected

# fixtures (défaut, byte-stable)
.venv/bin/python scripts/validate.py
# → oracles/receipts/RESULTS.sha256 == dffb88780654fb4861df84bbd6df18aae5d89b0a5b8f4fd12ce5fb5f9a7f0dab

# preuve que le hash bouge puis revient (sans écrire dans fixtures/)
.venv/bin/python scripts/validate.py --hash-probe --probe-mutant CII_example1.xml
```

Comportement par défaut **identique** : `RESULTS.json` canonique sans ids (les ids sont imprimés en résumé seulement). Hash fixtures inchangé.

## Runner (extensions)

`scripts/validate.py` :

- `--dir PATH` (défaut `fixtures/`)
- `--out-dir PATH` (défaut `oracles/receipts`)
- `--no-expected` (saute `expected.json` ; ne traite pas un failed-assert mutant comme STOP)
- `--hash-probe` / `--probe-mutant`
- résumé : colonne `ids` = attribut `id` de chaque `svrl:failed-assert`

Pas de journalisation des octets de facture.
