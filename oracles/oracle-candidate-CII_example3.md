**machine-verified candidate — EN16931 1.3.16 official XSLT**
Statut : CANDIDAT. Pas une signature founder. Pas une publication.

# Oracle candidat — CII_example3.xml

**Statut :** CANDIDAT — le founder/lead arbitre. Rien n’entre au corpus sans signature.
**Date de construction :** 16 août 2026 (Europe/Paris)
**Doctrine :** oracle-first. Dérivé de la norme, jamais d’un produit.
**Interdit respecté :** aucune consultation de facturxapi.com.

## Identité de la fixture
- Nom : `CII_example3.xml`
- Substitution : le plan demandait `CII_example2.xml`. Dans le ZIP 1.3.16, `CII_example2.xml` est **octet-identique** à `CII_business_example_01.xml` (même SHA256 `2ce8286333f4c2019166c505642963e1222f54c18558ae4210fd41fd5d526b2f`). Aucun CII numéroté du ZIP n’a un BT-3 ≠ 380. On retient donc `CII_example3.xml` (abonnement + charge document, DKK) pour la diversité.
- URL source exacte : chemin `examples/CII_example3.xml` dans [en16931-cii-1.3.16.zip](https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/download/validation-1.3.16/en16931-cii-1.3.16.zip) (tag [validation-1.3.16](https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/tag/validation-1.3.16), consulté 16 août 2026).
- SHA256 : `eda939773fa9556acb411555ef2e73df8d1eabe1d2c9ba99445a00abf889db6d`
- Taille : 7 985 octets
- Datetime de téléchargement : 16 août 2026, 00:12 (Europe/Paris)
- Syntaxe : CII D16B
- Dépôt / tag : ConnectingEurope/eInvoicing-EN16931 @ validation-1.3.16

## (1) Ce que la source normative dit que ce document EST

Facture 380 core EN16931, une ligne d’abonnement, une charge document (BG-21).

```xml
<ID>urn:cen.eu:en16931:2017</ID>                 <!-- BT-24 -->
<ID>TOSL108</ID>                                <!-- BT-1 -->
<TypeCode>380</TypeCode>                        <!-- BT-3 -->
<DateTimeString format="102">20130410</DateTimeString>
<InvoiceCurrencyCode>DKK</InvoiceCurrencyCode>
<Name>SubscriptionSeller</Name>
<ID schemeID="VA">DK16356706</ID>
<Name>Buyercompany ltd</Name>
```

Ligne unique : `Paper subscription`, qty 1 C62, BT-131 = 800, cat S 25 %. Charge document :

```xml
<ChargeIndicator><Indicator>true</Indicator></ChargeIndicator>
<ActualAmount>100</ActualAmount>
<ReasonCode>FC</ReasonCode>
<Reason>Freight charge</Reason>
<CategoryCode>S</CategoryCode>
<RateApplicablePercent>25</RateApplicablePercent>
```

Totaux et BG-23 :

```xml
<LineTotalAmount>800</LineTotalAmount>
<ChargeTotalAmount>100</ChargeTotalAmount>
<TaxBasisTotalAmount>900</TaxBasisTotalAmount>
<TaxTotalAmount currencyID="DKK">225</TaxTotalAmount>
<GrandTotalAmount>1125</GrandTotalAmount>
<DuePayableAmount>1125</DuePayableAmount>
<CalculatedAmount>225</CalculatedAmount>
<BasisAmount>900</BasisAmount>
<CategoryCode>S</CategoryCode>
<RateApplicablePercent>25</RateApplicablePercent>
```

Règles 1.3.16 (même ZIP, `EN16931-CII-validation-preprocessed.sch`, 16 août 2026) :

- `[BR-CO-10]` 800 = 800.
- `[BR-CO-12]` « Sum of charges on document level (BT-108) = Σ Document level charge amount (BT-99). » — 100 = 100.
- `[BR-CO-13]` BT-109 = Σ BT-131 − BT-107 + BT-108 : 800 − 0 + 100 = 900.
- `[BR-CO-15]` 900 + 225 = 1125.
- `[BR-CO-17]` / `[BR-S-09]` 900 × 25 % = 225.
- `[BR-CO-22]` charge : reason **et** reason code présents (`Freight charge` / `FC`).
- `[BR-CL-20]` « Coded charge reasons MUST belong to the UNCL 7161 code list » — `FC` (freight) est le code UNCL 7161 usuel ; le SVRL n’a pas échoué.

**Règles violées :** aucune — 0 `svrl:failed-assert` sur le XSLT officiel 1.3.16 du même ZIP (consulté et exécuté 16 août 2026, Europe/Paris).

**Validité machine :** XSLT officiel CII 1.3.16, SaxonC-HE 13.0, 16 août 2026 : **0 failed-assert**, 89 fired-rule.

**BR-FR v1.4.0.03 :** non pertinent (core `urn:cen.eu:en16931:2017`, vendeur DK, pas de champs CTC-FR). Source : [France_RFE v1.4.0.03](https://github.com/fnfempe/France_RFE/releases/tag/v1.4.0.03), consulté 16 août 2026.

## (2) Ce qu’un produit honnête DEVRAIT dire à l’utilisateur

Générable. Facture d’abonnement avec frais de port (BG-21) en DKK, TVA S 25 %. Pas invalide structurel, pas invalide métier EN16931 1.3.16. Ce n’est pas un avoir (BT-3 = 380, pas 381).

## (3) Points ambigus — DEUX lectures argumentées et sourcées

aucune ambiguïté mesurable sur la validité EN16931 1.3.16. La seule ambiguïté de **sélection** (hors document) : `CII_example2.xml` du même ZIP est un doublon binaire de `CII_business_example_01.xml` — substitution documentée ci-dessus.

## (4) Verdict candidat + confiance
- Verdict : **VALIDE EN16931 1.3.16**
- Confiance : **haute** — 0 failed-assert + additions BR-CO-10/12/13/15 exactes.
- Ce que le founder doit trancher : accepter la substitution example3 (diversité) vs forcer example2 malgré le doublon.
