# LICENSE-NOTES.md

**Date de lecture des textes :** 16 août 2026 (Europe/Paris) ; release 1.3.17 lue le 18 oct. 2026.  
**Objet :** obligations de redistribution des fichiers CEN
ConnectingEurope EN16931 1.3.17 (exemples XML + XSLT officiels) et des
fichiers France_RFE Flux2 `v1.4.0.02`, `v1.4.0.03` et `v1.4.0.04` (`brfr/vendor/`) ;
licence du dépôt (décision du 11 novembre 2026, § 4).

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
| Release `validation-1.3.17` | https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/tag/validation-1.3.17 | — | lue le 18 oct. 2026 |
| `LICENSE.txt` au tag `validation-1.3.17` | https://raw.githubusercontent.com/ConnectingEurope/eInvoicing-EN16931/validation-1.3.17/LICENSE.txt | `fc22ec1dcd8bee4636a395fb332e2308cde870fb3fdc71a2e260b919877cdef5` (identique) | lu le 18 oct. 2026 |

Copies jointes dans cette arborescence :

- `LICENSE-EUPL-1.2.txt` — texte EUPL 1.2 anglais (fichier SPDX ci-dessus).
- `vendor/en16931-1.3.17/LICENSE.txt` — `LICENSE.txt` ConnectingEurope, octets identiques à l'URL brute.
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

### 2.2 bis Corps de la release `validation-1.3.17` (citation, page lue le 18 oct. 2026)

> For both syntaxes, example documents are contained in the folder "examples".  
> This release of the EN16931 validation artefacts is licensed using European Union Public Licence (EUPL) version 1.2.

Publication : 12 octobre 2026, 12:28:45 UTC. Tag : `validation-1.3.17`. Même licence que 1.3.16.

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
- https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/tag/validation-1.3.17

**Protection des signes :** l'article 5 n'accorde pas le droit d'utiliser
les noms ou marques du Licensor, hors usage raisonnable pour décrire
l'origine du Work.

---

## 3. Application à cette arborescence

| Fichier / famille | Couvert par EUPL 1.2 ? | Modification | Redistribution ici |
|---|---|---|---|
| 10 XML `fixtures/*.xml` (exemples ZIP 1.3.17) | oui (release + LICENSE.txt) | **aucune** — copies non modifiées | oui, avec notices + Licence |
| 2 XSLT `vendor/en16931-1.3.17/xslt/*.xslt` | oui | **aucune** — copies non modifiées | oui, avec notices + Licence |
| `variants/533/` : `patches/*.patch`, `xslt/V1`, `xslt/V2`, `probes/` | oui (œuvre dérivée du Work 1.3.17) | **oui** — sources Schematron CII modifiées le 8 nov. 2026 (V1 / V2) et XSLT régénérés ; sondes = copies modifiées de 2 exemples ; mention de modification et date dans `variants/533/README.md` | oui, sous EUPL 1.2 (copyleft, art. 5) |
| `variants/533/xslt/BASE` | oui | **aucune** sur les sources — tag `validation-1.3.17` reconstruit par la chaîne amont (sans l'en-tête de licence de 5 lignes) | oui, avec notices + Licence |
| `NOTICE`, `LICENSE-*.txt`, `third-party/` | notices / Licence elles-mêmes | — | jointes (art. 5 attribution) |
| `gaps/*.xml`, `gaps/engine-errors/*.xml`, `mutants/*.xml` | oui (œuvres dérivées des exemples 1.3.16 / 1.3.17) | **oui** — une ligne modifiée par fichier ; mention de modification dans `gaps/README.md` et `mutants/README.md` | oui, sous EUPL 1.2 (art. 5) |
| `oracles/*.md`, `oracles/INDEX.md` | **non** | — | prose FacturX API = **CC-BY-4.0** (décision du 11 nov. 2026) |
| `*/receipts/*`, `RESULTS.json`, `RESULTS.sha256` | sortie machine de l'XSLT officiel ; pas une modification du Work | — | **EUPL 1.2** (décision du 11 nov. 2026) |
| `scripts/`, `tests/`, `.github/workflows/`, `variants/533/*.py`, `brfr/scripts/` | **non** (outils FacturX API) | — | **EUPL 1.2** (décision du 11 nov. 2026) |
| `README.md`, `GAPS.md`, `MUTANTS.md`, `MAPPING-PROOF.md`, `LICENSE-NOTES.md` et autres notes `.md` | **non** (prose FacturX API) | — | **CC-BY-4.0** (décision du 11 nov. 2026) |

**Copies non modifiées.** Les 10 XML et les 2 XSLT ont les SHA256 du
ZIP officiel (voir `SHA256SUMS`, `fixtures/SHA256SUMS`,
`vendor/en16931-1.3.17/XSLT.SHA256SUMS`). Aucun octet n'a été édité.

---

## 4. Licence du dépôt — décision du 11 novembre 2026

| Contenu | Licence |
|---|---|
| Fichiers CEN non modifiés (`fixtures/`, `vendor/en16931-*`) | EUPL-1.2 (amont, inchangé) |
| Sondes, mutants, `variants/533` (copies modifiées d'exemples CEN) | EUPL-1.2 (œuvres dérivées, art. 5) |
| Nos scripts, tests, workflows, recettes, fichiers `RESULTS` | EUPL-1.2 |
| Prose : README, GAPS.md, `oracles/*.md`, notes | CC-BY-4.0 |
| `brfr/vendor/` (France_RFE non modifié) | Apache-2.0 (amont, inchangé) |

Attribution : « FacturX API (facturxapi.com) ». Textes : `LICENSE` (copie de
`LICENSE-EUPL-1.2.txt`), `LICENSE-CC-BY-4.0.txt` (legalcode lu sur
https://creativecommons.org/licenses/by/4.0/legalcode.txt le 11 nov. 2026,
SHA256 `9ba9550ad48438d0836ddab3da480b3b69ffa0aac7b7878b5a0039e7ab429411`,
18657 octets ; copie du dépôt sans la dernière ligne vide finale),
`brfr/vendor/LICENSE-APACHE-2.0-France_RFE.txt`.

Hors périmètre :

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
   `vendor/en16931-1.3.17/LICENSE.txt`).
3. Redistribuer ces fichiers du Work sous EUPL 1.2 (ou version
   ultérieure, le texte amont n'ayant pas dit « 1.2 only »).
4. Fournir le Source Code (les XML/XSLT eux-mêmes) ou un pointeur vers
   le dépôt ConnectingEurope / la release `validation-1.3.17`.
5. Si l'on **modifie** un XML ou un XSLT : mentionner la modification
   et sa date (art. 5). Ce dépôt le fait pour `gaps/`, `mutants/` et
   `variants/533/` (mention dans le README de chaque dossier).

---

## BR-FR / France_RFE Flux2 (pack `brfr/`) — notes lues 16 août 2026

**Objet :** redistribution des **seuls** fichiers Flux2 utilisés sous
`brfr/vendor/v1.4.0.02/`, `brfr/vendor/v1.4.0.03/` et `brfr/vendor/v1.4.0.04/` (`.sch` / `.xslt`
UBL+CII Flux2), **sans** zipball entier (le zipball amont embarque aussi
des artefacts CEN / XSD UBL hors périmètre de ce pack).

### Textes / sources

| Texte | Source | Copie jointe |
|---|---|---|
| Apache License 2.0 (LICENSE racine du tag France_RFE) | https://raw.githubusercontent.com/fnfempe/France_RFE/v1.4.0.03/LICENSE | `brfr/vendor/LICENSE-APACHE-2.0-France_RFE.txt` |
| Apache License 2.0 au tag `v1.4.0.04` (commit `97ba0f3d`), lu le 11 nov. 2026 | https://raw.githubusercontent.com/fnfempe/France_RFE/v1.4.0.04/LICENSE | même fichier : SHA256 `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4`, 11357 octets, identique à la copie jointe |
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

