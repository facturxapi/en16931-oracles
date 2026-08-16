# Angles morts EN16931 1.3.16 — ce que le XSLT officiel ne teste pas (ou teste trop peu)

**Date :** 16 août 2026 (Europe/Paris) — 16 Aug 2026 PT
**Moteur :** SaxonC-HE 13.0 (`saxonche==13.0.0`)
**XSLT :** `vendor/en16931-1.3.16/xslt/EN16931-CII-validation.xslt` / `EN16931-UBL-validation.xslt`
**Schematron cité :** `/workspace/en16931-src/cii/schematron/preprocessed/EN16931-CII-validation-preprocessed.sch` et pendant UBL `…/ubl/schematron/preprocessed/EN16931-UBL-validation-preprocessed.sch` (release 1.3.16)
**Statut :** préparation, pas une publication. Aucun `git init`. Aucun site externe.

Sources primaires seulement pour les claims normatifs. Les notes `local-prep` ne sont pas une autorité — chaque test et chaque `id` ont été relus dans le sch/XSLT vendored, puis rejoués.

## Discipline

- Une ligne sémantique par sonde (copie, jamais l'original).
- Originaux dans `fixtures/` **non modifiés**. Contrôle final : `sha256sum -c fixtures/SHA256SUMS` (tous OK).
- Un verdict **angle mort** exige (1) le texte/test officiel de la règle et (2) un contre-test machine à 0 `svrl:failed-assert` pertinent.
- Sinon : **observation** (pas de règle qui *prétend* couvrir le cas) ou **couvert** (un `failed-assert` a tiré) ou **erreur moteur** (pas de SVRL).
- Distinction explicite : « la règle devrait normativement couvrir ce cas » vs « simple attente de test ».
- Les `id` viennent de l'attribut `id` du SVRL officiel. Les octets des factures ne sont pas journalisés.

## Comptage (23 sondes)

| Classe | n | Sens |
|---|---:|---|
| **Angle mort** | **8** | règle officielle citée + contre-test vert (0 failed-assert pertinent) |
| **Observation** | **8** | vert, mais aucune règle 1.3.16 ne *prétend* tester le cas |
| **Couvert** | **5** | `svrl:failed-assert` a tiré — ce n'est pas un trou |
| **Erreur moteur** | **2** | Saxon FORG0001, pas de SVRL (pas un passage silencieux) |

4 *findings* d'angle mort (plusieurs sondes par finding). 8 observations. 5 contrôles positifs. 2 erreurs `xs:decimal`.

## Table des sondes

| Sonde | Source | Mutation (une ligne) | fail | ids | Classe | SVRL |
|---|---|---|---:|---|---|---|
| `gaps/CII_business_example_Z-bt31-DE37.xml` | Z | L139 BT-31 `DE37/302/30168` → `DE37` | 0 | — | **angle mort** BR-CO-09 | `gaps/receipts/CII_business_example_Z-bt31-DE37.svrl.xml` |
| `gaps/CII_example5-bt31-NL1.xml` | ex5 | L232 BT-31 `NL16356706` → `NL1` | 0 | — | **angle mort** BR-CO-09 | `gaps/receipts/CII_example5-bt31-NL1.svrl.xml` |
| `gaps/CII_example5-bt48-DK1.xml` | ex5 | L266 BT-48 `DK16356607` → `DK1` | 0 | — | **angle mort** BR-CO-09 | `gaps/receipts/CII_example5-bt48-DK1.svrl.xml` |
| `gaps/ubl-tc434-creditnote1-bt31-BE00.xml` | ubl | L36 BT-31 `BE0000000196` → `BE00` | 0 | — | **angle mort** BR-CO-09 | `gaps/receipts/ubl-tc434-creditnote1-bt31-BE00.svrl.xml` |
| `gaps/ubl-tc434-creditnote1-bt31-A.xml` | ubl | L36 BT-31 → `A` | 0 | — | **angle mort** BR-CO-09 UBL (`contains` sans bornes) | `gaps/receipts/ubl-tc434-creditnote1-bt31-A.svrl.xml` |
| `gaps/CII_business_example_Z-date-20260231.xml` | Z | L20 BT-2 `20150109` → `20260231` | 0 | — | **angle mort** CII-DT-097 | `gaps/receipts/CII_business_example_Z-date-20260231.svrl.xml` |
| `gaps/CII_business_example_Z-date-20260431.xml` | Z | L183 échéance `20150109` → `20260431` | 0 | — | **angle mort** CII-DT-097 | `gaps/receipts/CII_business_example_Z-date-20260431.svrl.xml` |
| `gaps/CII_business_example_Z-dec-0.000.xml` | Z | L189 BT-110 `0.0` → `0.000` | 0 | — | **angle mort** BR-DEC-13 | `gaps/receipts/CII_business_example_Z-dec-0.000.svrl.xml` |
| `gaps/CII_business_example_Z-iban-badcheck.xml` | Z | L171 BT-84 dernier chiffre `0` → `1` (ISO 13616 mod97=28) | 0 | — | observation | `gaps/receipts/CII_business_example_Z-iban-badcheck.svrl.xml` |
| `gaps/ubl-tc434-creditnote1-iban-bad.xml` | ubl | L83 compte `…76` → `…77` (mod97=28) | 0 | — | observation | `gaps/receipts/ubl-tc434-creditnote1-iban-bad.svrl.xml` |
| `gaps/CII_example5-bt32-FC-XX.xml` | ex5 | L235 BT-32 `NL16356706` → `XX` | 0 | — | observation | `gaps/receipts/CII_example5-bt32-FC-XX.svrl.xml` |
| `gaps/CII_business_example_Z-bt30-X.xml` | Z | L130 BT-30 `57151520` → `X` | 0 | — | observation | `gaps/receipts/CII_business_example_Z-bt30-X.svrl.xml` |
| `gaps/CII_example5-bt29-gln1.xml` | ex5 | L204 BT-29 `5790000436101` → `1` (scheme 0088) | 0 | — | observation | `gaps/receipts/CII_example5-bt29-gln1.svrl.xml` |
| `gaps/CII_business_example_Z-bt46-X.xml` | Z | L143 BT-46 `10202` → `X` | 0 | — | observation | `gaps/receipts/CII_business_example_Z-bt46-X.svrl.xml` |
| `gaps/CII_business_example_Z-type-381.xml` | Z | L18 BT-3 `380` → `381` | 0 | — | observation | `gaps/receipts/CII_business_example_Z-type-381.svrl.xml` |
| `gaps/ubl-tc434-creditnote1-date-2026-02-31.xml` | ubl | L13 BT-2 `2019-09-23` → `2026-02-31` | 0 | — | observation | `gaps/receipts/ubl-tc434-creditnote1-date-2026-02-31.svrl.xml` |
| `gaps/CII_business_example_Z-bt31-A.xml` | Z | L139 BT-31 → `A` | 1 | `BR-CO-09` | **couvert** | `gaps/receipts/CII_business_example_Z-bt31-A.svrl.xml` |
| `gaps/CII_business_example_Z-date-20151399.xml` | Z | L20 BT-2 → `20151399` | 1 | `CII-DT-097` | **couvert** | `gaps/receipts/CII_business_example_Z-date-20151399.svrl.xml` |
| `gaps/CII_business_example_Z-dec-3frac.xml` | Z | L190 BT-112 `11693.87` → `11693.870` | 1 | `BR-DEC-14` | **couvert** | `gaps/receipts/CII_business_example_Z-dec-3frac.svrl.xml` |
| `gaps/CII_business_example_Z-dec-0.001.xml` | Z | L189 BT-110 `0.0` → `0.001` | 2 | `BR-DEC-13`, `BR-CO-14` | **couvert** | `gaps/receipts/CII_business_example_Z-dec-0.001.svrl.xml` |
| `gaps/ubl-tc434-creditnote1-type-380.xml` | ubl | L14 `381` → `380` | 1 | `BR-CL-01` | **couvert** | `gaps/receipts/ubl-tc434-creditnote1-type-380.svrl.xml` |
| `gaps/engine-errors/CII_business_example_Z-dec-1E100.xml` | Z | L190 BT-112 → `1E+100` | — | FORG0001 | erreur moteur | `gaps/engine-errors/receipts/CII_business_example_Z-dec-1E100.engine-error.txt` |
| `gaps/engine-errors/CII_business_example_Z-dec-sci.xml` | Z | L190 BT-112 → `1169387E-2` | — | FORG0001 | erreur moteur | `gaps/engine-errors/receipts/CII_business_example_Z-dec-sci.engine-error.txt` |

`gaps/receipts/RESULTS.sha256` (21 XML du lot, hors engine-errors) = `edc232f519a8a999c4c8d573eb0cacc6997135030053591fde766eff8954c364`

---

## FINDING 1 — BR-CO-09 ne teste que le préfixe pays (CII et UBL)

**Contre-test principal (rejoué, pas repris des notes) :** sur une copie de `CII_business_example_Z.xml`, BT-31 `DE37/302/30168` → `DE37`. XSLT 1.3.16 : **0 `svrl:failed-assert`** (106 fired-rule). Recette : `gaps/receipts/CII_business_example_Z-bt31-DE37.svrl.xml`.

Même silence, même règle, autres BT / syntaxes :

- BT-31 `NL16356706` → `NL1` (`CII_example5`) — 0 fail
- BT-48 `DK16356607` → `DK1` (`CII_example5`) — 0 fail
- UBL BT-31 `BE0000000196` → `BE00` — 0 fail

**Règle officielle (CII),** `EN16931-CII-validation-preprocessed.sch` L171–172, contexte `//ram:SpecifiedTaxRegistration/ram:ID[@schemeID='VA']` :

```
id="BR-CO-09"
test="contains(' 1A AD AE … ZW ', concat(' ', substring(.,1,2), ' '))"
[BR-CO-09]-The Seller VAT identifier (BT-31), the Seller tax representative VAT identifier (BT-63) and the Buyer VAT identifier (BT-48) shall have a prefix in accordance with ISO code ISO 3166-1 alpha-2 by which the country of issue may be identified. Nevertheless, Greece may use the prefix ‘EL’.
```

**Règle officielle (UBL),** même `id`, contexte `//cac:PartyTaxScheme[cac:TaxScheme/…='VAT']` :

```
test="( contains( ' 1A AD AE … ZW ', substring(cbc:CompanyID,1,2) ) )"
```

(texte BR-CO-09 identique). Aucune autre assert 1.3.16 ne contraint la longueur, le format national, ni la clé d'un identifiant `VA`.

**Pourquoi aucun failed-assert pertinent :** `substring(.,1,2)` de `DE37` / `NL1` / `DK1` / `BE00` ∈ liste ISO. Le corps après les 2 lettres n'entre pas dans le `test`. BR-S-02 / BR-Z-02 / BR-CO-26 ne testent que la *présence*.

**Contrôle négatif (couvert) :** même fixture Z, BT-31 → `A` (préfixe hors liste, avec les espaces CII) → **1 failed-assert `BR-CO-09`**. Donc la règle *lit* bien le champ ; elle est seulement trop courte.

**Distinction :** le *texte* de BR-CO-09 n'exige qu'un préfixe ISO. Le *test* implémente exactement cela. Appeler cela un angle mort, c'est dire : **la règle devrait normativement couvrir le corps** d'un identifiant TVA (BT-31/48/63 est un numéro de TVA, pas deux lettres). Ce n'est pas une « simple attente de test » cosmétique : `DE37` n'est pas un identifiant TVA DE (USt-IdNr = `DE` + 9 chiffres). Le document officiel Z porte déjà `DE37/302/30168` (forme Steuernummer) et est 0-failed-assert — le trou est dans le XSLT, pas dans notre mutation.

---

## FINDING 2 — UBL BR-CO-09 : `contains` sans bornes (lettre unique `A`)

**Contre-test :** `ubl-tc434-creditnote1` BT-31 → `A`. **0 failed-assert** (53 fired-rule).

**Test officiel UBL** (ci-dessus) : `contains( ' 1A AD AE … ', substring(cbc:CompanyID,1,2) )` — **sans** `concat(' ', …, ' ')`.

`substring('A',1,2)` = `A`. `contains(' 1A AD AE …', 'A')` est vrai (`A` apparaît dans `1A`, `AD`, `AE`, …).

**Contraste CII (couvert) :** le même `A` sur Z tire `BR-CO-09`, parce que CII teste `concat(' ', substring(.,1,2), ' ')` = `' A '`, absent de la liste.

**Distinction :** **la règle devrait normativement couvrir ce cas.** Le texte exige un préfixe ISO 3166-1 alpha-2. `A` n'en est pas un. Le test UBL est insuffisant (faux positif). Ce n'est pas une attente extra-normative.

---

## FINDING 3 — CII-DT-097 accepte des dates calendaires impossibles

**Contre-tests :**

- BT-2 `20150109` → `20260231` (31 février) — 0 failed-assert
- échéance `20150109` → `20260431` (31 avril) — 0 failed-assert

**Règle officielle,** sch CII L987–988, contexte `//udt:DateTimeString[@format = '102']` :

```
id="CII-DT-097"
test="matches(.,'^\s*(\d{4})(1[0-2]|0[1-9]){1}(3[01]|[12][0-9]|0[1-9]){1}\s*$')"
[CII-DT-097] - Date time string with format attribute 102 shall be YYYYMMDD.
```

Le regex autorise mois 01–12 et jour 01–31, sans calendrier (pas de 30/31 selon le mois, pas d'année bissextile). `20260231` et `20260431` matchent.

BR-03 ne teste que la présence : `normalize-space(…DateTimeString[@format='102']) != ''`.

**Contrôle négatif (couvert) :** `20151399` (mois 13, jour 99) → **1 failed-assert `CII-DT-097`**. La règle tire quand le *motif* casse ; elle est muette dès que le motif 8 chiffres « ressemble » à YYYYMMDD.

**Distinction :** le *texte* dit « shall be YYYYMMDD » (format 102). Un puriste du format 102 peut y voir une **simple attente de test** calendaire. BT-2 est pourtant une *date* d'émission : le 31 février n'en est pas une. **La règle devrait normativement couvrir** une date impossible, parce que c'est le seul filet format 102 du XSLT CII. Classé angle mort du *test* (insuffisant pour un BT date), pas d'une règle inventée.

**UBL (observation, pas angle mort) :** `IssueDate` → `2026-02-31` donne 0 failed-assert. BR-03 UBL = présence seulement (`normalize-space(cbc:IssueDate) != ''`). Aucune règle UBL 1.3.16 n'applique `xs:date` à BT-2 (BR-29/30 l'utilisent sur les *périodes*). Sans règle qui prétend valider le calendrier de BT-2, ce n'est pas un angle mort.

---

## FINDING 4 — BR-DEC-13 (numérique) laisse passer 3 décimales nulles

**Contre-test :** BT-110 `0.0` → `0.000` sur Z. **0 failed-assert.**

**Règle officielle,** sch CII L75 :

```
id="BR-DEC-13"
test="not(ram:TaxTotalAmount) or ram:TaxTotalAmount[(@currencyID = …InvoiceCurrencyCode and . = round(. * 100) div 100) or not (@currencyID = …)]"
[BR-DEC-13]-The allowed maximum number of decimals for the Invoice total VAT amount (BT-110) is 2.
```

Le *texte* limite à 2 décimales. Le *test* compare la valeur numérique à `round(. * 100) div 100`. `0.000 = 0`. Trois chiffres après la virgule passent.

**Contrastes (couverts) :**

- `0.001` → `BR-DEC-13` + `BR-CO-14` (la valeur n'est plus égale à l'arrondi / au Σ BT-117)
- BT-112 `11693.87` → `11693.870` → **`BR-DEC-14`** (`string-length(substring-after(.,'.'))<=2`, longueur 3)

BR-DEC-09/10/11/12/14/16/17/18 sont des tests *chaîne*. BR-DEC-13/15 sont des tests *numériques*. L'incohérence est dans le XSLT officiel.

**Distinction :** **la règle devrait normativement couvrir ce cas.** Le texte dit « maximum number of decimals … is 2 ». `0.000` a 3 décimales. Ce n'est pas une attente hors texte.

---

## Observations (vert, pas d'angle mort)

Aucune de ces sondes n'a de règle officielle dont le *texte* prétend tester le cas. Donc : observation, pas finding.

### IBAN BT-84 / clé ISO 13616

- Z : `DE12500105170648489890` (mod97=1, valide) → `…891` (mod97=28) — 0 fail.
- UBL : `BE91000000143476` (mod97=1) → `…77` (mod97=28) — 0 fail. (BT-81 = `1`, hors contexte 30/58 de BR-61.)

**Règles officielles les plus proches (CII L34–36) :**

```
id="BR-50" test="normalize-space(ram:IBANID) != '' or normalize-space(ram:ProprietaryID) != ''"
[BR-50]-A Payment account identifier (BT-84) shall be present if Credit transfer (BG-16) information is provided in the Invoice.

id="BR-61" test="(ram:IBANID) or (ram:ProprietaryID)"
[BR-61]-If the Payment means type code (BT-81) means SEPA credit transfer, Local credit transfer or Non-SEPA international credit transfer, the Payment account identifier (BT-84) shall be present.
```

Présence seulement. Aucune assert 1.3.16 ne calcule la clé IBAN, ni la longueur, ni le pays.

**Corpus officiel déjà démonstratif (0 failed-assert sur les fixtures) :**

- `CII_example5.xml` L357 : `<ram:IBANID>A</ram:IBANID>` (TypeCode 58, SEPA) — mod97 ≠ 1
- `CII_example5.xml` L351 : `DK1212341234123412` — mod97=55
- `XRechnung-O.xml` L202 : `<ram:IBANID>XX</ram:IBANID>`

**Distinction :** **simple attente de test.** BR-50/61 ne promettent pas ISO 13616. Un contrôle de clé serait une règle *nouvelle*, pas un trou d'une règle existante.

### Corps BT-32 / BT-30 / BT-29 / BT-46

| BT | Mutation | Règle la plus proche | Pourquoi 0 fail |
|---|---|---|---|
| BT-32 (`schemeID='FC'`) | `NL16356706` → `XX` | aucune sur le *corps* FC ; BR-CO-09 est borné à `@schemeID='VA'` ; BR-CL-11 exclut `SpecifiedTaxRegistration` | `XX` n'est jamais lu comme préfixe |
| BT-30 | `57151520` → `X` | BR-CO-26 = présence d'au moins un parmi BT-29/30/31 | présence conservée |
| BT-29 GlobalID `@schemeID='0088'` | GLN → `1` | BR-CL-10 = le *schemeID* ∈ ISO 6523 ICD | `0088` reste dans la liste ; pas de clé GLN |
| BT-46 | `10202` → `X` | BR-07 = nom de l'acheteur | pas de format d'identifiant acheteur |

`XRechnung-O.xml` porte déjà `schemeID="FC">XX` et `SpecifiedLegalOrganization/ID` = `XX` (fixture officielle, 0 fail).

**Distinction :** simple attente de test (absence de règle de format).

### TypeCode 381 sur une facture CII

`380` → `381` (avoir) sur Z, racine toujours `CrossIndustryInvoice` : 0 fail.

**BR-CL-01 CII** (L992–993) : *une* liste fusionnée UNTDID 1001 « invoice *and* credit note » qui contient `380` **et** `381`.

**BR-CL-01 UBL** (L1149–1150) : deux listes disjointes. `CreditNoteTypeCode` = `380` → **couvert** (`BR-CL-01`). C'est le contrôle positif : UBL sépare les natures, CII non.

**Distinction :** observation. Le code est dans la liste CII ; aucune règle CII n'exige que `381` soit porté par un avoir. Conforme à la consigne (« si le code est dans BR-CL-01, classer observation sauf règle normative contraire »).

---

## Erreurs moteur (notation scientifique)

`1E+100` et `1169387E-2` sur BT-112 : SaxonC-HE 13.0 lève `FORG0001 Cannot convert string "…" to xs:decimal: invalid character 'E'` dans un `xsl:when/@test` (BR-CO, `xs:decimal(...)`). **Pas de SVRL.** Ce n'est pas un document accepté.

BR-DEC-14 (`substring-after(.,'.')`) n'aurait *pas* tiré : pas de `.` dans `1E+100`. L'échec vient de la conversion XPath, pas d'un filet décimal. Classé **erreur moteur / observation**, pas angle mort (le document ne passe pas) et pas « couvert » (pas d'`id` SVRL).

---

## Reproduire

À la racine de `repo-v1/` :

```bash
# 21 sondes (lot principal, ignore expected.json)
.venv/bin/python scripts/validate.py --dir gaps --out-dir gaps/receipts --no-expected

# les 2 notations scientifiques (exception Saxon, pas de SVRL)
.venv/bin/python -c "
from pathlib import Path
from saxonche import PySaxonProcessor, PySaxonApiError
xslt='vendor/en16931-1.3.16/xslt/EN16931-CII-validation.xslt'
with PySaxonProcessor(license=False) as p:
    x=p.new_xslt30_processor().compile_stylesheet(stylesheet_file=xslt)
    for f in Path('gaps/engine-errors').glob('*.xml'):
        try:
            x.transform_to_string(source_file=str(f))
        except PySaxonApiError as e:
            print(f.name, ':', e)
"

# intégrité des originaux
(cd fixtures && sha256sum -c SHA256SUMS)
```

---

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

SHA256 des 10 fichiers = table du README (inchangés). `SHA256SUMS` racine (fixtures + 2 XSLT) : OK. Aucune écriture dans `fixtures/`.

---

## Méthode (rappel)

Généralisation du trou BR-CO-09 : pour chaque famille (corps d'identifiant, IBAN, code « légal mais absurde », date impossible, précision d'un montant), (1) lire le `test` officiel, (2) muter une copie d'une fixture CEN d'une ligne, (3) rejouer le XSLT 1.3.16, (4) classer seulement si le texte de règle *et* le contre-test s'accordent. Les 5 `failed-assert` obtenus sont des *contrôles* (la sonde n'est pas un trou), pas des findings.
