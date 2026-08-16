**machine-verified candidate — EN16931 1.3.16 official XSLT**
Statut : CANDIDAT. Pas une signature founder. Pas une publication.

# Oracle candidat — XRechnung-O.xml

**Statut :** CANDIDAT — le founder/lead arbitre. Rien n’entre au corpus sans signature.
**Date de construction :** 16 août 2026 (Europe/Paris)
**Doctrine :** oracle-first. Dérivé de la norme, jamais d’un produit.
**Interdit respecté :** aucune consultation de facturxapi.com.

## Identité de la fixture
- Nom : `XRechnung-O.xml`
- URL source exacte : chemin `examples/XRechnung-O.xml` dans [en16931-cii-1.3.16.zip](https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/download/validation-1.3.16/en16931-cii-1.3.16.zip) (tag [validation-1.3.16](https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/tag/validation-1.3.16), consulté 16 août 2026).
- SHA256 : `399acf31a9c7ce4722b1362fe429f8326a132a0a9c01e5792e4f6bc266c982bb`
- Taille : 11 914 octets
- Datetime de téléchargement : 16 août 2026, 00:12 (Europe/Paris)
- Syntaxe : CII D16B
- Dépôt / tag : ConnectingEurope/eInvoicing-EN16931 @ validation-1.3.16

## (1) Ce que la source normative dit que ce document EST

Facture 380 core, **catégorie O (Not subject to VAT)** — assurances, taxe d’assurance en charges document, noms anonymisés « XX ». BT-24 = URN EN16931, **pas** une URN XRechnung CIUS.

```xml
<ID>urn:cen.eu:en16931:2017</ID>                 <!-- BT-24 core, pas XR -->
<ID>150377292</ID>
<TypeCode>380</TypeCode>
<DateTimeString format="102">20210114</DateTimeString>
<InvoiceCurrencyCode>EUR</InvoiceCurrencyCode>
<Name>XX</Name>
<ID schemeID="FC">XX</ID>                       <!-- BT-32, pas BT-31 VA -->
<Name>XX</Name>
```

2 lignes cat O, unités ZZ : 83654.15 + 252646.80 = 336300.95. Deux charges « Versicherungssteuer » (ZZZ), cat O : 15894.27 + 33349.38 = 49243.65.

```xml
<CalculatedAmount>0.00</CalculatedAmount>
<ExemptionReason>Versicherungen sind von der Umsatzsteuer befreit.</ExemptionReason>
<BasisAmount>385544.60</BasisAmount>
<CategoryCode>O</CategoryCode>
<ExemptionReasonCode>vatex-eu-132-1a</ExemptionReasonCode>
<RateApplicablePercent>0.0000</RateApplicablePercent>
<LineTotalAmount>336300.95</LineTotalAmount>
<ChargeTotalAmount>49243.65</ChargeTotalAmount>
<TaxBasisTotalAmount>385544.60</TaxBasisTotalAmount>
<GrandTotalAmount>385544.60</GrandTotalAmount>
<DuePayableAmount>385544.60</DuePayableAmount>
```

**BT-110 (`TaxTotalAmount`) est absent.** BT-112 = BT-109 (pas de TVA ajoutée).

Règles 1.3.16 (même ZIP, 16 août 2026) :

- `[BR-O-01]` lignes/charges O ⇒ exactement un BG-23 O — observé.
- `[BR-O-02]` « shall **not** contain the Seller VAT identifier (BT-31) … or the Buyer VAT identifier (BT-48) » — pas de `schemeID="VA"` ; seul BT-32 `FC` = `XX`.
- `[BR-O-09]` BT-117 = 0 — `CalculatedAmount` 0.00.
- `[BR-O-10]` « shall have a VAT exemption reason code (BT-121) … or a VAT exemption reason text (BT-120) » — les deux présents (`vatex-eu-132-1a` / texte DE).
- `[BR-O-11]` pas d’autre catégorie que O.
- `[BR-CO-13]` 336300.95 + 49243.65 = 385544.60.
- `[BR-DEC-13]` « The allowed maximum number of decimals for … (BT-110) is 2. » — test : `not(ram:TaxTotalAmount) or …` : **l’absence de BT-110 est explicitement tolérée** par ce test.
- `[BR-CL-22]` VATEX : `vatex-eu-132-1a` (art. 132-1-a assurances).

**Règles violées :** aucune — 0 `svrl:failed-assert` sur le XSLT officiel 1.3.16 du même ZIP (consulté et exécuté 16 août 2026, Europe/Paris).

**Validité machine :** XSLT CII 1.3.16, SaxonC-HE 13.0, 16 août 2026 : **0 failed-assert**, 135 fired-rule.

**BR-FR v1.4.0.03 :** non pertinent (DE, cat O assurance, core EN). [France_RFE v1.4.0.03](https://github.com/fnfempe/France_RFE/releases/tag/v1.4.0.03), 16 août 2026.

## (2) Ce qu’un produit honnête DEVRAIT dire à l’utilisateur

Générable en core EN16931. Ce n’est **pas** une validation XRechnung (pas d’URN `urn:xoev-de:kosit:standard:xrechnung` dans BT-24). C’est une facture EN16931 catégorie O (hors champ TVA) avec taxe d’assurance en BG-21. Un produit ne doit pas exiger BT-31 (interdit par BR-O-02) ni inventer une TVA. L’absence de BT-110 n’est pas un failed-assert 1.3.16 (BR-DEC-13 prévoit `not(ram:TaxTotalAmount)`).

## (3) Points ambigus — DEUX lectures argumentées et sourcées

**Ambiguïté 1 — « XRechnung » dans le nom vs BT-24 core.**

- Lecture A : exemple ConnectingEurope pour la catégorie O, nommé XRechnung-O ; BT-24 = `urn:cen.eu:en16931:2017`. Valide **EN16931 core**, pas le CIUS XRechnung. Source : XML observé + BR-01.
- Lecture B : un utilisateur allemand attend les règles XRechnung (BT-10 Buyer reference, etc.). **non-mesure** XRechnung : le ZIP 1.3.16 ne contient pas le Schematron KoSIT.

**Ambiguïté 2 — BT-110 absent vs BR-CO-14/15.**

- Lecture A : VALIDE. BR-DEC-13 autorise l’absence ; pour O, TVA = 0 donc BT-112 = BT-109. SVRL 0 failed-assert.
- Lecture B : le texte de `[BR-CO-14]` « Invoice total VAT amount (BT-110) = Σ VAT category tax amount (BT-117) » suppose un BT-110. Si la règle est contextualisée sur `ram:TaxTotalAmount`, elle ne se déclenche pas en son absence. Désaccord possible texte / implémentation — ici le SVRL et BR-DEC-13 s’accordent sur « pas d’échec ».

**Ambiguïté 3 — `RateApplicablePercent` 0.0000 sur BG-23 O.**

- `[BR-O-05]` interdit le taux **en ligne** (BT-152), pas explicitement en BG-23. Présence d’un taux 0 en en-tête : non sanctionnée (0 failed-assert).

## (4) Verdict candidat + confiance
- Verdict : **VALIDE EN16931 1.3.16** (catégorie O) — **pas** une preuve de conformité XRechnung
- Confiance : **haute** sur EN16931 core ; **basse** sur tout claim XRechnung
- Ce que le founder doit trancher : libellé de l’oracle (« exemple O / assurance » vs « XRechnung »).
