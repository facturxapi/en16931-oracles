# LICENSE-NOTES.md

**Date de lecture des textes :** 16 août 2026 (Europe/Paris).  
**Objet :** obligations de redistribution des **seuls** fichiers CEN
ConnectingEurope EN16931 1.3.16 (exemples XML + XSLT officiels).  
**Hors périmètre :** aucune licence n'est choisie pour le *dépôt* ;
aucune licence n'est choisie pour le *texte* des oracles.

Doctrine : on ne cite que des textes **effectivement lus** ce jour.
On n'invente pas un « oui on peut » au-delà de l'EUPL 1.2 pour ces
fichiers CEN.

---

## 1. Textes effectivement lus (16 août 2026)

| Texte | URL | SHA256 du fichier récupéré | Lecture |
|---|---|---|---|
| `LICENSE.txt` ConnectingEurope (en-tête + EUPL 1.2) | https://raw.githubusercontent.com/ConnectingEurope/eInvoicing-EN16931/master/LICENSE.txt | `fc22ec1dcd8bee4636a395fb332e2308cde870fb3fdc71a2e260b919877cdef5` | lu |
| Page institutionnelle EUPL 1.2 (Joinup / Interoperable Europe) | https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12 | — (page HTML, pas le corps de licence) | lue |
| Texte EUPL 1.2 anglais (liste SPDX, fichier `EUPL-1.2.txt`) | https://raw.githubusercontent.com/spdx/license-list-data/main/text/EUPL-1.2.txt | `57fb42fbcd0b037ce528ed8f72f1ec095d67bc6825ecf1448ff39be1fe68a4b4` | lu |
| Page EUPL 1.2 EN | https://eupl.eu/1.2/en/ | — (HTML) | lue |
| Release `validation-1.3.16` | https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/tag/validation-1.3.16 | — | lue |

Copies jointes dans cette arborescence :

- `LICENSE-EUPL-1.2.txt` — texte EUPL 1.2 anglais (fichier SPDX ci-dessus).
- `vendor/en16931-1.3.16/LICENSE.txt` — `LICENSE.txt` ConnectingEurope, octets identiques à l'URL brute.
- `third-party/LICENSE-ConnectingEurope-EN16931.txt` — même fichier.

Le corps de `LICENSE.txt` ConnectingEurope **est** le texte EUPL 1.2
anglais, précédé de l'en-tête cité au § 2.

---

## 2. Ce que disent les textes

### 2.1 En-tête ConnectingEurope `LICENSE.txt` (citation)

> ====  
> Licensed under European Union Public Licence (EUPL) version 1.2.  
> ====

### 2.2 Corps de la release `validation-1.3.16` (citation, page lue le 16 août 2026)

> For both syntaxes, example documents are contained in the folder "examples".  
> This release of the EN16931 validation artefacts is licensed using European Union Public Licence (EUPL) version 1.2.

Les exemples XML du dossier `examples` des ZIP CII et UBL 1.3.16, ainsi
que les XSLT précompilés, font partie du **Work** couvert par cette
licence de release.

Publication de la release : 13 avril 2026, 12:58:43 UTC
(14:58 PT). Tag : `validation-1.3.16`.

### 2.3 EUPL 1.2 — article 2 (extrait, texte officiel lu)

> The Licensor hereby grants You a worldwide, royalty-free, non-exclusive, sublicensable licence to do the following, for the duration of copyright vested in the Original Work:  
> — use the Work in any circumstance and for all usage,  
> — reproduce the Work,  
> — modify the Work, and make Derivative Works based upon the Work,  
> — communicate to the public, including the right to make available or display the Work or copies thereof to the public […]  
> — distribute the Work or copies thereof,  
> — lend and rent the Work or copies thereof,  
> — sublicense rights in the Work or copies thereof.

### 2.4 EUPL 1.2 — article 5, obligations (extraits, texte officiel lu)

**Attribution :**

> The Licensee shall keep intact all copyright, patent or trademarks notices and all notices that refer to the Licence and to the disclaimer of warranties. The Licensee must include a copy of such notices and a copy of the Licence with every copy of the Work he/she distributes or communicates. The Licensee must cause any Derivative Work to carry prominent notices stating that the Work has been modified and the date of modification.

**Copyleft :**

> If the Licensee distributes or communicates copies of the Original Works or Derivative Works, this Distribution or Communication will be done under the terms of this Licence or of a later version of this Licence unless the Original Work is expressly distributed only under this version of the Licence — for example by communicating ‘EUPL v. 1.2 only’.

Le `LICENSE.txt` ConnectingEurope indique « EUPL version 1.2 ». Il
n'emploie **pas** la formule d'exemple « EUPL v. 1.2 only ». On
redistribue ces fichiers sous **EUPL 1.2** (la version du Work). On
n'ajoute pas de restriction « 1.2 only » que le texte amont n'écrit pas.

**Source Code :**

> When distributing or communicating copies of the Work, the Licensee will provide a machine-readable copy of the Source Code or indicate a repository where this Source will be easily and freely available for as long as the Licensee continues to distribute or communicate the Work.

Les XML d'exemple et les XSLT **sont** le Source Code. Pointeur amont
(dépôt / release officiels) :

- https://github.com/ConnectingEurope/eInvoicing-EN16931
- https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/tag/validation-1.3.16

**Protection des signes :** l'article 5 n'accorde pas le droit d'utiliser
les noms ou marques du Licensor, hors usage raisonnable pour décrire
l'origine du Work.

---

## 3. Application à cette arborescence

| Fichier / famille | Couvert par EUPL 1.2 ? | Modification | Redistribution ici |
|---|---|---|---|
| 10 XML `fixtures/*.xml` (exemples ZIP 1.3.16) | oui (release + LICENSE.txt) | **aucune** — copies non modifiées | oui, avec notices + Licence |
| 2 XSLT `vendor/en16931-1.3.16/xslt/*.xslt` | oui | **aucune** — copies non modifiées | oui, avec notices + Licence |
| `NOTICE`, `LICENSE-*.txt`, `third-party/` | notices / Licence elles-mêmes | — | jointes (art. 5 attribution) |
| `oracles/*.md`, `oracles/INDEX.md` | **non** | — | licence du *texte* = **non décidée** |
| `oracles/receipts/*.svrl.xml` | sortie machine de l'XSLT officiel sur un exemple officiel ; pas une modification du Work | — | recette de reproduction, pas un fork XSLT |
| `scripts/validate.py`, `README.md`, `LICENSE-NOTES.md` | **non** (textes / outils de ce pack) | — | licence du *dépôt* = **non décidée** |

**Copies non modifiées.** Les 10 XML et les 2 XSLT ont les SHA256 du
ZIP officiel (voir `SHA256SUMS`, `fixtures/SHA256SUMS`,
`vendor/en16931-1.3.16/XSLT.SHA256SUMS`). Aucun octet n'a été édité.

---

## 4. Ce que cette note ne décide pas

- **Licence du dépôt** (code / prose FacturXAPI) : non décidée.
  Ce fichier n'en choisit aucune (ni MIT, ni Apache-2.0, ni EUPL pour le repo).
- **Licence du texte des oracles** : non décidée. L'EUPL 1.2
  du Work ConnectingEurope ne s'étend pas à nos markdowns.
- **Factur-X / ZUGFeRD / FNFE / FeRD / lots 001–015 / AFNOR** : hors
  périmètre. Aucun de ces binaires n'est redistribué ici.
- **Publication** : ce dépôt public est `facturxapi/en16931-oracles`.
  La note ci-dessus documente les licences des artefacts redistribués ;
  elle ne date pas d'une préparation hors git.

---

## 5. Comment un tiers respecte l'EUPL s'il redistribue les XML/XSLT

1. Conserver les notices (ce `NOTICE`, l'en-tête ConnectingEurope, le
   présent fichier).
2. Joindre la Licence (`LICENSE-EUPL-1.2.txt` et/ou
   `vendor/en16931-1.3.16/LICENSE.txt`).
3. Redistribuer ces fichiers du Work sous EUPL 1.2 (ou version
   ultérieure, le texte amont n'ayant pas dit « 1.2 only »).
4. Fournir le Source Code (les XML/XSLT eux-mêmes) ou un pointeur vers
   le dépôt ConnectingEurope / la release `validation-1.3.16`.
5. Si l'on **modifie** un XML ou un XSLT : mentionner la modification
   et sa date (art. 5). **Ce pack ne le fait pas.**

---

## BR-FR / France_RFE Flux2 (pack `brfr/`) — notes lues 16 août 2026

**Objet :** redistribution des **seuls** fichiers Flux2 utilisés sous
`brfr/vendor/v1.4.0.02/` et `brfr/vendor/v1.4.0.03/` (`.sch` / `.xslt`
UBL+CII Flux2), **sans** zipball entier (le zipball amont embarque aussi
des artefacts CEN / XSD UBL hors périmètre de ce pack).

### Textes / sources

| Texte | Source | Copie jointe |
|---|---|---|
| Apache License 2.0 (LICENSE racine du tag France_RFE) | https://raw.githubusercontent.com/fnfempe/France_RFE/v1.4.0.03/LICENSE | `brfr/vendor/LICENSE-APACHE-2.0-France_RFE.txt` |
| En-têtes Schematron Flux2 (verbatim) | fichiers `.sch` vendored | inchangés |

### Licence applicable

- Licence de redistribution des copies **non modifiées** utilisées ici :
  **Apache-2.0** (LICENSE du dépôt amont au tag `v1.4.0.03`, mesurée 11357 octets).
- Les en-têtes `.sch` citent **« European Union Public Licence (EUPL) version 1.4.0 »**.
  **Aucune EUPL 1.4.0 n’existe** dans le catalogue EUPL connu (Joinup / eupl.eu) —
  anomalie d’en-tête amont (confusion probable avec la version du Schematron /
  du pack France_RFE). Les `.sch` sont redistribués ici sous **Apache-2.0**
  uniquement (autorité du LICENSE racine du tag). L’en-tête « EUPL version 1.4.0 »
  est documenté comme anomalie d’en-tête ; on n’invente **aucune** autre licence
  EUPL pour ces fichiers France_RFE.
- Aucun usage du nom **FNFE** comme marque ; références factuelles au dépôt
  `fnfempe/France_RFE` uniquement.
- Les XSLT compilés n’ont pas de NOTICE séparée : le `.sch` source est conservé
  à côté de chaque `.xslt` exécuté.

