# Angles morts BR-FR Flux2 v1.4.0.03 — ce que le XSLT officiel France_RFE ne teste pas (ou teste trop peu)

**Date :** 16 août 2026 (Europe/Paris) — 16 Aug 2026 PT
**Moteur :** SaxonC-HE 13.0 (`saxonche==13.0.0`)
**XSLT :** `vendor/v1.4.0.03/ubl-flux2/BR-FR-Flux2-Schematron-UBL.xslt` SHA256 `4a54e8b363907b7ca13c6d63302910aa7e42681fdaa6d16ef18b9a414973c09c`
**XSLT :** `vendor/v1.4.0.03/cii-flux2/BR-FR-Flux2-Schematron-CII.xslt` SHA256 `a5509334f70a3c8268f0339a968c49185c17cba60f71c8f6fc095deba94e6438`
**Schematron cité :** `vendor/v1.4.0.03/ubl-flux2/BR-FR-Flux2-Schematron-UBL.sch` / `…/cii-flux2/BR-FR-Flux2-Schematron-CII.sch` (tag France_RFE `v1.4.0.03`, commit `a63e6b538bdaff460f17c38dc1bc5455cf1ba35a`)
**Scope:** documented Flux2 gaps. Synthetic probes only.

Sources primaires seulement pour les claims normatifs : les `.sch` à côté des XSLT exécutés. Les notes de travail ne sont pas une autorité normative. XP Z12-012 (AFNOR, payant) n’a **pas** été récupéré — aucune citation d’Annexe A.

Ce n’est **pas** un scoop « France 2026 » au-delà de ce qui est démontré ci-dessous sur Flux2 v1.4.0.03.

## Discipline

- Une ligne sémantique par sonde (copie, jamais l’original). Détail : `gaps-fr/DIFFS.md`.
- Originaux dans `fixtures/` **non modifiés**. Contrôle final : `sha256sum -c fixtures/SHA256SUMS` (4 × OK).
- Les fixtures CEN racine (`fixtures/`) n'ont pas été modifiées.
- Un verdict **angle mort** exige (1) le texte/test officiel de la règle et (2) un contre-test machine à 0 `svrl:failed-assert` pertinent.
- Sinon : **observation** (pas de règle qui *prétend* couvrir le cas) ou **couvert** (un `failed-assert` a tiré) ou **erreur moteur** (pas de SVRL).
- Distinction explicite : « la règle devrait normativement couvrir ce cas » vs « simple attente de test ».
- Les `id` viennent de l’attribut `id` du SVRL officiel. Les octets des factures ne sont pas journalisés.

## Comptage (30 sondes)

| Classe | n | Sens |
|---|---:|---|
| **Angle mort** | **5** | règle officielle citée + contre-test vert (0 failed-assert pertinent) |
| **Observation** | **12** | vert, mais aucune règle Flux2 .03 ne *prétend* tester le cas |
| **Couvert** | **13** | `svrl:failed-assert` a tiré — ce n’est pas un trou |
| **Erreur moteur** | **0** | — |

3 *findings* d’angle mort (plusieurs sondes pour BR-FR-05). 12 observations. 13 contrôles positifs.

`gaps-fr/receipts/RESULTS.sha256` (30 XML) = `a89691ce4fff7ea74985ee5ae1f90dcba6134840acc5d4d3a02758b940970b84`

## Table des sondes

Abréviations source : **S1** = `ubl-synth-S1-pass.xml` ; **BT** = `ubl-synth-S1-bt128-pass.xml` ; **CII** = `cii-synth-S1-pass.xml`.

| Sonde | Src | Mutation (une ligne) | fail | ids | Classe | SVRL |
|---|---|---|---:|---|---|---|
| `gaps-fr/cii-date-suffix.xml` | CII | BT-2 `20260816` → `20260816XX` | 0 | — | **angle mort** BR-FR-03 | `gaps-fr/receipts/cii-date-suffix.svrl.xml` |
| `gaps-fr/ubl-pmt-vide.xml` | S1 | `#PMT#FICTIF` → `#PMT#` | 0 | — | **angle mort** BR-FR-05 | `gaps-fr/receipts/ubl-pmt-vide.svrl.xml` |
| `gaps-fr/ubl-pmd-ws.xml` | S1 | `#PMD#FICTIF` → `#PMD#` + 3 espaces | 0 | — | **angle mort** BR-FR-05 | `gaps-fr/receipts/ubl-pmd-ws.svrl.xml` |
| `gaps-fr/cii-pmt-vide.xml` | CII | Content PMT → vide | 0 | — | **angle mort** BR-FR-05 | `gaps-fr/receipts/cii-pmt-vide.svrl.xml` |
| `gaps-fr/ubl-siren-espaces.xml` | S1 | BT-30 → ` 000000000 ` | 0 | — | **angle mort** BR-FR-10/32 | `gaps-fr/receipts/ubl-siren-espaces.svrl.xml` |
| `gaps-fr/ubl-siren-123456789.xml` | S1 | BT-30 → `123456789` (Luhn ≠ 0) | 0 | — | observation | `gaps-fr/receipts/ubl-siren-123456789.svrl.xml` |
| `gaps-fr/cii-siren-123456789.xml` | CII | BT-30 → `123456789` | 0 | — | observation | `gaps-fr/receipts/cii-siren-123456789.svrl.xml` |
| `gaps-fr/ubl-pmt-dot.xml` | S1 | `#PMT#FICTIF` → `#PMT#.` | 0 | — | observation | `gaps-fr/receipts/ubl-pmt-dot.svrl.xml` |
| `gaps-fr/ubl-pmt-na.xml` | S1 | `#PMT#FICTIF` → `#PMT#n/a` | 0 | — | observation | `gaps-fr/receipts/ubl-pmt-na.svrl.xml` |
| `gaps-fr/cii-pmt-dot.xml` | CII | Content PMT → `.` | 0 | — | observation | `gaps-fr/receipts/cii-pmt-dot.svrl.xml` |
| `gaps-fr/cii-pmt-na.xml` | CII | Content PMT → `n/a` | 0 | — | observation | `gaps-fr/receipts/cii-pmt-na.svrl.xml` |
| `gaps-fr/ubl-bt128-espace.xml` | BT | BT-128 `OBJET-FICTIF-001` → `OBJET FICTIF 001` | 0 | — | observation | `gaps-fr/receipts/ubl-bt128-espace.svrl.xml` |
| `gaps-fr/ubl-bt24-garbage.xml` | S1 | BT-24 URI → `urn:example:not-a-ctc-fr-profile` | 0 | — | observation | `gaps-fr/receipts/ubl-bt24-garbage.svrl.xml` |
| `gaps-fr/ubl-id-hyphen.xml` | S1 | BT-1 → `SYNTH-BRFR-0001-OK` | 0 | — | observation | `gaps-fr/receipts/ubl-id-hyphen.svrl.xml` |
| `gaps-fr/ubl-s1-type-381.xml` | S1 | BT-3 `380` → `381` | 0 | — | observation | `gaps-fr/receipts/ubl-s1-type-381.svrl.xml` |
| `gaps-fr/ubl-siren-meme.xml` | S1 | BT-47 = BT-30 `000000000` | 0 | — | observation | `gaps-fr/receipts/ubl-siren-meme.svrl.xml` |
| `gaps-fr/ubl-vat-z-20.xml` | S1 | BT-118 `S` → `Z` (20.00 inchangé) | 0 | — | observation | `gaps-fr/receipts/ubl-vat-z-20.svrl.xml` |
| `gaps-fr/ubl-siren-court.xml` | S1 | BT-30 → `12345678` | 2 | `BR-FR-10_BT-30`, `BR-FR-32-LEGALID` | **couvert** | `gaps-fr/receipts/ubl-siren-court.svrl.xml` |
| `gaps-fr/ubl-siren-lettres.xml` | S1 | BT-30 → `AAAAAAAAA` | 2 | `BR-FR-10_BT-30`, `BR-FR-32-LEGALID` | **couvert** | `gaps-fr/receipts/ubl-siren-lettres.svrl.xml` |
| `gaps-fr/cii-siren-lettres.xml` | CII | BT-30 → `AAAAAAAAA` | 2 | `BR-FR-10_BT-30`, `BR-FR-32-LEGALID` | **couvert** | `gaps-fr/receipts/cii-siren-lettres.svrl.xml` |
| `gaps-fr/ubl-id-lead-space.xml` | S1 | BT-1 préfixe espace | 2 | `BR-FR-01_BT-1-2`, `BR-FR-02_BT-1` | **couvert** | `gaps-fr/receipts/ubl-id-lead-space.svrl.xml` |
| `gaps-fr/ubl-id-trail-space.xml` | S1 | BT-1 suffixe espace | 2 | `BR-FR-01_BT-1-2`, `BR-FR-02_BT-1` | **couvert** | `gaps-fr/receipts/ubl-id-trail-space.svrl.xml` |
| `gaps-fr/ubl-id-nbsp.xml` | S1 | BT-1 NBSP U+00A0 | 2 | `BR-FR-01_BT-1-2`, `BR-FR-02_BT-1` | **couvert** | `gaps-fr/receipts/ubl-id-nbsp.svrl.xml` |
| `gaps-fr/ubl-id-long.xml` | S1 | BT-1 36 caractères | 1 | `BR-FR-01_BT-1-1` | **couvert** | `gaps-fr/receipts/ubl-id-long.svrl.xml` |
| `gaps-fr/ubl-date-2026-02-31.xml` | S1 | BT-2 → `2026-02-31` | 1 | `BR-FR-03_BT-2` | **couvert** | `gaps-fr/receipts/ubl-date-2026-02-31.svrl.xml` |
| `gaps-fr/cii-date-20260231.xml` | CII | BT-2 → `20260231` | 1 | `BR-FR-03_BT-2` | **couvert** | `gaps-fr/receipts/cii-date-20260231.svrl.xml` |
| `gaps-fr/cii-date-20260431.xml` | CII | BT-9 → `20260431` | 2 | `BR-FR-03_BT-9`, `BR-FR-CO-07_BT-9` | **couvert** | `gaps-fr/receipts/cii-date-20260431.svrl.xml` |
| `gaps-fr/ubl-date-order.xml` | S1 | BT-9 → `2026-08-01` (&lt; BT-2) | 1 | `BR-FR-CO-07_BT-9` | **couvert** | `gaps-fr/receipts/ubl-date-order.svrl.xml` |
| `gaps-fr/ubl-b4-acompte.xml` | S1 | BT-23 `B4` + BT-3 `386` | 1 | `BR-FR-CO-08_BT-23` | **couvert** | `gaps-fr/receipts/ubl-b4-acompte.svrl.xml` |
| `gaps-fr/ubl-vat-20-000.xml` | S1 | BT-119 `20.00` → `20.000` | 2 | `BR-FR-16_BT-119`, `BR-FR-DEC-04_BT-119` | **couvert** | `gaps-fr/receipts/ubl-vat-20-000.svrl.xml` |

---

## FINDING 1 — BR-FR-03 CII tronque la date aux 8 premiers caractères

**Contre-test (rejoué) :** copie de `cii-synth-S1-pass.xml`, BT-2 `20260816` → `20260816XX`. XSLT Flux2 CII v1.4.0.03 : **0 `svrl:failed-assert`** (59 fired-rule). Recette : `gaps-fr/receipts/cii-date-suffix.svrl.xml`.

**Règle officielle (CII),** `BR-FR-Flux2-Schematron-CII.sch` L262–271, contexte `rsm:ExchangedDocument/ram:IssueDateTime/udt:DateTimeString` :

```
id="BR-FR-03_BT-2"
test="custom:is-valid-date-format(.)"
BR-FR-03/BT-2 : La date d’émission (udt:DateTimeString) doit contenir une année comprise entre 2000 et 2099, au format AAAAMMJJ.
```

**Fonction officielle (CII),** L38–65 — commentaire et implémentation :

```
<!-- Tronque la date aux 8 premiers caractères -->
<xsl:variable name="shortDate" select="substring($date, 1, 8)"/>
<xsl:variable name="isFormatValid" select="matches($shortDate, '^20\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])$')"/>
… maxDay (calendrier + bissextile) …
<xsl:sequence select="$isFormatValid and $day le $maxDay"/>
```

`substring('20260816XX', 1, 8)` = `20260816` : format et calendrier OK. Le suffixe n’entre pas dans le `test`.

**Contrastes (couverts) — le calendrier, lui, tire :**

- CII BT-2 `20260231` (31 février) → **1 failed-assert `BR-FR-03_BT-2`**
- CII BT-9 `20260431` (31 avril) → **`BR-FR-03_BT-9`** + `BR-FR-CO-07_BT-9`
- UBL BT-2 `2026-02-31` → **1 failed-assert `BR-FR-03_BT-2`**

La fonction UBL (même fichier de règles, L38–64 du `.sch` UBL) **n’a pas** de `substring` : le regex est ancré `^20\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$` sur la chaîne entière, puis le même calendrier. Un suffixe UBL casserait le motif. Le trou est **CII seulement**, et ce n’est **pas** le trou EN16931 CII-DT-097 (regex sans calendrier) : Flux2 .03 *a* un calendrier.

**Pourquoi aucun failed-assert pertinent :** le `test` ne voit que 8 octets. `20260816XX` n’est pas AAAAMMJJ.

**Distinction :** **la règle devrait normativement couvrir ce cas.** Le texte dit « au format AAAAMMJJ ». `20260816XX` n’est pas ce format. Ce n’est pas une attente extra-normative (pas une demande de fuseau, ni de `xs:date` UBL). Le commentaire « Tronque la date » est dans l’artefact officiel : le test est volontairement plus court que le texte.

---

## FINDING 2 — BR-FR-05 teste le jeton PMT/PMD, pas le texte de la mention

**Contre-tests (0 failed-assert, 59 fired-rule) :**

- UBL `#PMT#FICTIF` → `#PMT#` (rien après le code)
- UBL `#PMD#FICTIF` → `#PMD#` + trois espaces
- CII `ram:Content` de la note PMT → vide (`SubjectCode` PMT conservé)

**Règle officielle (UBL),** `BR-FR-Flux2-Schematron-UBL.sch` L411–424 :

```
<title>BR-FR-05 — Présence obligatoire des mentions légales dans les notes (BG-3)</title>
<let name="allNotes" value="string-join(./cbc:Note, '')"/>
id="BR-FR-05_BT-22-1"  test="contains($allNotes, '#PMT#')"
[BR-FR-05/BT-22] : La mention relative aux frais de recouvrement (code PMT) est absente. Elle est obligatoire dans les notes (BG-3).
id="BR-FR-05_BT-22-2"  test="contains($allNotes, '#PMD#')"
[BR-FR-05/BT-22] : La mention relative aux pénalités de retard (code PMD) est absente. Elle est obligatoire dans les notes (BG-3).
```

**Règle officielle (CII),** `BR-FR-Flux2-Schematron-CII.sch` L402–409 :

```
id="BR-FR-05_BT-22_PMT"  test="exists($notes[ram:SubjectCode = 'PMT'])"
BR-FR-05/BT-22 : La mention relative aux frais de recouvrement (code PMT) est absente. Elle est obligatoire dans les notes (BG-1).
```

Aucune assert Flux2 .03 ne lit le texte après `#PMT#` / `#PMD#` / `#AAB#`, ni `ram:Content`. BR-FR-06 ne teste que l’unicité du jeton.

**Contrôle négatif (déjà dans `mutants/`, pas rejoué ici comme finding) :** retirer `#PMT#` → `BR-FR-05_BT-22-1`. La règle *lit* bien les notes ; elle est muette dès que le code est présent.

**Pourquoi aucun failed-assert pertinent :** `#PMT#` ∈ `string-join(Note)` ; CII `exists(… SubjectCode='PMT')` reste vrai avec Content vide.

**Distinction :** **la règle devrait normativement couvrir** l’absence de *texte* de mention. Le titre dit « mentions légales » ; l’assert dit « la mention relative aux frais de recouvrement … est obligatoire ». Un code sans corps (`#PMT#`, Content vide, `#PMD#` + blancs) n’est pas une mention de frais de recouvrement / de pénalités. Ce n’est pas une attente que Flux2 relise le Code de commerce (libellé des 40 €, taux légal, etc.) : voir les observations `#PMT#.` / `n/a` ci-dessous.

---

## FINDING 3 — BR-FR-10 / BR-FR-32 acceptent un SIREN paddé d’espaces

**Contre-test :** BT-30 vendeur `000000000` → ` 000000000 ` (espace de chaque côté). **0 failed-assert** (59 fired-rule). Recette : `gaps-fr/receipts/ubl-siren-espaces.svrl.xml`.

**Règle officielle (UBL),** L554–562 et pattern `BR-FR-32` :

```
<title>BR-FR-10 — SIREN du vendeur obligatoire et valide (BT-30)</title>
test="$siren and matches(normalize-space($siren), '^\d{9}$')"
[BR-FR-10/BT-30] : Le SIREN du vendeur (CompanyID[@schemeID='0002']) est obligatoire et doit être composé exactement de 9 chiffres.

<title>BR-FR-32 — Le SIREN contient exactement 9 chiffres </title>
test="matches(normalize-space(.), '^\d{9}$')"
[BR-FR-32/LEGALID] : Tout identifiant légal d'une Partie avec schemeID = '0002' DOIT être composé de 9 chiffres.
```

**Pourquoi aucun failed-assert pertinent :** `normalize-space(' 000000000 ')` = `000000000`, qui matche `^\d{9}$`. La valeur XML a 11 caractères.

**Contrastes (couverts) :**

- 8 chiffres `12345678` → `BR-FR-10_BT-30` + `BR-FR-32-LEGALID`
- 9 lettres `AAAAAAAAA` → les mêmes ids (UBL et CII)

Les règles *lisent* le champ. Elles sont muettes dès que, *après trim*, il reste 9 chiffres.

**Distinction :** **la règle devrait normativement couvrir** un jeton qui n’est pas « exactement 9 chiffres ». BR-FR-01/02 savent refuser un espace en tête/fin sur BT-1 (`not(starts-with($id,' '))`, `not(matches($id,' '))`). BR-FR-10/32 ont choisi `normalize-space`. Ce n’est pas une demande de clé Luhn (voir observation `123456789`).

---

## Observations (vert, pas d’angle mort)

Aucune de ces sondes n’a de règle officielle dont le *texte* prétend tester le cas.

### Corps SIREN / clé Luhn (`123456789`)

UBL et CII : BT-30 `000000000` → `123456789` (9 chiffres, Luhn mod 10 ≠ 0) — 0 fail.

Le SHALL de BR-FR-10 / BR-FR-32 est « 9 chiffres ». Le mot « valide » du *titre* BR-FR-10 et de la clausule « Veuillez renseigner un identifiant SIREN valide » ne formule pas une clé INSEE. Aucune fonction Luhn dans le `.sch`. La fixture officielle du pack porte déjà `000000000` (9 zéros) et est 0-failed-assert.

**Distinction :** **simple attente de test.** Un contrôle Luhn serait une règle *nouvelle*. (La consigne : 9 chiffres « garbage » n’est un angle mort que si une règle citée prétend plus que la longueur.)

### PMT/PMD avec un corps factice (`.`, `n/a`)

`#PMT#.`, `#PMT#n/a`, CII Content `.` / `n/a` : 0 fail.

Le jeton / `SubjectCode` est présent *et* un texte non vide existe. Aucune assert Flux2 n’exige un libellé légal (indemnité 40 €, taux, etc.).

**Distinction :** simple attente de test (qualité rédactionnelle de la mention).

### BT-128 espace sur `.03` (Mission 17, pas un trou nouveau)

`InvoiceLine/cac:DocumentReference/cbc:ID` = `OBJET FICTIF 001` : 0 fail sur `.03` (60 fired-rule).

BR-FR-01/02 `.03` portent sur `InvoiceLine/cac:BillingReference/cac:InvoiceDocumentReference/cbc:ID` (EXT-FR-FE-136), plus sur BT-128. Le texte `.03` ne *prétend* plus formater BT-128. Reproduit ici pour ne pas le reclasser angle mort.

### BT-24 / CustomizationID

URI CTC-FR remplacé par `urn:example:not-a-ctc-fr-profile` : 0 fail. Flux2 n’a pas d’assert sur BT-24 (le README du pack le notait déjà : BR-FR-08 teste BT-23 / `ProfileID`).

### Tiret dans BT-1

`SYNTH-BRFR-0001-OK` : 0 fail. `is-valid-id-format` autorise `-`. Le texte BR-FR-02 le dit.

### Type 381 sur une facture UBL S1

`InvoiceTypeCode` `380` → `381`, racine toujours `ubl:Invoice` : 0 fail.

BR-FR-04 : liste unique `380 … 381 … 503` sur `InvoiceTypeCode | CreditNoteTypeCode`. Aucune règle Flux2 n’interdit `381` sur une facture (contrairement à EN16931 UBL BR-CL-01, listes disjointes).

**Distinction :** observation. Le code est dans la liste.

### SIREN vendeur = SIREN acheteur

BT-47 → `000000000` : 0 fail. Aucune assert « les deux parties distinctes ».

### Catégorie TVA Z + taux 20 %

BT-118 `S` → `Z`, `Percent` 20.00 inchangé : 0 fail.

BR-FR-15 = liste de catégories ; BR-FR-16 = liste de taux ; pas de cohérence catégorie↔taux (pas d’équivalent Flux2 de BR-Z-03 / BR-S-05 EN16931).

### Fonction `is-valid-eas-code` jamais appelée

Le `.sch` définit `custom:is-valid-eas-code` (liste EAS). Aucun `assert` ne l’utilise. BR-FR-12/13 = présence de l’EndpointID seulement. Pas d’angle mort : aucune règle ne *prétend* valider le scheme EAS.

---

## Contrôles positifs (rappel)

Ces `failed-assert` montrent que les filets voisins tirent. Ce ne sont pas des findings.

| Famille | Ce qui tire |
|---|---|
| SIREN trop court / lettres | `BR-FR-10_BT-30`, `BR-FR-32-LEGALID` |
| BT-1 espace / NBSP | `BR-FR-01_BT-1-2`, `BR-FR-02_BT-1` |
| BT-1 36 caractères | `BR-FR-01_BT-1-1` (`string-length(.) le 35`) |
| Date calendaire impossible | `BR-FR-03_BT-2` / `_BT-9` (UBL **et** CII) |
| Échéance &lt; émission | `BR-FR-CO-07_BT-9` |
| Cadre B4 + type acompte 386 | `BR-FR-CO-08_BT-23` |
| Taux `20.000` | `BR-FR-16_BT-119` (liste chaînes) + `BR-FR-DEC-04_BT-119` (max 2 décimales / 4 positions) |

---

## Reproduire

```bash
cd brfr  # from repository root
.venv/bin/python scripts/validate.py --dir gaps-fr --out-dir gaps-fr/receipts --tag 03
sha256sum -c fixtures/SHA256SUMS
```

Le runner refuse un XSLT dont le SHA ≠ `4a54e8b3…` (UBL) / `a5509334…` (CII).

---

## `sha256sum -c fixtures/SHA256SUMS` (après tout travail)

Exécuté depuis `fixtures/` le 16 Aug 2026 PT :

```
cii-synth-S1-pass.xml: OK
ubl-synth-B1-pass.xml: OK
ubl-synth-S1-bt128-pass.xml: OK
ubl-synth-S1-pass.xml: OK
```

SHA256 des 4 fichiers = table du README / `SHA256SUMS` racine (inchangés). Aucune écriture dans `fixtures/`. Les fixtures CEN racine (`fixtures/`) n'ont pas été modifiées.

---

## Méthode (rappel)

Généralisation du trou BR-CO-09 (Mission 15) : pour chaque famille (corps SIREN, mention PMT/PMD, cohérence inter-champs, format d’ID, date, BT-128), (1) lire le `test` et le texte officiels dans le `.sch` v1.4.0.03, (2) muter une copie d’une fixture synthétique d’une ligne, (3) rejouer le XSLT Flux2 .03, (4) classer seulement si le texte de règle *et* le contre-test s’accordent. Les 13 `failed-assert` obtenus sont des *contrôles*, pas des findings.

## Limites

- **Flux2 seulement.** EXTENDED-CTC-FR, EN16931 FNFE, CDAR, Factur-X 1.09.2 : `non-mesure`.
- **Pas de XSD.** Pas de `cvc-*`.
- **Pas les exemples Annexe B** du ZIP du tag (identifiants de démo FNFE, non redistribués).
- **XP Z12-012** non cité.
- CII Flux2 `.02` / `.03` byte-identical (déjà mesuré dans le README du pack) ; les sondes n’ont été jouées que sur `.03`.
