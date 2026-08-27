# Preuve de mappings d'identifiants de règles — EN16931 1.3.16

**Date :** 16 août 2026 (Europe/Paris) — 16 Aug 2026 PT  
**Moteur :** SaxonC-HE 13.0 (`saxonche==13.0.0`)  
**XSLT CII exécuté :** `vendor/en16931-1.3.16/xslt/EN16931-CII-validation.xslt`  
**SHA256 XSLT CII :** `0b234dea2bbfee739b7761e607a992c17fab88773014ef56355b6158cfb1cc53`  
**XSLT UBL exécuté :** `vendor/en16931-1.3.16/xslt/EN16931-UBL-validation.xslt`  
**SHA256 XSLT UBL :** `39f9d282867f1a49e7708d9e29a53da89643e1ee56f10cec1ebcf1277595fcbd`  
**Schematron / XSLT :** `vendor/en16931-1.3.16/` (XSLT exécuté ; SHA ci-dessus)
**Statut :** notes de corpus. Claims d'équivalence uniquement sur textes
officiels + id SVRL réellement tiré.
**`fixtures/` officiel :** non modifié (`sha256sum -c fixtures/SHA256SUMS` : 10 × OK après ce travail).

Trois classes, jamais mélangées :

| Classe | Sens |
|---|---|
| **Équivalence normative** | même règle métier EN16931 (`BR-*` du modèle abstrait) |
| **Équivalence fonctionnelle** | même intention de test (prouvé par textes officiels **et** par un `id` SVRL réellement tiré) |
| **Mapping interne** | simple renommage d'`id` dans l'artefact |

Une équivalence n'est **pas** affirmée sans (a) les deux `id`/textes dans un artefact officiel **ou** une issue officielle **et** (b), si l'on prétend une équivalence fonctionnelle, un SVRL qui montre l'`id` réellement tiré.

---

## 1. Vérification de la revendication (sources officielles, pas nos notes)

**Revendication :** `BR-CO-27` n'apparaît pas comme `id` de `svrl:failed-assert` dans le Schematron/XSLT officiel EN16931 1.3.16, et le contrôle correspondant est porté par **`CII-SR-470`**.

### 1.1 Comptages dans l'artefact exécuté et le Schematron préprocessé

Occurrences de la chaîne (Python `str.count`, 16 Aug 2026 PT) :

| Fichier | `BR-CO-27` | `CII-SR-470` |
|---|---:|---:|
| XSLT CII 1.3.16 exécuté (`EN16931-CII-validation.xslt`) | **0** | **2** (`id` + texte) |
| XSLT UBL 1.3.16 exécuté | **0** | **0** |
| Préprocessé CII 1.3.16 | **0** | **2** (`id` + texte) |
| Préprocessé UBL 1.3.16 | **0** | **0** |
| Source `cii/schematron/abstract/EN16931-CII-syntax.sch` | **0** | 3 |
| Source `cii/schematron/CII/EN16931-CII-syntax.sch` (param) | **0** | 1 |
| Source `cii/schematron/abstract/EN16931-CII-model.sch` | **0** | **0** |
| XSLT CII **1.3.15** (ZIP officiel) | **0** | **0** |
| Préprocessé CII **1.3.15** | **0** | **0** |

`BR-CO-27` est donc **absent** de l'artefact exécuté 1.3.16 **et** du ZIP 1.3.15. Il ne peut pas apparaître comme `id` de `failed-assert`.

### 1.2 Texte et test exacts de `CII-SR-470` (artefact)

Préprocessé CII 1.3.16, ligne 823, contexte `…/ram:ApplicableHeaderTradeSettlement` :

```xml
<assert id="CII-SR-470" flag="fatal" test="count(ram:SpecifiedTradeSettlementPaymentMeans[(normalize-space(ram:TypeCode) = '30' or normalize-space(ram:TypeCode) = '58') and not(ram:PayeePartyCreditorFinancialAccount/ram:IBANID or ram:PayeePartyCreditorFinancialAccount/ram:ProprietaryID)]) = 0">[CII-SR-470] - Either the IBAN or a Proprietary ID (BT-84) shall be used.</assert>
```

XSLT exécuté (l. 10381–10389), même test, `xsl:attribute name="id"` = `CII-SR-470`, texte SVRL identique.

Param source `CII/EN16931-CII-syntax.sch` l. 469 :

```xml
<param name="CII-SR-470" value="count(ram:SpecifiedTradeSettlementPaymentMeans[(normalize-space(ram:TypeCode) = '30' or normalize-space(ram:TypeCode) = '58') and not(ram:PayeePartyCreditorFinancialAccount/ram:IBANID or ram:PayeePartyCreditorFinancialAccount/ram:ProprietaryID)]) = 0"/>
```

### 1.3 Texte `BR-CO-27` : issue officielle seulement, pas l'artefact

Le libellé `BR-CO-27` n'existe **pas** dans les `.sch` / `.xslt` 1.3.15 ni 1.3.16. Il n'apparaît que dans le texte d'issue officielle.

Issue [#454](https://github.com/ConnectingEurope/eInvoicing-EN16931/issues/454) (fermée, milestone `1.3.16 (May-26)`), corps (citation) :

```
<assert test="$BR-CO-27" flag="fatal" id="BR-CO-27">[BR-CO-27]- Either the IBAN or a Proprietary ID (BT-84) shall be used.</assert>
```

et :

```
Please rename from BR-CO-27 to CII-SR-467
```

Le contexte cité dans #454 utilisait `tokenize('49 59'` — l'issue dit que c'est faux et que les codes crédit sont **30 / 58**.

Commentaire Oriol 2026-04-04 : « Please @AndreasPvd, check whether **CII-SR-470** resolves your requirement. » — puis clôture.

Notes de release 1.3.16 ([validation-1.3.16](https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/tag/validation-1.3.16), publiée 2026-04-13T12:58:43Z = **14:58 PT**) listent #454 parmi les issues corrigées, sans donner le nouvel `id`.

Issue [#500](https://github.com/ConnectingEurope/eInvoicing-EN16931/issues/500) (commentaire phax 2026-04-26) : « BR-CO-27 was also removed in 1.3.16, based on #454 ». Commentaire csautereau 2026-06-17 : « BR-CO-27 only makes sense in CII as there is 2 different Xpath for IBAN and proprietary ID where only one in UBL for BT-84 […] it should be a syntax rule only for CII (a SR-CII-XXX) ».

### 1.4 Verdict sur la revendication

**Confirmée**, avec trois précisions obligatoires :

1. L'`id` qui tire est `CII-SR-470`, jamais `BR-CO-27` (0 occurrence dans l'artefact 1.3.16).
2. Le texte d'assert est le même à l'espace près (`[BR-CO-27]- Either…` dans #454 vs `[CII-SR-470] - Either…` dans l'artefact).
3. Le test 1.3.16 est un **OU** (au moins un de `IBANID` / `ProprietaryID` sur un moyen 30 ou 58), **pas** le XOR « exactement un des deux » décrit par #454 / #500. Un compte **avec les deux** IDs ne viole **pas** `CII-SR-470`.

---

## 2. Preuve d'exécution — `CII-SR-470`

Fixture synthétique : `mapping/fixtures/CII-SR-470-no-bt84.xml`  
Base : copie de l'exemple officiel `CII_example3.xml` (CEN ZIP 1.3.16).  
Mutation : un seul `SpecifiedTradeSettlementPaymentMeans` `TypeCode=30`, **sans** `PayeePartyCreditorFinancialAccount` (donc sans `IBANID` et sans `ProprietaryID`). Compte entier retiré pour que `BR-50` / `BR-61` (contexte `…TypeCode='30' or '58'/ram:PayeePartyCreditorFinancialAccount`) n'aient **pas** de nœud.

SHA256 fixture : `7877b5b6b0e01a004bc9fd60cb6128d97453d80f31337bc6cb94f320362c33c9`

SVRL : `mapping/receipts/CII-SR-470-no-bt84.svrl.xml`  
Moteur SaxonC-HE 13.0 — **1** `svrl:failed-assert`, `id` réel = **`CII-SR-470`** (pas `BR-CO-27`, pas `BR-50`, pas `BR-61`).

```xml
<svrl:failed-assert test="count(ram:SpecifiedTradeSettlementPaymentMeans[(normalize-space(ram:TypeCode) = '30' or normalize-space(ram:TypeCode) = '58') and not(ram:PayeePartyCreditorFinancialAccount/ram:IBANID or ram:PayeePartyCreditorFinancialAccount/ram:ProprietaryID)]) = 0"
                   id="CII-SR-470"
                   flag="fatal"
                   location="…/ApplicableHeaderTradeSettlement[1]">
  <svrl:text>[CII-SR-470] - Either the IBAN or a Proprietary ID (BT-84) shall be used.</svrl:text>
</svrl:failed-assert>
```

`fired-rule` : 81. Recette : `mapping/receipts/CII-SR-470-no-bt84.receipt.md`.

### Classification `BR-CO-27` ↔ `CII-SR-470`

| Classe | Verdict | Pourquoi |
|---|---|---|
| Équivalence **normative** (même BR EN16931) | **Non** | #454 et #500 : `BR-CO-27` n'est **pas** une règle officielle EN ; le contrôle est une règle de syntaxe CII (`CII-SR-*`). Absent du modèle abstrait 1.3.16. |
| Équivalence **fonctionnelle** (même intention) | **Oui, partielle** | Même libellé BT-84, mêmes codes 30/58, même « au moins un identifiant de compte ». **Pas** le XOR « un seul des deux » demandé par #454. Prouvé par le SVRL ci-dessus. |
| Mapping **interne** (rename d'`id` dans l'artefact) | **Non au sens strict** | `BR-CO-27` n'existe dans **aucun** ZIP publié 1.3.15 / 1.3.16. #454 demandait le rename vers **`CII-SR-467`** ; l'`id` publié pour *cette* sémantique IBAN/BT-84 est **`CII-SR-470`**. C'est un nouvel `id` SR, pas un rename mesurable dans l'artefact publié. |

---

## 3. Mappings voisins (2–3 candidats, prouvés ou non affirmés)

### 3.1 `BR-CO-25` — **retrait**, pas un mapping

Présent en 1.3.15 (CII + UBL), **absent** en 1.3.16 (0 occurrence XSLT/préprocessé CII et UBL).

Texte 1.3.15 (préprocessé CII) :

```xml
<assert id="BR-CO-25" flag="fatal" test="(number(//ram:DuePayableAmount) > 0 and ((//ram:SpecifiedTradePaymentTerms/ram:DueDateDateTime) or (//ram:SpecifiedTradePaymentTerms/ram:Description))) or not(number(//ram:DuePayableAmount)>0)">[BR-CO-25]-In case the Amount due for payment (BT-115) is positive, either the Payment due date (BT-9) or the Payment terms (BT-20) shall be present.</assert>
```

Release 1.3.16 + issue [#477](https://github.com/ConnectingEurope/eInvoicing-EN16931/issues/477) ; #500 / phax : « BR-CO-25 was removed for last release 1.3.16 ». Aucun `CII-SR-*` / `UBL-SR-*` de 1.3.16 ne reprend ce test.

Preuve d'absence (pas d'équivalence) : `mapping/fixtures/CII-BR-CO-25-absent.xml` (BT-115 = 1125, plus de BT-9 / BT-20).  
SVRL : **0** `failed-assert`. `BR-CO-25` **ne tire pas**.  
SHA256 : `69d6e231a80f017ff231fd7b5d993c1800c47d7624e62b1b6166138bffa7ca50`.

**Pas un mapping.** C'est une suppression d'`id`.

### 3.2 #454 citait `CII-SR-467` — l'id IBAN réel est `CII-SR-470`

#454 : « Please rename from BR-CO-27 to **CII-SR-467** ».  
L'artefact 1.3.16 a **les deux** `id`, avec des tests **différents**.

`CII-SR-467` (préprocessé, contexte `/rsm:CrossIndustryInvoice`) :

```xml
<assert id="CII-SR-467" flag="fatal" test="count(//ram:SpecifiedTradeSettlementPaymentMeans/ram:TypeCode[normalize-space(.) != normalize-space((//ram:SpecifiedTradeSettlementPaymentMeans/ram:TypeCode)[1])]) = 0">[CII-SR-467] - All Payment means type codes (BT-81) shall have the same value across all SpecifiedTradeSettlementPaymentMeans.</assert>
```

Preuve SVRL : `mapping/fixtures/CII-SR-467-divergent-bt81.xml` (TypeCode 30 **et** 58, BT-84 présent).  
**1** `failed-assert`, `id` = **`CII-SR-467`** — pas `CII-SR-470`.  
SHA256 : `ca9c7048a92bd9fe3094232efacc0c199f46bd6b72c7c321d783a7dfda657b16`.

Donc : le rename demandé par #454 vers `CII-SR-467` **n'est pas** le contrôle IBAN/BT-84. `CII-SR-467` porte l'égalité des BT-81 (voir 3.4).

### 3.3 Équivalent UBL de `CII-SR-470` (virement 30/58 + BT-84)

**Pas** d'`UBL-SR-*` « IBAN ou ProprietaryID ». UBL n'a qu'un `cbc:ID` pour BT-84 (#500, csautereau).  
`BR-CO-27` : 0 dans le XSLT UBL 1.3.16.

Règles UBL voisines (préprocessé) :

```xml
<!-- contexte cac:PaymentMeans[code 30|58]/cac:PayeeFinancialAccount -->
<assert id="BR-50" flag="fatal" test="normalize-space(cbc:ID) != ''">[BR-50]-A Payment account identifier (BT-84) shall be present if Credit transfer (BG-17) information is provided in the Invoice.</assert>

<!-- contexte cac:PaymentMeans -->
<assert id="BR-61" flag="fatal" test="(exists(cac:PayeeFinancialAccount/cbc:ID) and ((normalize-space(cbc:PaymentMeansCode) = '30') or (normalize-space(cbc:PaymentMeansCode) = '58') )) or ((normalize-space(cbc:PaymentMeansCode) != '30') and (normalize-space(cbc:PaymentMeansCode) != '58'))">[BR-61]-If the Payment means type code (BT-81) means SEPA credit transfer, Local credit transfer or Non-SEPA international credit transfer, the Payment account identifier (BT-84) shall be present.</assert>
```

Côté CII, `BR-50` / `BR-61` existent aussi, mais leur contexte exige déjà `PayeePartyCreditorFinancialAccount`. `CII-SR-470` est le seul fatal qui attrape un TypeCode 30/58 **sans** ce nœud.

Preuve SVRL UBL : `mapping/fixtures/ubl-BR-61-no-bt84.xml` (code 30, pas de `PayeeFinancialAccount`).  
**1** `failed-assert`, `id` = **`BR-61`** (pas `BR-50` : le compte n'existe pas ; pas `BR-CO-27` ; pas `CII-SR-470`).  
SHA256 : `ba152efc389aa9ea13f96e05704e13629188d446d61b5c8fd2763dac44027d4f`.

| Paire | Classe | Verdict |
|---|---|---|
| `CII-SR-470` ↔ `BR-61` (UBL) | Fonctionnelle | **Oui, limitée** : « virement 30/58 ⇒ BT-84 présent ». Un seul champ UBL, pas IBAN/Proprietary. SVRL : `BR-61`. |
| `CII-SR-470` ↔ `BR-50` (UBL) | Fonctionnelle | **Non affirmée ici** : `BR-50` ne s'applique que si `PayeeFinancialAccount` existe. Notre synthétique UBL ne le tire pas. |
| `CII-SR-470` ↔ un `UBL-SR-*` | — | **Aucune**. 0 `UBL-SR` avec ce test. |
| `CII-SR-470` ↔ `BR-CO-27` UBL | Normative | **Non** (id absent). |

### 3.4 `CII-SR-467` ↔ `UBL-SR-47` (et 468/469)

Issue officielle [#457](https://github.com/ConnectingEurope/eInvoicing-EN16931/issues/457) : « Repeating BT-81, BT-82 and BT-83 with different content should be prohibited **equivalent to UBL-SR-47**. » (marquée *duplicate* de #484).  
Issue [#484](https://github.com/ConnectingEurope/eInvoicing-EN16931/issues/484) : BT-81 même valeur sur tous les `SpecifiedTradeSettlementPaymentMeans` ; BT-82 et BT-83 au plus une fois. Release 1.3.16 liste #457 et #484.

Textes officiels 1.3.16 :

```xml
<assert id="CII-SR-467" …>[CII-SR-467] - All Payment means type codes (BT-81) shall have the same value across all SpecifiedTradeSettlementPaymentMeans.</assert>
<assert id="CII-SR-468" …>[CII-SR-468] - All Payment means texts (BT-82) shall have the same value across all SpecifiedTradeSettlementPaymentMeans.</assert>
<assert id="CII-SR-469" …>[CII-SR-469] - Payment reference (BT-83) shall occur at most once in the document.</assert>
<assert id="UBL-SR-47" flag="fatal" test="count(//cbc:PaymentMeansCode[not(preceding::cbc:PaymentMeansCode/. = .)]) &lt;= 1">[UBL-SR-47]-When there are more than one payment means code, they shall be equal</assert>
```

Preuve SVRL UBL : `mapping/fixtures/ubl-SR-47-divergent-bt81.xml` (codes 1 **et** 30).  
**1** `failed-assert`, `id` = **`UBL-SR-47`**.  
SHA256 : `7a1393d6f50f5b96bd7bc7c20ca32954e01831eebafcde9a0075da8cbcb0cd35`.

Couplé au SVRL `CII-SR-467` (§ 3.2) :

| Paire | Classe | Verdict |
|---|---|---|
| `CII-SR-467` ↔ `UBL-SR-47` | Fonctionnelle | **Oui** : même intention (BT-81 identiques s'il y en a plusieurs). Issue #457 + deux SVRL. |
| `CII-SR-467` ↔ `UBL-SR-47` | Normative | **Non** : deux règles de syntaxe, pas un `BR-*` commun. |
| `CII-SR-468` ↔ `UBL-SR-47` | — | **Non affirmée.** 468 = égalité des textes BT-82. `UBL-SR-47` ne parle que du code. Pas de SVRL 468. |
| `CII-SR-469` ↔ `UBL-SR-47` | — | **Non affirmée.** 469 = cardinalité BT-83 ≤ 1. Voisin UBL plutôt `UBL-SR-44` (PaymentID unique) — tests non identiques, pas de SVRL ici. |

---

## 4. Tableau récapitulatif

| Candidat | Type | `id` qui tire (SVRL 1.3.16) | Preuve |
|---|---|---|---|
| `BR-CO-27` → `CII-SR-470` | fonctionnelle partielle (libellé BT-84 / 30-58) ; **pas** normative ; **pas** rename mesurable dans le ZIP | `CII-SR-470` | artefact 0× `BR-CO-27` ; #454 / #500 ; SVRL `CII-SR-470-no-bt84` |
| `BR-CO-25` | **retrait** (1.3.15 → 1.3.16) | *aucun* | 0× dans 1.3.16 ; SVRL `CII-BR-CO-25-absent` = 0 failed-assert |
| #454 « rename vers `CII-SR-467` » | **contredit** par l'artefact | `CII-SR-467` = BT-81, pas IBAN | SVRL `CII-SR-467-divergent-bt81` |
| `CII-SR-470` ↔ UBL | fonctionnelle limitée via **`BR-61`** | `BR-61` | SVRL `ubl-BR-61-no-bt84` ; pas d'`UBL-SR` IBAN/Proprietary |
| `CII-SR-467` ↔ `UBL-SR-47` | fonctionnelle (BT-81) | `CII-SR-467` / `UBL-SR-47` | #457 + deux SVRL |
| `CII-SR-468` / `CII-SR-469` ↔ `UBL-SR-47` | **non affirmé** | — | textes différents ; pas de SVRL dédié |

---

## 5. Fichiers livrés

```
MAPPING-PROOF.md                          (ce fichier)
mapping/fixtures/CII-SR-470-no-bt84.xml
mapping/fixtures/CII-SR-467-divergent-bt81.xml
mapping/fixtures/CII-BR-CO-25-absent.xml
mapping/fixtures/ubl-SR-47-divergent-bt81.xml
mapping/fixtures/ubl-BR-61-no-bt84.xml
mapping/fixtures/SHA256SUMS
mapping/fixtures/SOURCES.md
mapping/receipts/*.svrl.xml
mapping/receipts/*.receipt.md
mapping/receipts/RESULTS.json
mapping/receipts/RESULTS.sha256
```

`mapping/receipts/RESULTS.sha256` = `d35463f19e04fe0db9678239ab634d22cf2ec1fa18e01a0f2c18e4db454744f5`

SHA256 des synthétiques (`mapping/fixtures/SHA256SUMS`) :

```
69d6e231a80f017ff231fd7b5d993c1800c47d7624e62b1b6166138bffa7ca50  CII-BR-CO-25-absent.xml
ca9c7048a92bd9fe3094232efacc0c199f46bd6b72c7c321d783a7dfda657b16  CII-SR-467-divergent-bt81.xml
7877b5b6b0e01a004bc9fd60cb6128d97453d80f31337bc6cb94f320362c33c9  CII-SR-470-no-bt84.xml
ba152efc389aa9ea13f96e05704e13629188d446d61b5c8fd2763dac44027d4f  ubl-BR-61-no-bt84.xml
7a1393d6f50f5b96bd7bc7c20ca32954e01831eebafcde9a0075da8cbcb0cd35  ubl-SR-47-divergent-bt81.xml
```

Commande : `.venv/bin/python scripts/validate.py --mode reference --dir mapping/fixtures --out-dir mapping/receipts --no-expected`  
(16 Aug 2026 PT, `SOURCE_DATE_EPOCH=1771286400`).
