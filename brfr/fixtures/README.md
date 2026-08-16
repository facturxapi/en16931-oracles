# Fixtures synthétiques BR-FR

Documents **inventés** pour exercer le Schematron Flux2 officiel.
Aucun identifiant réel, aucun client, aucun RIB, aucun moyen de paiement.

Identifiants volontairement faux : SIREN `000000000` / `111111111`,
EndpointID identiques, noms « SOCIETE FICTIVE … », adresses « RUE FICTIVE / FICTIVILLE / 00000 ».

| Fichier | Syntaxe | Profil (BT-23) | Particularité | Verdict Flux2 .02 | Verdict Flux2 .03 |
|---|---|---|---|---|---|
| `ubl-synth-S1-pass.xml` | UBL | S1 | minimal | 0 failed-assert | 0 failed-assert |
| `ubl-synth-S1-bt128-pass.xml` | UBL | S1 | + BT-128 `OBJET-FICTIF-001` TypeCode 130 | 0 | 0 |
| `ubl-synth-B1-pass.xml` | UBL | B1 | + note `#BAR#B2B#` | 0 | 0 |
| `cii-synth-S1-pass.xml` | CII | S1 | minimal CII | 0 | 0 |

`CustomizationID` / guideline : `urn:cen.eu:en16931:2017#compliant#urn.cpro.gouv.fr:1p0:en16931-ctc-fr`
(Flux2 ne teste pas cet URI ; `ProfileID` / BT-23 est testé par `BR-FR-08`).

SHA256 : `SHA256SUMS`. Ne pas modifier ces fichiers.
