**machine-verified candidate — EN16931 1.3.16 official XSLT**
Statut : candidat machine-vérifié (0 failed-assert sur le XSLT officiel 1.3.16).
Pas une signature produit. Pas une preuve CIUS / Factur-X / BR-FR.

# Index des oracles candidats EN16931 1.3.16

**Statut :** candidat machine-vérifié — le verdict définitif d'admission
au corpus reste ouvert (voir la question en fin de note).
**Date de construction :** 16 août 2026 (Europe/Paris)
**Doctrine :** oracle-first. Dérivé de la norme, jamais d’un produit.

## Artefacts téléchargés

| Artefact | URL | SHA256 | Taille | Téléchargé |
|---|---|---|---|---|
| ZIP CII 1.3.16 | https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/download/validation-1.3.16/en16931-cii-1.3.16.zip | `1cd53cb8a84d38aedc82c0caede217da983a7934dd663f793a092fd66443c561` | 226 664 o | 16 août 2026 00:12 PT |
| ZIP UBL 1.3.16 | https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/download/validation-1.3.16/en16931-ubl-1.3.16.zip | `bafada015efbc5248bf5e05ad2191e1d9833ef96e9dd5f4bce420a747342da85` | 2 650 024 o | 16 août 2026 00:12 PT |
| Release notes | https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/tag/validation-1.3.16 | — | — | 16 août 2026 |
| Listing examples CII | https://github.com/ConnectingEurope/eInvoicing-EN16931/tree/master/cii/examples | — | — | 16 août 2026 |

Validation machine : XSLT officiels `xslt/EN16931-CII-validation.xslt` et `xslt/EN16931-UBL-validation.xslt` des mêmes ZIP, SaxonC-HE 13.0, local, 16 août 2026. **Aucun appel à un validateur commercial.**

## Les 10 fichiers

| # | Fichier oracle | Fixture | URL source | SHA256 | Verdict candidat |
|---|---|---|---|---|---|
| 1 | [oracle-candidate-CII_example1.md](oracle-candidate-CII_example1.md) | CII_example1.xml | ZIP CII `examples/CII_example1.xml` | `0c12e3ca9aab58299e6271b89d061274694c62159510ca2d848f13d287ee4f99` | **VALIDE EN16931 1.3.16** — facture 380 EUR, 20 lignes S 6/21 %, 0 failed-assert |
| 2 | [oracle-candidate-CII_example3.md](oracle-candidate-CII_example3.md) | CII_example3.xml | ZIP CII `examples/CII_example3.xml` | `eda939773fa9556acb411555ef2e73df8d1eabe1d2c9ba99445a00abf889db6d` | **VALIDE EN16931 1.3.16** — substitution de CII_example2 (doublon de business_01) ; abonnement + charge DKK |
| 3 | [oracle-candidate-CII_example5.md](oracle-candidate-CII_example5.md) | CII_example5.xml | ZIP CII `examples/CII_example5.xml` | `473b2f9bd47b807804db7f8729eecbdd4b404c6232aca31262897bd5371d802b` | **VALIDE EN16931 1.3.16** — touché 1.3.16 ; DKK+EUR ; allowance/charge ; acompte |
| 4 | [oracle-candidate-CII_business_example_01.md](oracle-candidate-CII_business_example_01.md) | CII_business_example_01.xml | ZIP CII `examples/CII_business_example_01.xml` | `2ce8286333f4c2019166c505642963e1222f54c18558ae4210fd41fd5d526b2f` | **VALIDE EN16931 1.3.16** — = CII_example2 ; NOK ; retours ; cat E |
| 5 | [oracle-candidate-CII_business_example_02.md](oracle-candidate-CII_business_example_02.md) | CII_business_example_02.xml | ZIP CII `examples/CII_business_example_02.xml` | `53a636ac10592aa6fdc280190a366955380a64883519a4d58926b96802eb7163` | **LIMITE** — 0 failed-assert mais BT-24 = `urn:ferd:…:1p0:comfort` |
| 6 | [oracle-candidate-CII_business_example_Z.md](oracle-candidate-CII_business_example_Z.md) | CII_business_example_Z.xml | ZIP CII `examples/CII_business_example_Z.xml` | `68222346e14dfff673ae32b349f4efef054bd8e55f10370d0fcba1ec55262d56` | **LIMITE** — cat Z OK ; profil FeRD 1.0 ; BT-31 atypique |
| 7 | [oracle-candidate-CII-BR-CO-10-RoundingIssue.md](oracle-candidate-CII-BR-CO-10-RoundingIssue.md) | CII-BR-CO-10-RoundingIssue.xml | ZIP CII `examples/CII-BR-CO-10-RoundingIssue.xml` | `04711e7a649e3f28bf4e54cff901fd8cab5e6fdc91141c60a0553b9f0784a998` | **LIMITE** — BR-CO-10 **ne échoue pas** (0=0) ; nom trompeur ; totaux nuls |
| 8 | [oracle-candidate-XRechnung-O.md](oracle-candidate-XRechnung-O.md) | XRechnung-O.xml | ZIP CII `examples/XRechnung-O.xml` | `399acf31a9c7ce4722b1362fe429f8326a132a0a9c01e5792e4f6bc266c982bb` | **VALIDE EN16931 1.3.16** (cat O) — **pas** une preuve XRechnung CIUS |
| 9 | [oracle-candidate-ubl-tc434-creditnote1.md](oracle-candidate-ubl-tc434-creditnote1.md) | ubl-tc434-creditnote1.xml | ZIP UBL `examples/ubl-tc434-creditnote1.xml` | `911d7ac2cb4fa72d21331c76914468e7d94eda03629e0def75c64ab18e3e9dce` | **VALIDE EN16931 1.3.16** — avoir UBL 381, cat E, sans BT-25 |
| 10 | [oracle-candidate-huf_example_cii.md](oracle-candidate-huf_example_cii.md) | huf_example_cii.xml | ZIP CII `examples/huf_example_cii.xml` | `fad73604fc1ff6ac4c762687bdf394d1f4fe14b5b8830d607abf1c1cdfc68758` | **VALIDE EN16931 1.3.16** — HUF 27 % ; fallback ZUGFeRD (e-mail gate) |

## Blockers / non-mesure

1. **Pack ZUGFeRD 2.5.2 / Factur-X 1.09.2** : e-mail gate FeRD (`E-mail address *` sur ferd-net.de, 16 août 2026) et FNFE-MPE. Corpus GitHub ZUGFeRD/corpus autoproclamé « inofficial ». Aucun XML ZUGFeRD officiel téléchargeable sans e-mail. Slot 10 = `huf_example_cii.xml`.
2. **BR-FR v1.4.0.03** : [fnfempe/France_RFE v1.4.0.03](https://github.com/fnfempe/France_RFE/releases/tag/v1.4.0.03) (16 août 2026). Aucune des 10 fixtures n’est un document CTC-FR / EXTENDED-CTC-FR. BR-FR non appliqué.
3. **CII_example2.xml** : doublon binaire de `CII_business_example_01.xml`. Remplacé par `CII_example3.xml`. Aucun CII du ZIP n’a BT-3 ≠ 380 ; l’avoir est le UBL `ubl-tc434-creditnote1.xml`.
4. **BR-CO-25** : cité dans les notes de release 1.3.16 (issue #477) mais **id absent** du Schematron préprocessé → non-mesure, non inventé.
5. **Saxon JAR Maven** : `Saxon-HE-12.5.jar` n'est pas le runner de ce dépôt ; runner effectif = `saxonche` 13.0 (Saxonica) via pip. Même famille XSLT 2.0, artefact XSLT = celui du ZIP officiel.

## Recette SVRL (tous 0 failed-assert)

| Fixture | fired-rule | failed-assert |
|---|---|---|
| CII_example1.xml | 423 | 0 |
| CII_example3.xml | 89 | 0 |
| CII_example5.xml | 248 | 0 |
| CII_business_example_01.xml | 287 | 0 |
| CII_business_example_02.xml | 117 | 0 |
| CII_business_example_Z.xml | 106 | 0 |
| CII-BR-CO-10-RoundingIssue.xml | 140 | 0 |
| XRechnung-O.xml | 135 | 0 |
| ubl-tc434-creditnote1.xml | 53 | 0 |
| huf_example_cii.xml | 203 | 0 |
