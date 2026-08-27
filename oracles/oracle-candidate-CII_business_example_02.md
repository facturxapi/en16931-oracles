**machine-verified candidate — EN16931 1.3.16 official XSLT**
Statut : candidat machine-vérifié (0 failed-assert sur le XSLT officiel 1.3.16).
Pas une signature produit. Pas une preuve CIUS / Factur-X / BR-FR.

# Oracle candidat — CII_business_example_02.xml

**Statut :** candidat machine-vérifié — le verdict définitif d'admission
au corpus reste ouvert (voir la question en fin de note).
**Date de construction :** 16 août 2026 (Europe/Paris)
**Doctrine :** oracle-first. Dérivé de la norme, jamais d’un produit.

## Identité de la fixture
- Nom : `CII_business_example_02.xml`
- URL source exacte : chemin `examples/CII_business_example_02.xml` dans [en16931-cii-1.3.16.zip](https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/download/validation-1.3.16/en16931-cii-1.3.16.zip) (tag [validation-1.3.16](https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/tag/validation-1.3.16), consulté 16 août 2026).
- SHA256 : `53a636ac10592aa6fdc280190a366955380a64883519a4d58926b96802eb7163`
- Taille : 10 178 octets
- Datetime de téléchargement : 16 août 2026, 00:12 (Europe/Paris)
- Syntaxe : CII D16B
- Dépôt / tag : ConnectingEurope/eInvoicing-EN16931 @ validation-1.3.16

## (1) Ce que la source normative dit que ce document EST

Petite facture 380 EUR, 3 lignes S 19 %, **BT-24 = URN ZUGFeRD 1.0 Comfort** (pas l’URN EN16931 2017).

```xml
<ID>urn:ferd:CrossIndustryDocument:invoice:1p0:comfort</ID>  <!-- BT-24 -->
<ID>INV000013</ID>
<TypeCode>380</TypeCode>
<DateTimeString format="102">20130825</DateTimeString>
<InvoiceCurrencyCode>EUR</InvoiceCurrencyCode>
<Name>xxxx</Name>
<ID schemeID="VA">DE1111111</ID>
<Name>Buyercompany ltd</Name>
```

Lignes : 1.26 + 1.26 + 7.48 = 10.00. BG-23 S 19 % tax 1.90.

```xml
<LineTotalAmount>10.00</LineTotalAmount>
<ChargeTotalAmount>0.00</ChargeTotalAmount>
<AllowanceTotalAmount>0.00</AllowanceTotalAmount>
<TaxBasisTotalAmount>10.00</TaxBasisTotalAmount>
<TaxTotalAmount currencyID="EUR">1.90</TaxTotalAmount>
<GrandTotalAmount>11.90</GrandTotalAmount>
<DuePayableAmount>11.90</DuePayableAmount>
```

Règles 1.3.16 (même ZIP, 16 août 2026) :

- `[BR-01]` « An Invoice shall have a Specification identifier (BT-24). » — test : `normalize-space(…/ram:ID) != ''`. L’URN FeRD 1.0 **satisfait** ce test (non-vide). Le Schematron core **ne contraint pas** la valeur de BT-24 à `urn:cen.eu:en16931:2017`.
- `[BR-CO-10]` 10.00 = 10.00 ; `[BR-CO-15]` 10.00 + 1.90 = 11.90 ; `[BR-CO-17]` 10 × 19 % = 1.90.
- `[BR-CO-09]` préfixe ISO du BT-31 : `DE1111111` commence par `DE` (présent dans la liste du test). Le Schematron ne vérifie pas la longueur d’une USt-IdNr allemande.
- `[BR-CL-01]` 380 autorisé.

**Règles violées :** aucune — 0 `svrl:failed-assert` sur le XSLT officiel 1.3.16 du même ZIP (consulté et exécuté 16 août 2026, Europe/Paris).

**Validité machine EN16931 1.3.16 :** XSLT officiel, SaxonC-HE 13.0, 16 août 2026 : **0 failed-assert**, 117 fired-rule. Aucune BR du pack 1.3.16 n’est violée.

**Profil :** hors EN16931 *en intention* (ZUGFeRD 1.0 Comfort, pré-2017) mais **dans** le périmètre du test BR-01 tel qu’écrit.

**BR-FR v1.4.0.03 :** non pertinent (pas CTC-FR ; URN FeRD 1.0). [France_RFE v1.4.0.03](https://github.com/fnfempe/France_RFE/releases/tag/v1.4.0.03), 16 août 2026.

## (2) Ce qu’un produit honnête DEVRAIT dire à l’utilisateur

Pas bloqué par EN16931 1.3.16 (machine). Distinguer clairement :

- **valide métier EN16931 (additions, TVA S)** : oui selon le XSLT 1.3.16 ;
- **profil hors EN16931** : BT-24 est `urn:ferd:CrossIndustryDocument:invoice:1p0:comfort`, pas `urn:cen.eu:en16931:2017`. Un produit honnête doit afficher « profil ZUGFeRD 1.0 Comfort déclaré — le validateur EN16931 core n’interdit pas cette URN, il exige seulement un BT-24 non vide (BR-01) ».
- TVA vendeur `DE1111111` : format atypique (USt-IdNr DE = DE + 9 chiffres). Non-mesure côté EN16931 (BR-CO-09 ne teste que le préfixe).

Générable au sens EN16931 core. Réparable si l’utilisateur vise un profil EN16931 / Factur-X EN16931 : remplacer BT-24.

## (3) Points ambigus — DEUX lectures argumentées et sourcées

**Ambiguïté : BT-24 FeRD 1.0 vs EN16931.**

- Lecture A : **valide EN16931 1.3.16**. `[BR-01]` ne teste que le non-vide. SVRL 1.3.16 : 0 failed-assert. Source : `EN16931-CII-validation-preprocessed.sch` du ZIP 1.3.16, test `normalize-space(…) != ''`.
- Lecture B : **profil hors EN16931**. L’URN `urn:ferd:CrossIndustryDocument:invoice:1p0:comfort` identifie ZUGFeRD 1.0 Comfort (pré-EN16931). ConnectingEurope livre ce fichier comme « example » du pack de *validation EN16931*, ce qui n’en fait pas un document EN16931-identifié. Un CIUS / un profil Factur-X EN16931 exigerait une autre URN.

Pas de désaccord SVRL / texte BR-01 : les deux lectures portent sur *ce que BR-01 devrait exiger*, pas sur ce qu’il exige.

## (4) Verdict candidat + confiance
- Verdict : **LIMITE** (machine VALIDE EN16931 1.3.16 ; profil déclaré hors EN16931)
- Confiance : **moyenne** — 0 failed-assert est un fait ; l’interprétation « EST une facture EN16931 » dépend de la lecture de BT-24.
- Question ouverte : oracle « LIMITE profil FeRD 1.0 » ou « VALIDE car BR-01 ne contraint pas l’URN ».
