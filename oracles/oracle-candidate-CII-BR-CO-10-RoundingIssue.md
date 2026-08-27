**machine-verified candidate — EN16931 1.3.16 official XSLT**
Statut : candidat machine-vérifié (0 failed-assert sur le XSLT officiel 1.3.16).
Pas une signature produit. Pas une preuve CIUS / Factur-X / BR-FR.

# Oracle candidat — CII-BR-CO-10-RoundingIssue.xml

**Statut :** candidat machine-vérifié — le verdict définitif d'admission
au corpus reste ouvert (voir la question en fin de note).
**Date de construction :** 16 août 2026 (Europe/Paris)
**Doctrine :** oracle-first. Dérivé de la norme, jamais d’un produit.

## Identité de la fixture
- Nom : `CII-BR-CO-10-RoundingIssue.xml`
- URL source exacte : chemin `examples/CII-BR-CO-10-RoundingIssue.xml` dans [en16931-cii-1.3.16.zip](https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/download/validation-1.3.16/en16931-cii-1.3.16.zip) (tag [validation-1.3.16](https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/tag/validation-1.3.16), consulté 16 août 2026).
- SHA256 : `04711e7a649e3f28bf4e54cff901fd8cab5e6fdc91141c60a0553b9f0784a998`
- Taille : 12 181 octets
- Datetime de téléchargement : 16 août 2026, 00:12 (Europe/Paris)
- Syntaxe : CII D16B
- Dépôt / tag : ConnectingEurope/eInvoicing-EN16931 @ validation-1.3.16

## (1) Ce que la source normative dit que ce document EST

Le **nom** suggère un échec BR-CO-10. La **norme 1.3.16** ne le confirme pas. Document 380, totaux à zéro, 4 lignes qui s’annulent (billet + storno), catégories S 19 % et Z 0 %, BT-24 FeRD 1.0 Comfort.

```xml
<ID>urn:ferd:CrossIndustryDocument:invoice:1p0:comfort</ID>
<ID>0</ID>                                          <!-- BT-1 -->
<TypeCode>380</TypeCode>
<DateTimeString format="102">20210326</DateTimeString>
<InvoiceCurrencyCode>EUR</InvoiceCurrencyCode>
<Name>Seller GmbH</Name>
<ID schemeID="VA">DE 123 456 789</ID>
<Name>BuyerName</Name>
```

Lignes BT-131 : 720.81 (S 19) ; 0.01 (Z) ; −720.81 (S 19) ; −0.01 (Z). Σ = 0.00.

```xml
<LineTotalAmount>0.00</LineTotalAmount>
<ChargeTotalAmount>0</ChargeTotalAmount>
<AllowanceTotalAmount>0</AllowanceTotalAmount>
<TaxBasisTotalAmount>0.00</TaxBasisTotalAmount>
<TaxTotalAmount currencyID="EUR">0.00</TaxTotalAmount>
<GrandTotalAmount>0.00</GrandTotalAmount>
<TotalPrepaidAmount>0</TotalPrepaidAmount>
<DuePayableAmount>0.00</DuePayableAmount>
<IssuerAssignedID>0</IssuerAssignedID>              <!-- BG-3 / BT-25 -->
```

BG-23 : Z base 0.00 tax 0.00 ; S 19 % base 0.00 tax 0.00.

Règle visée, citation brute (`EN16931-CII-validation-preprocessed.sch`, ZIP 1.3.16, 16 août 2026) :

```
[BR-CO-10]-Sum of Invoice line net amount (BT-106) = Σ Invoice line net amount (BT-131).
test: xs:decimal(ram:LineTotalAmount) = round(xs:decimal(sum(../../ram:IncludedSupplyChainTradeLineItem/ram:SpecifiedLineTradeSettlement/ram:SpecifiedTradeSettlementLineMonetarySummation/ram:LineTotalAmount)) * xs:decimal(100)) div xs:decimal(100)
```

Calcul : 720.81 + 0.01 + (−720.81) + (−0.01) = 0.00 = BT-106. **BR-CO-10 est satisfaite.** Le `round(…*100) div 100` n’a rien à arrondir ici.

Autres BR : `[BR-02]` BT-1 non vide — la valeur `0` n’est pas vide. `[BR-55]` BT-25 = `0` non vide. `[BR-Z-09]` / `[BR-S-09]` taxes 0. `[BR-01]` URN FeRD 1.0 non vide.

**Règles violées :** aucune — 0 `svrl:failed-assert` sur le XSLT officiel 1.3.16 du même ZIP (consulté et exécuté 16 août 2026, Europe/Paris).

**Validité machine :** XSLT CII 1.3.16, SaxonC-HE 13.0, 16 août 2026 : **0 failed-assert**, 140 fired-rule. **Ne pas inventer une invalidité** à partir du nom de fichier.

**BR-FR v1.4.0.03 :** non pertinent. [France_RFE v1.4.0.03](https://github.com/fnfempe/France_RFE/releases/tag/v1.4.0.03), 16 août 2026.

## (2) Ce qu’un produit honnête DEVRAIT dire à l’utilisateur

Cas limite d’annulation (storno), **pas** un échec BR-CO-10 mesurable en 1.3.16. Un produit qui dirait « invalide BR-CO-10 » à cause du nom de fichier mentirait. Dire plutôt : « totaux nuls, lignes qui s’annulent, le Schematron 1.3.16 n’émet aucun failed-assert ; le profil déclaré est ZUGFeRD 1.0 Comfort ; le numéro de facture est "0". » Générable au sens machine. Réparable si l’utilisateur veut un profil EN16931 (BT-24) ou un vrai numéro.

## (3) Points ambigus — DEUX lectures argumentées et sourcées

**Ambiguïté 1 — le nom « RoundingIssue » vs le Schematron actuel.**

- Lecture A : **valide BR-CO-10**. Texte + test 1.3.16 + arithmétique 0.00 = 0.00 + SVRL 0 failed-assert. Source : ZIP 1.3.16, règle citée ci-dessus.
- Lecture B : le fichier a été déposé comme *repro* d’un ancien écart d’arrondi (souvent BR-CO-17 / TVA sur 720.81 × 19 % = 136.9539). En 1.3.16 les bases S/Z sont déjà à 0.00 : l’écart n’est plus observable. **non-mesure** de l’intention historique au-delà du nom.

**Ambiguïté 2 — profil FeRD 1.0 + BT-1 = "0".**

- Lecture A : BR-01 et BR-02 ne testent que le non-vide. SVRL OK.
- Lecture B : URN hors EN16931 ; un numéro `0` est un placeholder. Qualité métier faible, hors BR.

## (4) Verdict candidat + confiance
- Verdict : **LIMITE** (machine VALIDE EN16931 1.3.16, y compris BR-CO-10 ; nom trompeur ; profil FeRD 1.0 ; totaux nuls)
- Confiance : **haute** sur « BR-CO-10 ne échoue pas » ; **moyenne** sur l’intention du fichier.
- Question ouverte : oracle « ne pas croire le nom de fichier » — interdit d’enseigner une invalidité BR-CO-10 sans SVRL.
