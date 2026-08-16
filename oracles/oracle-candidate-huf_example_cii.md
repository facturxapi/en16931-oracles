**machine-verified candidate — EN16931 1.3.16 official XSLT**
Statut : CANDIDAT. Pas une signature founder. Pas une publication.

# Oracle candidat — huf_example_cii.xml

**Statut :** CANDIDAT — le founder/lead arbitre. Rien n’entre au corpus sans signature.
**Date de construction :** 16 août 2026 (Europe/Paris)
**Doctrine :** oracle-first. Dérivé de la norme, jamais d’un produit.
**Interdit respecté :** aucune consultation de facturxapi.com.

## Identité de la fixture
- Nom : `huf_example_cii.xml`
- Substitution ZUGFeRD : le 10ᵉ slot devait être un échantillon officiel ZUGFeRD/Factur-X. **non-mesure** — pack officiel derrière un formulaire e-mail.
  - FeRD ZUGFeRD 2.5.2 : [ferd-net.de … zugferd-252-english](https://www.ferd-net.de/en/downloads/publications/details/zugferd-252-english) (consulté 16 août 2026) — citation : « To receive the latest ZUGFeRD release package … please provide the requested details » + champ « E-mail address * ». Le pack « includes … Sample invoices ».
  - FNFE-MPE Factur-X 1.09.2 : [fnfe-mpe.org/factur-x](https://fnfe-mpe.org/factur-x/) (consulté 16 août 2026) — pack exemples à télécharger séparément, historiquement e-mail-gated (consigne de mission).
  - GitHub [ZUGFeRD/corpus](https://github.com/ZUGFeRD/corpus) (consulté 16 août 2026) : README — « temporary, makeshift, **inofficial** samples can be created based on a part of AWV's ZUGFeRD Infopaket ». Pas des fixtures officielles FeRD.
- URL source exacte retenue : chemin `examples/huf_example_cii.xml` dans [en16931-cii-1.3.16.zip](https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/download/validation-1.3.16/en16931-cii-1.3.16.zip) (tag [validation-1.3.16](https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/tag/validation-1.3.16), 16 août 2026). Fallback prévu par la mission.
- SHA256 : `fad73604fc1ff6ac4c762687bdf394d1f4fe14b5b8830d607abf1c1cdfc68758`
- Taille : 111 526 octets
- Datetime de téléchargement : 16 août 2026, 00:12 (Europe/Paris)
- Syntaxe : CII D16B
- Dépôt / tag : ConnectingEurope/eInvoicing-EN16931 @ validation-1.3.16

## (1) Ce que la source normative dit que ce document EST

Facture 380 core, devise **HUF**, TVA S 27 % (Hongrie), vendeur DE avec ID TVA HU, acheteur DE.

```xml
<ID>urn:cen.eu:en16931:2017</ID>
<ID>21/001003559/996</ID>
<TypeCode>380</TypeCode>
<DateTimeString format="102">20211005</DateTimeString>
<InvoiceCurrencyCode>HUF</InvoiceCurrencyCode>
<Name>DKV Euro Service GmbH + Co. KG</Name>
<ID schemeID="VA">HU30048650</ID>
<Name>HIL Heeresinstandsetzungslogistik GmbH</Name>
<ID schemeID="VA">DE242688168</ID>
```

3 lignes carburant DIZEL (LTR) : 23440.00 + 21389.00 + 24351.00 = 69180.00, toutes S 27 %.

```xml
<CalculatedAmount>18679.00</CalculatedAmount>
<BasisAmount>69180.00</BasisAmount>
<CategoryCode>S</CategoryCode>
<RateApplicablePercent>27.00</RateApplicablePercent>
<LineTotalAmount>69180.00</LineTotalAmount>
<TaxBasisTotalAmount>69180.00</TaxBasisTotalAmount>
<TaxTotalAmount currencyID="HUF">18679.00</TaxTotalAmount>
<GrandTotalAmount>87859.00</GrandTotalAmount>
<TotalPrepaidAmount>0.00</TotalPrepaidAmount>
<DuePayableAmount>87859.00</DuePayableAmount>
```

Contrôle : 69180 × 27 % = 18678.6 → document porte 18679.00 (arrondi à l’unité, cohérent avec une monnaie à 0 décimale usuelle HUF, mais stocké avec `.00`).

Règles 1.3.16 (ZIP CII, 16 août 2026) :

- `[BR-CL-04]` « Invoice currency code MUST be coded using ISO code list 4217 alpha-3 » — `HUF` est dans la liste du test (`… HTG HUF IDR …`).
- `[BR-CO-10]` 69180.00 = Σ lignes.
- `[BR-CO-14]` 18679.00 = 18679.00.
- `[BR-CO-15]` 69180 + 18679 = 87859.
- `[BR-CO-17]` / `[BR-S-09]` : le test BR-S-09 autorise une tolérance d’**1** : `(abs(BT-117) - 1 < round(BT-116 * taux) div 100) and (abs(BT-117) + 1 > …)`. 18679 vs 18678.6 : écart 0.40 < 1. Passe.
- `[BR-CO-09]` préfixes `HU` et `DE` dans la liste ISO.
- `[BR-CL-16]` moyen de paiement TypeCode `70` (UNCL 4461).

**Règles violées :** aucune — 0 `svrl:failed-assert` sur le XSLT officiel 1.3.16 du même ZIP (consulté et exécuté 16 août 2026, Europe/Paris).

**Validité machine :** XSLT CII 1.3.16, SaxonC-HE 13.0, 16 août 2026 : **0 failed-assert**, 203 fired-rule.

**BR-FR v1.4.0.03 :** non pertinent (core EN, HUF, parties DE/HU). [France_RFE v1.4.0.03](https://github.com/fnfempe/France_RFE/releases/tag/v1.4.0.03), 16 août 2026.

## (2) Ce qu’un produit honnête DEVRAIT dire à l’utilisateur

Générable. Facture carburant en forint, TVA 27 %. L’arrondi 18678.6 → 18679 est **dans** la tolérance BR-S-09 / BR-CO-17 du Schematron 1.3.16 (fenêtre ±1). Un produit ne doit pas inventer une invalidité d’arrondi. Ce n’est **pas** un échantillon ZUGFeRD officiel (voir identité).

## (3) Points ambigus — DEUX lectures argumentées et sourcées

**Ambiguïté : arrondi HUF 18678.6 vs 18679.00.**

- Lecture A : VALIDE. `[BR-S-09]` (Schematron 1.3.16) : `abs(CalculatedAmount) - 1 < round(BasisAmount * Rate) div 100` — 18679 − 1 = 18678 < 18678.6, et 18679 + 1 > 18678.6. SVRL 0 failed-assert.
- Lecture B : un contrôle « exact 2 décimales sans fenêtre » rejetterait 0.40 d’écart. Ce n’est **pas** le texte 1.3.16. Qualifier « cas limite d’arrondi » côté UX, pas « invalide ».

**Ambiguïté : substitution ZUGFeRD.**

- Lecture A : fallback autorisé (huf_example) dès lors que le pack FeRD/FNFE est e-mail-gated. Sources : pages FeRD et FNFE citées, 16 août 2026.
- Lecture B : les business_02 / _Z / RoundingIssue du même ZIP portent déjà une URN FeRD 1.0 — ce sont des CII ConnectingEurope, pas le pack ZUGFeRD 2.5.2. Ne pas les relabeler « official ZUGFeRD 2.5.2 sample ».

## (4) Verdict candidat + confiance
- Verdict : **VALIDE EN16931 1.3.16** (avec mention UX « arrondi HUF dans la fenêtre ±1 »)
- Confiance : **haute** sur la validité machine ; le slot ZUGFeRD reste **non-mesure** (e-mail gate)
- Ce que le founder doit trancher : garder huf comme 10ᵉ oracle ; éventuellement relancer un téléchargement FeRD **humain** plus tard, hors automate.
