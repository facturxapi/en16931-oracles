**machine-verified candidate — EN16931 1.3.16 official XSLT**
Statut : CANDIDAT. Pas une signature founder. Pas une publication.

# Oracle candidat — CII_example1.xml

**Statut :** CANDIDAT — le founder/lead arbitre. Rien n’entre au corpus sans signature.
**Date de construction :** 16 août 2026 (Europe/Paris)
**Doctrine :** oracle-first. Dérivé de la norme, jamais d’un produit.
**Interdit respecté :** aucune consultation de facturxapi.com.

## Identité de la fixture
- Nom : `CII_example1.xml`
- URL source exacte : chemin `examples/CII_example1.xml` dans le ZIP officiel [en16931-cii-1.3.16.zip](https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/download/validation-1.3.16/en16931-cii-1.3.16.zip) (tag [validation-1.3.16](https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/tag/validation-1.3.16), consulté 16 août 2026). Listing public : [cii/examples](https://github.com/ConnectingEurope/eInvoicing-EN16931/tree/master/cii/examples).
- SHA256 : `0c12e3ca9aab58299e6271b89d061274694c62159510ca2d848f13d287ee4f99`
- Taille : 34 459 octets
- Datetime de téléchargement : 16 août 2026, 00:12 (Europe/Paris) — ZIP CII SHA256 `1cd53cb8a84d38aedc82c0caede217da983a7934dd663f793a092fd66443c561` (226 664 octets)
- Syntaxe : CII D16B (`rsm:CrossIndustryInvoice`, URN `urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100`)
- Dépôt / tag : ConnectingEurope/eInvoicing-EN16931 @ validation-1.3.16

## (1) Ce que la source normative dit que ce document EST

Facture commerciale typique EN16931 core, syntaxe CII.

Champs observés (extraits bruts, namespaces omis) :

```xml
<ID>urn:cen.eu:en16931:2017</ID>                 <!-- BT-24 -->
<ID>12115118</ID>                               <!-- BT-1 -->
<TypeCode>380</TypeCode>                        <!-- BT-3 -->
<DateTimeString format="102">20150109</DateTimeString>  <!-- BT-2 -->
<InvoiceCurrencyCode>EUR</InvoiceCurrencyCode>  <!-- BT-5 -->
<Name>De Koksmaat</Name>                        <!-- BT-27 -->
<ID schemeID="VA">NL8200.98.395.B.01</ID>       <!-- BT-31 -->
<Name>ODIN 59</Name>                            <!-- BT-44 -->
```

Pas de BT-48 (TVA acheteur absente). 20 lignes BG-25, catégories S à 6 % et 21 %. Totaux :

```xml
<LineTotalAmount>229.6</LineTotalAmount>          <!-- BT-106 -->
<TaxBasisTotalAmount>229.6</TaxBasisTotalAmount>  <!-- BT-109 -->
<TaxTotalAmount currencyID="EUR">20.73</TaxTotalAmount> <!-- BT-110 -->
<GrandTotalAmount>250.33</GrandTotalAmount>       <!-- BT-112 -->
<DuePayableAmount>250.33</DuePayableAmount>       <!-- BT-115 -->
```

BG-23 (deux taux S) :

```xml
<CalculatedAmount>10.99</CalculatedAmount><BasisAmount>183.23</BasisAmount>
<CategoryCode>S</CategoryCode><RateApplicablePercent>6</RateApplicablePercent>
<CalculatedAmount>9.74</CalculatedAmount><BasisAmount>46.37</BasisAmount>
<CategoryCode>S</CategoryCode><RateApplicablePercent>21</RateApplicablePercent>
```

Pas de BG-20/BG-21 (allowance/charge document). Pas de BG-3 (facture antérieure). Moyen de paiement TypeCode 30.

Règles 1.3.16 pertinentes (Schematron préprocessé `schematron/preprocessed/EN16931-CII-validation-preprocessed.sch` du même ZIP, consulté 16 août 2026) :

- `[BR-01]` « An Invoice shall have a Specification identifier (BT-24). » — test : `normalize-space(.../ram:ID) != ''` — présent `urn:cen.eu:en16931:2017`.
- `[BR-02]` BT-1, `[BR-03]` BT-2 format 102, `[BR-04]` BT-3, `[BR-05]` BT-5, `[BR-06]` BT-27, `[BR-07]` BT-44 : présents.
- `[BR-CL-01]` TypeCode dans UNTDID 1001 — `380` est dans la liste (`… 380 381 382 …`).
- `[BR-CO-10]` « Sum of Invoice line net amount (BT-106) = Σ Invoice line net amount (BT-131). » — test : `xs:decimal(ram:LineTotalAmount) = round(xs:decimal(sum(…/ram:LineTotalAmount)) * 100) div 100`. Somme observée des 20 BT-131 = 229.6 = BT-106.
- `[BR-CO-14]` BT-110 = Σ BT-117 : 10.99 + 9.74 = 20.73.
- `[BR-CO-15]` BT-112 = BT-109 + BT-110 : 229.6 + 20.73 = 250.33.
- `[BR-S-01]` / `[BR-S-09]` catégorie S présente en ligne et en BG-23.

**Règles violées :** aucune — 0 `svrl:failed-assert` sur le XSLT officiel 1.3.16 du même ZIP (consulté et exécuté 16 août 2026, Europe/Paris).

**Validité machine EN16931 1.3.16 :** XSLT officiel `xslt/EN16931-CII-validation.xslt` du même ZIP, exécuté localement (SaxonC-HE 13.0, 16 août 2026) : **0 `svrl:failed-assert`**, 423 `fired-rule`. Aucune règle violée mesurable.

**BR-FR v1.4.0.03 :** non pertinent. Le document porte `urn:cen.eu:en16931:2017` (core EN), pas un profil CTC-FR / EXTENDED-CTC-FR. Source BR-FR : [fnfempe/France_RFE v1.4.0.03](https://github.com/fnfempe/France_RFE/releases/tag/v1.4.0.03) (consulté 16 août 2026) — pack CIUS France ; ne s’applique pas à un exemple ConnectingEurope core.

## (2) Ce qu’un produit honnête DEVRAIT dire à l’utilisateur

Générable. Document core EN16931 CII, type 380, totaux cohérents, TVA S à deux taux. Pas de blocage métier EN16931 1.3.16. Pas un cas limite d’arrondi. Pas un profil hors EN16931. L’absence de TVA acheteur (BT-48) n’est pas une erreur core : `[BR-07]-An Invoice shall contain the Buyer name (BT-44).` (Schematron 1.3.16, même ZIP, 16 août 2026) — le nom `ODIN 59` est présent ; aucune BR 1.3.16 n’exige BT-48 sur une facture S domestique NL.

## (3) Points ambigus — DEUX lectures argumentées et sourcées

aucune ambiguïté mesurable. BT-24 est l’URN core CEN ; le SVRL 1.3.16 et le texte des BR-CO d’addition concordent (0 failed-assert).

## (4) Verdict candidat + confiance
- Verdict : **VALIDE EN16931 1.3.16**
- Confiance : **haute** — fixture officielle du ZIP 1.3.16 + 0 failed-assert sur le XSLT du même ZIP + totaux recalculés alignés sur BR-CO-10/14/15.
- Ce que le founder doit trancher : admission au corpus comme oracle « facture core typique CII 380 ».
