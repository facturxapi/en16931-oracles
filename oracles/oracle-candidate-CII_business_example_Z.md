**machine-verified candidate — EN16931 1.3.16 official XSLT**
Statut : CANDIDAT. Pas une signature founder. Pas une publication.

# Oracle candidat — CII_business_example_Z.xml

**Statut :** CANDIDAT — le founder/lead arbitre. Rien n’entre au corpus sans signature.
**Date de construction :** 16 août 2026 (Europe/Paris)
**Doctrine :** oracle-first. Dérivé de la norme, jamais d’un produit.
**Interdit respecté :** aucune consultation de facturxapi.com.

## Identité de la fixture
- Nom : `CII_business_example_Z.xml`
- URL source exacte : chemin `examples/CII_business_example_Z.xml` dans [en16931-cii-1.3.16.zip](https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/download/validation-1.3.16/en16931-cii-1.3.16.zip) (tag [validation-1.3.16](https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/tag/validation-1.3.16), consulté 16 août 2026).
- SHA256 : `68222346e14dfff673ae32b349f4efef054bd8e55f10370d0fcba1ec55262d56`
- Taille : 8 779 octets
- Datetime de téléchargement : 16 août 2026, 00:12 (Europe/Paris)
- Syntaxe : CII D16B
- Dépôt / tag : ConnectingEurope/eInvoicing-EN16931 @ validation-1.3.16

## (1) Ce que la source normative dit que ce document EST

Facture 380 EUR, **catégorie TVA Z (zero rated)** sur toutes les lignes, une ligne négative (« Abzug »), BT-24 = ZUGFeRD 1.0 Comfort.

```xml
<ID>urn:ferd:CrossIndustryDocument:invoice:1p0:comfort</ID>
<ID>2016166</ID>
<TypeCode>380</TypeCode>
<DateTimeString format="102">20150109</DateTimeString>
<InvoiceCurrencyCode>EUR</InvoiceCurrencyCode>
<Name>XXX AG</Name>
<ID schemeID="VA">DE37/302/30168</ID>
<Name>XXX AG</Name>
```

Lignes : 12122.59 (Festpreis) ; −606.13 (Abzug) ; 177.41. Σ = 11693.87. Toutes cat Z, taux 0.00.

```xml
<CalculatedAmount>0.00</CalculatedAmount>
<TypeCode>VAT</TypeCode>
<BasisAmount>11693.87</BasisAmount>
<CategoryCode>Z</CategoryCode>
<RateApplicablePercent>0.00</RateApplicablePercent>
<LineTotalAmount>11693.87</LineTotalAmount>
<TaxBasisTotalAmount>11693.87</TaxBasisTotalAmount>
<TaxTotalAmount currencyID="EUR">0.0</TaxTotalAmount>
<GrandTotalAmount>11693.87</GrandTotalAmount>
<DuePayableAmount>11693.87</DuePayableAmount>
```

Règles 1.3.16 (même ZIP, 16 août 2026) :

- `[BR-Z-01]` ligne Z ⇒ exactement un BG-23 Z — observé.
- `[BR-Z-05]` « Invoiced item VAT rate (BT-152) shall be 0 (zero) » — 0.00.
- `[BR-Z-09]` « VAT category tax amount (BT-117) … "Zero rated" shall equal 0 » — 0.00.
- `[BR-Z-10]` « shall **not** have a VAT exemption reason code (BT-121) or VAT exemption reason text (BT-120) » — ni `ExemptionReason` ni `ExemptionReasonCode` dans le BG-23. Conforme (Z ≠ E).
- `[BR-CO-10]` 11693.87 = Σ lignes ; `[BR-CO-15]` 11693.87 + 0.0 = 11693.87.
- `[BR-01]` BT-24 non vide (URN FeRD 1.0).
- `[BR-CO-09]` préfixe `DE` accepté. La valeur `DE37/302/30168` ressemble à un Steuernummer, pas à une USt-IdNr (DE+9 chiffres) — **non-mesure** par le Schematron (préfixe seulement).

**Règles violées :** aucune — 0 `svrl:failed-assert` sur le XSLT officiel 1.3.16 du même ZIP (consulté et exécuté 16 août 2026, Europe/Paris).

**Validité machine :** XSLT CII 1.3.16, SaxonC-HE 13.0, 16 août 2026 : **0 failed-assert**, 106 fired-rule.

**BR-FR v1.4.0.03 :** non pertinent. [France_RFE v1.4.0.03](https://github.com/fnfempe/France_RFE/releases/tag/v1.4.0.03), 16 août 2026.

## (2) Ce qu’un produit honnête DEVRAIT dire à l’utilisateur

Pas bloqué par EN16931 1.3.16. Distinguer :

- **métier EN16931 catégorie Z** : cohérent (taux 0, taxe 0, pas de motif d’exonération — BR-Z-10) ;
- **profil hors EN16931** : même URN FeRD 1.0 Comfort que business_02 ;
- **identifiant fiscal** `DE37/302/30168` sous `schemeID="VA"` : douteux comme BT-31, non sanctionné par BR-CO-09.

Générable. La ligne négative « Abzug » n’en fait pas un avoir (BT-3 = 380).

## (3) Points ambigus — DEUX lectures argumentées et sourcées

**Ambiguïté 1 — profil FeRD 1.0 (identique à business_02).**

- Lecture A : VALIDE machine, BR-01 satisfait. Source : test BR-01 + SVRL 0 failed-assert.
- Lecture B : profil hors EN16931. Source : valeur BT-24 observée `urn:ferd:CrossIndustryDocument:invoice:1p0:comfort`.

**Ambiguïté 2 — BT-31 `DE37/302/30168`.**

- Lecture A : BR-CO-09 ne teste que le préfixe ISO ; `DE` est dans la liste du Schematron 1.3.16. SVRL OK.
- Lecture B : en droit allemand, un Steuernummer n’est pas une USt-IdNr ; `schemeID="VA"` (BT-31) est sémantiquement douteux. **non-mesure** EN16931 (pas de BR de format national).

## (4) Verdict candidat + confiance
- Verdict : **LIMITE** (machine VALIDE ; profil FeRD 1.0 + identifiant fiscal atypique)
- Confiance : **moyenne**
- Ce que le founder doit trancher : oracle « catégorie Z + profil FeRD 1.0 » vs scinder profil et TVA Z.
