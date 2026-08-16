# Objectif A — UBL BT-128 espace, .02 vs .03

Fixture unique : `ubl-bt128-espace.xml`.
C’est `fixtures/ubl-synth-S1-bt128-pass.xml` avec **une** substitution :

`OBJET-FICTIF-001` → `OBJET FICTIF 001` (espaces dans BT-128 / `InvoiceLine/cac:DocumentReference/cbc:ID`, TypeCode 130).

Même fichier, deux XSLT :

| Tag | XSLT SHA256 | failed-assert | id |
|---|---|---:|---|
| v1.4.0.02 | `e308eade08e21ad69881328a2c14290ec2877b02b7ec873531baf82aae2f6628` | 1 | `BR-FR-02_EXT-FR-FE-136` |
| v1.4.0.03 | `4a54e8b363907b7ca13c6d63302910aa7e42681fdaa6d16ef18b9a414973c09c` | 0 | — |

SVRL côte à côte :

- `../receipts/v1.4.0.02/objective-a/ubl-bt128-espace.svrl.xml`
- `../receipts/v1.4.0.03/objective-a/ubl-bt128-espace.svrl.xml`

Verdict : **faux positif corrigé** (reproduit, pas déduit du blurb de release).
