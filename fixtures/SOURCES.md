# SOURCES.md

**Date :** 16 août 2026 (Europe/Paris).

Les 10 XML de `fixtures/` sont extraits, octets pour octets, des ZIP
officiels ConnectingEurope eInvoicing-EN16931 **validation-1.3.16**.
Aucune modification.

## Release

- Page : https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/tag/validation-1.3.16
- Publiée : 13 avril 2026, 12:58:43 UTC (14:58 PT)
- Citation lue le 16 août 2026 :

> For both syntaxes, example documents are contained in the folder "examples".  
> This release of the EN16931 validation artefacts is licensed using European Union Public Licence (EUPL) version 1.2.

## ZIP

| ZIP | URL | SHA256 | Taille |
|---|---|---|---|
| CII 1.3.16 | https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/download/validation-1.3.16/en16931-cii-1.3.16.zip | `1cd53cb8a84d38aedc82c0caede217da983a7934dd663f793a092fd66443c561` | 226 664 o |
| UBL 1.3.16 | https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/download/validation-1.3.16/en16931-ubl-1.3.16.zip | `bafada015efbc5248bf5e05ad2191e1d9833ef96e9dd5f4bce420a747342da85` | 2 650 024 o |

ZIP déjà présents sur disque le 16 août 2026 ; SHA256 revérifiés avant
copie. Pas de re-téléchargement (empreintes concordantes).

## Fichiers

| Fichier | ZIP | Chemin dans le ZIP | SHA256 du fichier | Date |
|---|---|---|---|---|
| `CII_example1.xml` | CII | `examples/CII_example1.xml` | `0c12e3ca9aab58299e6271b89d061274694c62159510ca2d848f13d287ee4f99` | 16 août 2026 |
| `CII_example3.xml` | CII | `examples/CII_example3.xml` | `eda939773fa9556acb411555ef2e73df8d1eabe1d2c9ba99445a00abf889db6d` | 16 août 2026 |
| `CII_example5.xml` | CII | `examples/CII_example5.xml` | `473b2f9bd47b807804db7f8729eecbdd4b404c6232aca31262897bd5371d802b` | 16 août 2026 |
| `CII_business_example_01.xml` | CII | `examples/CII_business_example_01.xml` | `2ce8286333f4c2019166c505642963e1222f54c18558ae4210fd41fd5d526b2f` | 16 août 2026 |
| `CII_business_example_02.xml` | CII | `examples/CII_business_example_02.xml` | `53a636ac10592aa6fdc280190a366955380a64883519a4d58926b96802eb7163` | 16 août 2026 |
| `CII_business_example_Z.xml` | CII | `examples/CII_business_example_Z.xml` | `68222346e14dfff673ae32b349f4efef054bd8e55f10370d0fcba1ec55262d56` | 16 août 2026 |
| `CII-BR-CO-10-RoundingIssue.xml` | CII | `examples/CII-BR-CO-10-RoundingIssue.xml` | `04711e7a649e3f28bf4e54cff901fd8cab5e6fdc91141c60a0553b9f0784a998` | 16 août 2026 |
| `XRechnung-O.xml` | CII | `examples/XRechnung-O.xml` | `399acf31a9c7ce4722b1362fe429f8326a132a0a9c01e5792e4f6bc266c982bb` | 16 août 2026 |
| `ubl-tc434-creditnote1.xml` | UBL | `examples/ubl-tc434-creditnote1.xml` | `911d7ac2cb4fa72d21331c76914468e7d94eda03629e0def75c64ab18e3e9dce` | 16 août 2026 |
| `huf_example_cii.xml` | CII | `examples/huf_example_cii.xml` | `fad73604fc1ff6ac4c762687bdf394d1f4fe14b5b8830d607abf1c1cdfc68758` | 16 août 2026 |

## XSLT officiels (même ZIP, même date)

| Fichier | ZIP | Chemin dans le ZIP | SHA256 |
|---|---|---|---|
| `EN16931-CII-validation.xslt` | CII | `xslt/EN16931-CII-validation.xslt` | `0b234dea2bbfee739b7761e607a992c17fab88773014ef56355b6158cfb1cc53` |
| `EN16931-UBL-validation.xslt` | UBL | `xslt/EN16931-UBL-validation.xslt` | `39f9d282867f1a49e7708d9e29a53da89643e1ee56f10cec1ebcf1277595fcbd` |

Vendored sous `/vendor/en16931-1.3.16/xslt/`.
