**machine-verified candidate — EN16931 1.3.16 official XSLT**
Statut : candidat machine-vérifié (0 failed-assert sur le XSLT officiel 1.3.16).
Pas une signature produit. Pas une preuve CIUS / Factur-X / BR-FR.

# Oracle candidat — CII_business_example_01.xml

**Statut :** candidat machine-vérifié — le verdict définitif d'admission
au corpus reste ouvert (voir la question en fin de note).
**Date de construction :** 16 août 2026 (Europe/Paris)
**Doctrine :** oracle-first. Dérivé de la norme, jamais d’un produit.

## Identité de la fixture
- Nom : `CII_business_example_01.xml`
- URL source exacte : chemin `examples/CII_business_example_01.xml` dans [en16931-cii-1.3.16.zip](https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/download/validation-1.3.16/en16931-cii-1.3.16.zip) (tag [validation-1.3.16](https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/tag/validation-1.3.16), consulté 16 août 2026). Horodatage ZIP : 2026-04-09 17:18 (mis à jour dans 1.3.16).
- SHA256 : `2ce8286333f4c2019166c505642963e1222f54c18558ae4210fd41fd5d526b2f`
- Taille : 26 758 octets
- Datetime de téléchargement : 16 août 2026, 00:12 (Europe/Paris)
- Identique octet à octet à `examples/CII_example2.xml` du même ZIP (même SHA256).
- Syntaxe : CII D16B
- Dépôt / tag : ConnectingEurope/eInvoicing-EN16931 @ validation-1.3.16

## (1) Ce que la source normative dit que ce document EST

Facture 380 core NOK, lignes positives et négatives (retours), allowance + charge, acompte, trois catégories TVA (S 25 %, S 15 %, E 0 %).

```xml
<ID>urn:cen.eu:en16931:2017</ID>
<ID>TOSL108</ID>
<TypeCode>380</TypeCode>
<DateTimeString format="102">20130630</DateTimeString>
<InvoiceCurrencyCode>NOK</InvoiceCurrencyCode>
<Name>Salescompany ltd.</Name>
<ID schemeID="VA">NO123456789MVA</ID>
<Name>The Buyercompany</Name>
<ID schemeID="VA">NO987654321MVA</ID>
```

Lignes (BT-131) : 1273 ; −3.96 ; 4.96 ; −25 (cat E) ; 187.5. Σ = 1436.5.

```xml
<LineTotalAmount>1436.5</LineTotalAmount>
<ChargeTotalAmount>100</ChargeTotalAmount>
<AllowanceTotalAmount>100</AllowanceTotalAmount>
<TaxBasisTotalAmount>1436.5</TaxBasisTotalAmount>
<TaxTotalAmount currencyID="NOK">365.28</TaxTotalAmount>
<GrandTotalAmount>1801.78</GrandTotalAmount>
<TotalPrepaidAmount>1000</TotalPrepaidAmount>
<DuePayableAmount>801.78</DuePayableAmount>
```

BG-23 :

```xml
<CalculatedAmount>365.13</CalculatedAmount><BasisAmount>1460.5</BasisAmount>
<CategoryCode>S</CategoryCode><RateApplicablePercent>25</RateApplicablePercent>
<CalculatedAmount>0.15</CalculatedAmount><BasisAmount>1</BasisAmount>
<CategoryCode>S</CategoryCode><RateApplicablePercent>15</RateApplicablePercent>
<CalculatedAmount>0</CalculatedAmount><BasisAmount>-25</BasisAmount>
<CategoryCode>E</CategoryCode>
<ExemptionReason>Exempt New Means of Transport</ExemptionReason>
<RateApplicablePercent>0</RateApplicablePercent>
```

Règles 1.3.16 (même ZIP, 16 août 2026) :

- `[BR-CO-10]` 1436.5 = Σ BT-131.
- `[BR-CO-13]` 1436.5 − 100 + 100 = 1436.5.
- `[BR-CO-14]` 365.13 + 0.15 + 0 = 365.28.
- `[BR-CO-15]` 1436.5 + 365.28 = 1801.78.
- `[BR-CO-16]` 1801.78 − 1000 = 801.78.
- `[BR-E-01]` une ligne E ⇒ exactement un BG-23 E — observé.
- `[BR-E-09]` « VAT category tax amount (BT-117) … "Exempt from VAT" shall equal 0 » — `CalculatedAmount` = 0.
- `[BR-E-10]` « shall have a VAT exemption reason code (BT-121) or a VAT exemption reason text (BT-120) » — texte `Exempt New Means of Transport` présent.
- `[BR-CL-01]` 380 autorisé.

**Règles violées :** aucune — 0 `svrl:failed-assert` sur le XSLT officiel 1.3.16 du même ZIP (consulté et exécuté 16 août 2026, Europe/Paris).

**Validité machine :** XSLT CII 1.3.16, SaxonC-HE 13.0, 16 août 2026 : **0 failed-assert**, 287 fired-rule.

**BR-FR v1.4.0.03 :** non pertinent (core EN, parties NO). [France_RFE v1.4.0.03](https://github.com/fnfempe/France_RFE/releases/tag/v1.4.0.03), 16 août 2026.

## (2) Ce qu’un produit honnête DEVRAIT dire à l’utilisateur

Générable. Facture avec retours (quantités négatives) et une ligne exonérée E, pas un avoir : BT-3 = 380. Totaux et acompte cohérents. Un produit ne doit pas classer les lignes négatives comme « credit note » tant que BT-3 n’est pas 381.

## (3) Points ambigus — DEUX lectures argumentées et sourcées

**Ambiguïté : lignes négatives vs avoir.**

- Lecture A : c’est une facture 380 qui impute des retours (BT-131 négatifs). `[BR-CL-01]` autorise 380 ; le Schematron 1.3.16 n’exige pas BG-3 pour 380. SVRL : 0 failed-assert.
- Lecture B : métierlement, un retour de « IBM 5150 » et d’un livre ressemble à un avoir. Contre-preuve normative : TypeCode observé `380`, pas `381` ; pas de `InvoiceReferencedDocument`.

**Ambiguïté de corpus :** ce fichier = `CII_example2.xml`. Ne pas compter deux oracles distincts.

## (4) Verdict candidat + confiance
- Verdict : **VALIDE EN16931 1.3.16**
- Confiance : **haute** — mis à jour 1.3.16, 0 failed-assert, BR-E-09/10 satisfaits.
- Question ouverte : un seul oracle pour example2 / business_01 (doublon).
