**machine-verified candidate — EN16931 1.3.16 official XSLT**
Statut : CANDIDAT. Pas une signature founder. Pas une publication.

# Oracle candidat — CII_example5.xml

**Statut :** CANDIDAT — le founder/lead arbitre. Rien n’entre au corpus sans signature.
**Date de construction :** 16 août 2026 (Europe/Paris)
**Doctrine :** oracle-first. Dérivé de la norme, jamais d’un produit.
**Interdit respecté :** aucune consultation de facturxapi.com.

## Identité de la fixture
- Nom : `CII_example5.xml`
- URL source exacte : chemin `examples/CII_example5.xml` dans [en16931-cii-1.3.16.zip](https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/download/validation-1.3.16/en16931-cii-1.3.16.zip) (tag [validation-1.3.16](https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/tag/validation-1.3.16), consulté 16 août 2026). Horodatage dans le ZIP : 2026-04-09 14:37 (fichier touché dans la release 1.3.16, contrairement à la plupart des examples datés 2025-06-14).
- SHA256 : `473b2f9bd47b807804db7f8729eecbdd4b404c6232aca31262897bd5371d802b`
- Taille : 24 065 octets
- Datetime de téléchargement : 16 août 2026, 00:12 (Europe/Paris)
- Syntaxe : CII D16B
- Dépôt / tag : ConnectingEurope/eInvoicing-EN16931 @ validation-1.3.16

## (1) Ce que la source normative dit que ce document EST

Facture 380 core, double devise (DKK facture / EUR TVA comptable), allowance + charge, acompte, facture de référence.

```xml
<ID>urn:cen.eu:en16931:2017</ID>
<ID>TOSL110</ID>
<TypeCode>380</TypeCode>
<DateTimeString format="102">20130410</DateTimeString>
<InvoiceCurrencyCode>DKK</InvoiceCurrencyCode>
<TaxCurrencyCode>EUR</TaxCurrencyCode>            <!-- BT-6 -->
<Name>SellerCompany</Name>
<ID schemeID="VA">NL16356706</ID>                 <!-- BT-31 -->
<ID schemeID="FC">NL16356706</ID>                 <!-- BT-32 -->
<Name>Buyercompany ltd</Name>
<ID schemeID="VA">DK16356607</ID>                 <!-- BT-48 -->
```

3 lignes : Printing paper 1000 S 25 %, Parker Pen 500 S 25 %, American Cookies 2500 S 12 %. Σ BT-131 = 4000.

BG-20 / BG-21 :

```xml
<Indicator>false</Indicator><ActualAmount>150</ActualAmount>
<ReasonCode>95</ReasonCode><Reason>Loyal customer</Reason>   <!-- allowance -->
<Indicator>true</Indicator><ActualAmount>150</ActualAmount>
<ReasonCode>ABL</ReasonCode><Reason>Packaging</Reason>       <!-- charge -->
```

BG-23 : S 25 % base 1500 tax 375 ; S 12 % base 2500 tax 300.

```xml
<LineTotalAmount>4000.00</LineTotalAmount>
<ChargeTotalAmount>150</ChargeTotalAmount>
<AllowanceTotalAmount>150</AllowanceTotalAmount>
<TaxBasisTotalAmount>4000</TaxBasisTotalAmount>
<TaxTotalAmount currencyID="DKK">675.00</TaxTotalAmount>   <!-- BT-110 -->
<TaxTotalAmount currencyID="EUR">628.62</TaxTotalAmount>   <!-- BT-111 -->
<GrandTotalAmount>4675</GrandTotalAmount>
<TotalPrepaidAmount>2337.5</TotalPrepaidAmount>            <!-- BT-113 -->
<DuePayableAmount>2337.5</DuePayableAmount>
<IssuerAssignedID>TOSL109</IssuerAssignedID>               <!-- BT-25 -->
```

Règles 1.3.16 (même ZIP, 16 août 2026) :

- `[BR-CO-10]` 4000.00 = 1000+500+2500.
- `[BR-CO-11]` / `[BR-CO-12]` 150 = 150.
- `[BR-CO-13]` 4000 − 150 + 150 = 4000.
- `[BR-CO-14]` 375 + 300 = 675.00 (DKK).
- `[BR-CO-15]` 4000 + 675 = 4675.
- `[BR-CO-16]` « Amount due for payment (BT-115) = Invoice total amount with VAT (BT-112) − Paid amount (BT-113) + Rounding amount (BT-114). » — 4675 − 2337.5 = 2337.5 (pas de BT-114).
- `[BR-DEC-15]` décimales de BT-111 (TVA en devise comptable) : 628.62, 2 décimales.
- `[BR-55]` « Each Preceding Invoice reference (BG-3) shall contain a Preceding Invoice reference (BT-25). » — `TOSL109` non vide.
- `[BR-CL-01]` 380 autorisé.

**Règles violées :** aucune — 0 `svrl:failed-assert` sur le XSLT officiel 1.3.16 du même ZIP (consulté et exécuté 16 août 2026, Europe/Paris).

**Validité machine :** XSLT CII 1.3.16, SaxonC-HE 13.0, 16 août 2026 : **0 failed-assert**, 248 fired-rule.

**BR-FR v1.4.0.03 :** non pertinent (core EN, vendeur NL / acheteur DK). [France_RFE v1.4.0.03](https://github.com/fnfempe/France_RFE/releases/tag/v1.4.0.03), 16 août 2026.

## (2) Ce qu’un produit honnête DEVRAIT dire à l’utilisateur

Générable. Facture core avec deux devises, remise + frais, acompte 50 %, référence TOSL109. Ce n’est pas un avoir : BT-3 reste 380 ; BG-3 est une référence antérieure, pas un type 381. Pas de blocage EN16931 1.3.16.

## (3) Points ambigus — DEUX lectures argumentées et sourcées

**Ambiguïté : présence d’une facture référencée (BG-3) sur une facture 380.**

- Lecture A : document de type 380 (UNTDID 1001, `[BR-CL-01]`) ; BG-3 est optionnel et n’en fait pas un avoir. Source : TypeCode observé `380` + texte BR-CL-01 du Schematron 1.3.16.
- Lecture B : un utilisateur peut lire « TOSL109 » comme un avoir partiel. Contre-preuve : pas de `381`, et le release 1.3.16 ([notes](https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/tag/validation-1.3.16), 16 août 2026) distingue explicitement les credit notes (issue BR-CO-25 UBL vs CII). Ici CII 380.

Pas de désaccord SVRL / texte de règle (0 failed-assert).

## (4) Verdict candidat + confiance
- Verdict : **VALIDE EN16931 1.3.16**
- Confiance : **haute** — fixture retouchée dans 1.3.16, 0 failed-assert, totaux et double TVA DKK/EUR cohérents.
- Ce que le founder doit trancher : oracle « facture multi-taux + BT-6/BT-111 + acompte ».
