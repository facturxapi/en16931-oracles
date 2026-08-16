**machine-verified candidate — EN16931 1.3.16 official XSLT**
Statut : CANDIDAT. Pas une signature founder. Pas une publication.

# Oracle candidat — ubl-tc434-creditnote1.xml

**Statut :** CANDIDAT — le founder/lead arbitre. Rien n’entre au corpus sans signature.
**Date de construction :** 16 août 2026 (Europe/Paris)
**Doctrine :** oracle-first. Dérivé de la norme, jamais d’un produit.
**Interdit respecté :** aucune consultation de facturxapi.com.

## Identité de la fixture
- Nom : `ubl-tc434-creditnote1.xml`
- URL source exacte : chemin `examples/ubl-tc434-creditnote1.xml` dans [en16931-ubl-1.3.16.zip](https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/download/validation-1.3.16/en16931-ubl-1.3.16.zip) (tag [validation-1.3.16](https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/tag/validation-1.3.16), consulté 16 août 2026). ZIP UBL SHA256 `bafada015efbc5248bf5e05ad2191e1d9833ef96e9dd5f4bce420a747342da85` (2 650 024 octets), téléchargé 16 août 2026 00:12 Europe/Paris.
- SHA256 : `911d7ac2cb4fa72d21331c76914468e7d94eda03629e0def75c64ab18e3e9dce`
- Taille : 4 935 octets
- Syntaxe : UBL 2.1 CreditNote (`xmlns="urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2"`)
- Dépôt / tag : ConnectingEurope/eInvoicing-EN16931 @ validation-1.3.16

## (1) Ce que la source normative dit que ce document EST

Avoir UBL (BT-3 = 381), exonération E, profil Peppol BIS déclaré en plus du core EN.

```xml
<CustomizationID>urn:cen.eu:en16931:2017</CustomizationID>   <!-- BT-24 -->
<ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</ProfileID>
<ID>018304 / 28865</ID>                                      <!-- BT-1 -->
<IssueDate>2019-09-23</IssueDate>                            <!-- BT-2 -->
<CreditNoteTypeCode>381</CreditNoteTypeCode>                 <!-- BT-3 -->
<DocumentCurrencyCode>EUR</DocumentCurrencyCode>
<Name>My Supplier Company N.V.</Name>
<CompanyID>BE0000000196</CompanyID>                          <!-- BT-31 -->
<Name>My Customer Company S.A.</Name>
<CompanyID>BE0000000295</CompanyID>                          <!-- BT-48 -->
```

1 ligne CreditNoteLine : `Exonération du versement du PP`, qty 1 C62, 100.11, cat E 0 %.

```xml
<TaxAmount currencyID="EUR">0.00</TaxAmount>
<TaxableAmount currencyID="EUR">100.11</TaxableAmount>
<cbc:ID>E</cbc:ID><Percent>0.00</Percent>
<TaxExemptionReason>Taxes are not applicable</TaxExemptionReason>
<LineExtensionAmount currencyID="EUR">100.11</LineExtensionAmount>
<TaxExclusiveAmount currencyID="EUR">100.11</TaxExclusiveAmount>
<TaxInclusiveAmount currencyID="EUR">100.11</TaxInclusiveAmount>
<PayableAmount currencyID="EUR">100.11</PayableAmount>
```

Pas de `cac:BillingReference` (pas de BT-25).

Règles 1.3.16 UBL (`schematron/preprocessed/EN16931-UBL-validation-preprocessed.sch` + `xslt/EN16931-UBL-validation.xslt` du ZIP UBL, 16 août 2026) :

- `[BR-CL-01]` « The document type code MUST be coded by the invoice and credit note related code lists of UNTDID 1001. » — `381` est dans la liste (`… 380 381 382 …`).
- `[BR-E-01]` / `[BR-E-09]` / `[BR-E-10]` : un BG-23 E, taxe 0, motif `Taxes are not applicable`.
- `[BR-55]` ne s’applique que **si** BG-3 est présent (« Each Preceding Invoice reference (BG-3) shall contain … »). BG-3 absent ⇒ règle non déclenchée.
- `[UBL-SR-06]` « Preceding invoice reference shall occur maximum once » — 0 ≤ 1.
- `[UBL-SR-07]` « If there is a preceding invoice reference, the preceding invoice number shall be present » — conditionnelle, pas de référence.
- Notes de release 1.3.16 ([tag](https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/tag/validation-1.3.16), 16 août 2026) : « BR-CO-25 applied on credit notes in UBL but not CII » (issue #477). **BR-CO-25 n’apparaît pas** comme `id` dans le Schematron préprocessé 1.3.16 (recherche exacte : vide). **non-mesure** de BR-CO-25 : on n’invente pas le numéro.

**Règles violées :** aucune — 0 `svrl:failed-assert` sur le XSLT officiel 1.3.16 du même ZIP (consulté et exécuté 16 août 2026, Europe/Paris).

**Validité machine :** XSLT UBL 1.3.16, SaxonC-HE 13.0, 16 août 2026 : **0 failed-assert**, 53 fired-rule.

**BR-FR v1.4.0.03 :** non pertinent (core + Peppol profile, parties BE, pas CTC-FR). [France_RFE v1.4.0.03](https://github.com/fnfempe/France_RFE/releases/tag/v1.4.0.03), 16 août 2026.

## (2) Ce qu’un produit honnête DEVRAIT dire à l’utilisateur

Générable comme **avoir** EN16931 UBL (type 381), exonéré E. Distinguer :

- **valide EN16931 1.3.16** (XSLT officiel, 0 failed-assert) ;
- **profil Peppol déclaré** (`ProfileID`) : hors périmètre du seul Schematron EN16931 (le XSLT 1.3.16 ne valide pas Peppol BIS) ;
- **pas de facture d’origine (BT-25)** : autorisé par le core (BR-55 seulement si BG-3 présent). Un produit peut *avertir* métierlement (« avoir sans pièce de référence ») sans bloquer EN16931.

Ce n’est pas une facture 380. Ne pas le « réparer » en Invoice.

## (3) Points ambigus — DEUX lectures argumentées et sourcées

**Ambiguïté : avoir sans BT-25.**

- Lecture A : VALIDE core. BR-55 et UBL-SR-07 sont conditionnels. SVRL 0 failed-assert. Source : Schematron UBL 1.3.16 cité.
- Lecture B : un avoir sans facture précédente est incomplet métierlement. La note de release 1.3.16 évoque BR-CO-25 sur les credit notes UBL (issue #477) mais **l’id BR-CO-25 est absent** du préprocessé 1.3.16 → **non-mesure** de cette règle.

**Ambiguïté : Peppol vs EN core.**

- Lecture A : BT-24 = `urn:cen.eu:en16931:2017` ⇒ EN core. Le ProfileID Peppol est additionnel.
- Lecture B : un validateur Peppol BIS pourrait exiger d’autres champs (Endpoint, etc.). **non-mesure** Peppol (artefact non exécuté ; hors demande).

## (4) Verdict candidat + confiance
- Verdict : **VALIDE EN16931 1.3.16** (avoir UBL 381, cat E)
- Confiance : **haute** sur EN16931 ; **moyenne** sur l’attente métier « avoir ⇒ BT-25 »
- Ce que le founder doit trancher : avertissement BT-25 manquant = info utilisateur, pas invalidité EN.
