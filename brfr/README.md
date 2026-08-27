# BR-FR / France_RFE Flux2 oracles (v1.1)

Machine-verified fixtures, mutants, gaps, and dual-version receipts for the
official France_RFE Flux2 Schematron/XSLT (`v1.4.0.02` / `v1.4.0.03`).

**Engine:** SaxonC-HE 13.0 (`saxonche==13.0.0`).
**Executed artefacts:** Flux2 XSLT under `vendor/` (unmodified copies).

Synthetic fixtures only — no customer invoices or payment means.
Licence: `vendor/LICENSE-APACHE-2.0-France_RFE.txt` + root `LICENSE-NOTES.md`.

---

| Élément | URL primaire | Mesure |
|---|---|---|
| Dépôt | https://github.com/fnfempe/France_RFE | — |
| Release `.02` | https://github.com/fnfempe/France_RFE/releases/tag/v1.4.0.02 | `published_at` 2026-07-14T17:20:22Z = **19:20 PT** |
| Release `.03` | https://github.com/fnfempe/France_RFE/releases/tag/v1.4.0.03 | `published_at` 2026-08-04T17:59:39Z = **19:59 PT** |
| API `.02` | https://api.github.com/repos/fnfempe/France_RFE/releases/tags/v1.4.0.02 | JSON : `meta/release-v1.4.0.02.json` (provenance slim) |
| API `.03` | https://api.github.com/repos/fnfempe/France_RFE/releases/tags/v1.4.0.03 | JSON : `meta/release-v1.4.0.03.json` (provenance slim) |
| Ref tag `.02` | https://api.github.com/repos/fnfempe/France_RFE/git/refs/tags/v1.4.0.02 | commit **`e9520ce398cc99bed4bab493773a494af8ca5aff`** |
| Ref tag `.03` | https://api.github.com/repos/fnfempe/France_RFE/git/refs/tags/v1.4.0.03 | commit **`a63e6b538bdaff460f17c38dc1bc5455cf1ba35a`** |
| Zipball `.02` | https://api.github.com/repos/fnfempe/France_RFE/zipball/v1.4.0.02 | SHA256 **mesuré** `9ba5d5550f0504a067a431339a7d17c122eda9a7031eab0b0a453b78af3e037d` — racine `fnfempe-France_RFE-e9520ce` |
| Zipball `.03` | https://api.github.com/repos/fnfempe/France_RFE/zipball/v1.4.0.03 | SHA256 **mesuré** `2c247a25691ab72d2c0ddf72d1957673b7d427b0775508da3ef6810a71863019` — racine `fnfempe-France_RFE-a63e6b5` |

**Écart zipball vs une mesure antérieure** (SHA cités `506a5b98…` / `ee8c29e0…`).  
Les SHA **mesurés aujourd’hui** diffèrent (les zipballs GitHub ne sont pas byte-stables : horodatage / commentaire ZIP).  
Les **commits de tag** sont identiques à ceux de la mesure antérieure. L’autorité d’exécution est le SHA des **XSLT extraits**, pas celui du zipball.

Licence des artefacts France_RFE : Apache 2.0 (`LICENSE` du zipball) ; en-tête Schematron Flux2 : EUPL 1.4.0 (citation brute du fichier).

README officiel du tag `.03` : versioning 1.4.x = XP Z12-012 1.4 ; `.03` « Following different issues #17, #19, #21, #22, #25 ». Le blurb n’est **pas** la source de vérité — le diff des `.sch` / l’exécution l’est.

---

## Artefacts réellement exécutés (SHA avant tout test)

| XSLT | Tag | SHA256 |
|---|---|---|
| `vendor/v1.4.0.02/ubl-flux2/BR-FR-Flux2-Schematron-UBL.xslt` | v1.4.0.02 | `e308eade08e21ad69881328a2c14290ec2877b02b7ec873531baf82aae2f6628` |
| `vendor/v1.4.0.03/ubl-flux2/BR-FR-Flux2-Schematron-UBL.xslt` | v1.4.0.03 | `4a54e8b363907b7ca13c6d63302910aa7e42681fdaa6d16ef18b9a414973c09c` |
| `vendor/v1.4.0.02/cii-flux2/BR-FR-Flux2-Schematron-CII.xslt` | v1.4.0.02 | `a5509334f70a3c8268f0339a968c49185c17cba60f71c8f6fc095deba94e6438` |
| `vendor/v1.4.0.03/cii-flux2/BR-FR-Flux2-Schematron-CII.xslt` | v1.4.0.03 | `a5509334f70a3c8268f0339a968c49185c17cba60f71c8f6fc095deba94e6438` |

CII Flux2 **byte-identical** `.02` / `.03`.  
Les copies EN16931 et EXTENDED-CTC-FR de Flux2 UBL sont byte-identical **à l’intérieur d’un même tag**.  
Le runner refuse un XSLT dont le SHA ne correspond pas (voir `scripts/validate.py`).

---

## Objectif A — UBL BT-128 `.02` vs `.03`

### 1. Diff fichier (pas le blurb)

Fichiers : `BR-FR-Flux2-Schematron-UBL.sch` (même octets dans EN16931 et EXTENDED-CTC-FR d’un tag).  
Citation brute : `diffs/BT-128-BR-FR-01-02-03.txt`.

**`.02` `BR-FR-02_EXT-FR-FE-136`**

```
context = ubl:Invoice/cac:InvoiceLine/cac:DocumentReference/cbc:ID
          | cn:CreditNote/cac:CreditNoteLine/cac:DocumentReference/cbc:ID
test    = custom:is-valid-id-format(.)
```

Ce contexte UBL est **BT-128** (DocumentReference de ligne, TypeCode 130 dans EN16931).  
`is-valid-id-format` refuse tout espace (`not(matches($id, ' '))`).

**`.03` `BR-FR-02_EXT-FR-FE-136`**

```
context = ubl:Invoice/cac:InvoiceLine/cac:BillingReference/cac:InvoiceDocumentReference/cbc:ID
          | cn:CreditNote/cac:CreditNoteLine/cac:BillingReference/cac:InvoiceDocumentReference/cbc:ID
test    = custom:is-valid-id-format(.)   (inchangé)
```

Le contexte a quitté BT-128 pour EXT-FR-FE-136 (facture antérieure en ligne).  
Même déplacement pour `BR-FR-03_EXT-FR-FE-138` (date).  
`BR-FR-01_*136` : `.02` chemin `BillingReference/cac:DocumentReference` (XSD invalide) + id `BR-FR-01_BT-EXT-FR-FE-136-2` ; `.03` `InvoiceDocumentReference` + id `BR-FR-01_EXT-FR-FE-136-2`.

Changement de test **visible**. Une fixture a donc été construite.

### 2. Reproduction (même XML, deux XSLT)

Fixture : `objective-a/ubl-bt128-espace.xml`  
= `fixtures/ubl-synth-S1-bt128-pass.xml` (0 failed-assert sur `.02` **et** `.03`) avec **une** substitution :

`InvoiceLine/cac:DocumentReference/cbc:ID` : `OBJET-FICTIF-001` → `OBJET FICTIF 001`.

| Exécution | failed-assert | id |
|---|---:|---|
| XSLT `.02` | **1** | `BR-FR-02_EXT-FR-FE-136` |
| XSLT `.03` | **0** | — |

SVRL côte à côte : `objective-a/receipts-02/` et `objective-a/receipts-03/`  
(également `receipts/v1.4.0.02/objective-a/` et `receipts/v1.4.0.03/objective-a/`).

Citation brute `.02` (texte d’assert **tel quel** dans l’artefact — le libellé dit `BR-FR-03/EXT-FR-FE-136`, l’attribut `id` dit `BR-FR-02_EXT-FR-FE-136`) :

```
<svrl:failed-assert test="custom:is-valid-id-format(.)"
                    id="BR-FR-02_EXT-FR-FE-136"
                    flag="fatal"
                    location="…/InvoiceLine[1]/DocumentReference[1]/ID[1]">
  … Valeur actuelle : "OBJET FICTIF 001".
```

### 3. Verdict Objectif A

**faux positif corrigé** — après reproduction, pas d’après le body de release.

Le document avec espace dans BT-128 est rejeté en fatal par `.02` sur une règle étiquetée EXT-FR-FE-136, et n’est plus visé par cette règle en `.03`.

---

## Objectif B — mini jeu BR-FR (discipline Mission 13)

Artefact de verdict : **Flux2 v1.4.0.03** (UBL ou CII selon le fichier). Version enregistrée dans chaque recette.

Flux2 s’applique dès qu’un `ubl:Invoice` / `rsm:CrossIndustryInvoice` est présent : pas de garde sur l’URI de spécification. Les exemples CEN « core » sans `#PMT#` / `ProfileID` / SIREN `0002` échouent BR-FR (non rejoués ici — hors périmètre, et ils ne sont pas dans ce dossier). Les fixtures de ce pack portent un `CustomizationID` / guideline CTC-FR **et** les champs que Flux2 exige réellement (`ProfileID` ∈ B1/S1/…, notes `#PMT#` `#PMD#` `#AAB#`, SIREN 9 chiffres, EndpointID).

### Originaux (verrouillés, jamais réécrits)

`sha256sum -c fixtures/SHA256SUMS` : 4 × OK après tout le travail.

| Fixture | SHA256 | Syntaxe | `.02` | `.03` |
|---|---|---|---|---|
| `ubl-synth-S1-pass.xml` | `d544fc2c0f474bb58bf37bc738d1f2f4193ad91be7ac40b6e774150fd41422a9` | UBL | 0 | 0 |
| `ubl-synth-S1-bt128-pass.xml` | `e15abf78974f5813ec20511b2f828e7626dd111e787aff863c042dc9d9ac7d77` | UBL | 0 | 0 |
| `ubl-synth-B1-pass.xml` | `a491abede5640cca6f478d114127081964f2eb2341e5ae4d4aa08961f8c0b85d` | UBL | 0 | 0 |
| `cii-synth-S1-pass.xml` | `11dffcf8f4b8769995a44b2e39d81ab45aee10848360b6abc44036cb791172f0` | CII | 0 | 0 |

Recettes : `receipts/v1.4.0.02/fixtures/` et `receipts/v1.4.0.03/fixtures/`.

### Mutants (une ligne, ids SVRL officiels)

| Mutant | Original | Mutation | fail | ids |
|---|---|---|---:|---|
| `ubl-id-espace.xml` | S1-pass | BT-1 avec espaces | 2 | `BR-FR-01_BT-1-2`, `BR-FR-02_BT-1` |
| `ubl-date-annee.xml` | S1-pass | BT-2 année 1999 | 1 | `BR-FR-03_BT-2` |
| `ubl-type-invalide.xml` | S1-pass | BT-3 = 999 | 1 | `BR-FR-04_BT-3` |
| `ubl-note-pmt-absent.xml` | S1-pass | `#PMT#` retiré | 1 | `BR-FR-05_BT-22-1` |
| `ubl-profile-invalide.xml` | S1-pass | BT-23 = `XX` | 1 | `BR-FR-08_BT-23` |
| `ubl-siren-vendeur-court.xml` | S1-pass | BT-30 8 chiffres | 2 | `BR-FR-10_BT-30`, `BR-FR-32-LEGALID` |
| `ubl-tva-taux.xml` | S1-pass | BT-119 = 21.00 | 1 | `BR-FR-16_BT-119` |
| `cii-id-espace.xml` | CII-pass | BT-1 avec espaces | 1 | `BR-FR-02_BT-1` |

8 fichiers, **8 × ≥1 failed-assert**, 0 vert. Détail : `mutants/DIFFS.md`. SVRL : `mutants/receipts/v1.4.0.03/`.

---

## Reproduire

```bash
cd brfr  # from repository root
python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt
.venv/bin/python scripts/validate.py --dir fixtures --out-dir receipts/v1.4.0.03/fixtures --tag 03
.venv/bin/python scripts/validate.py --dir mutants --out-dir mutants/receipts/v1.4.0.03 --tag 03
.venv/bin/python scripts/validate.py --dir objective-a --out-dir receipts/v1.4.0.02/objective-a --tag 02
.venv/bin/python scripts/validate.py --dir objective-a --out-dir receipts/v1.4.0.03/objective-a --tag 03
sha256sum -c fixtures/SHA256SUMS
```

---

## Limites (honnêtes)

- **Flux2 seulement.** Les XSLT `EXTENDED-CTC-FR-*.xslt`, EN16931 préprocessés FNFE, CDAR et Factur-X 1.09.2 n’ont **pas** été le moteur de verdict de ce pack (`non-mesure` pour BR-FREXT / CDV / Factur-X).
- **Pas de XSD.** Aucune validation `cvc-*`.
- **Pas les exemples officiels Annexe B** (ZIP du tag) : ils portent des identifiants de démo FNFE ; ce pack n’en redistribue aucun octet. Structure lue uniquement pour confirmer `ProfileID` / `CustomizationID` / forme BT-128.
- **XP Z12-012 texte AFNOR :** non récupéré (payant). Aucune citation d’Annexe A.
- Issue #25 (BY/SE BR-CL-10 UBL) : **hors Objectif A** ; non rejouée ici.
- Libellé d’assert `.02` `BR-FR-02_EXT-FR-FE-136` : le texte dit `[BR-FR-03/EXT-FR-FE-136]` — décalage texte/id **dans l’artefact**, cité tel quel.
- Zipball SHA ≠ mesure antérieure : reporté ci-dessus ; commits de tag et SHA XSLT font foi.

---

## Interdits respectés

- pas de donnée client réelle
- fixtures CEN du dépôt racine (`fixtures/`) non touchées
- pas d'usage du nom FNFE comme marque
