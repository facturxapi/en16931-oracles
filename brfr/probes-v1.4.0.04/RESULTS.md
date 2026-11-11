# Sondes France_RFE `.03` vs `.04` (SaxonC-HE 13.0.0)

Chaque fichier de `inputs/` part d'une fixture synthétique de `../fixtures/` et ne change qu'un point.
Moteur : `saxonche==13.0.0`, XSLT non modifiés de `../vendor/`. `ERREUR` = la transformation s'arrête sur une erreur dynamique XPath/XSLT : **aucun SVRL n'est produit**, il n'y a ni « pass » ni « fail ».

| Sonde | Ce qui change | `.03` | `.04` | Écart |
|---|---|---|---|---|
| `cii-c1-bar-b2cint.xml` | BAR=B2CINT (CII) — seul le texte du message change | pass | pass | non |
| `cii-c10-b2-paid-empty.xml` | cadre B2, montant payé vide (CII) | BR-FR-CO-09_BT-23-1, BR-FR-DEC-01_BT-113 | ERREUR FORG0001 (conversion xs:decimal) | oui |
| `cii-c1b-bar-b2c.xml` | BAR=B2C (CII), témoin | pass | pass | non |
| `cii-c2-issue-date-slash.xml` | date d'émission « 16/08/2026 » (CII) | BR-FR-03_BT-2 | BR-FR-03_BT-2 | non |
| `cii-c3-due-date-slash.xml` | échéance « 15/09/2026 » (CII) | BR-FR-03_BT-9, BR-FR-CO-07_BT-9 | BR-FR-03_BT-9, BR-FR-CO-07_BT-9 | non |
| `cii-c4-two-due-dates-both-ok.xml` | deux échéances, toutes postérieures à l'émission (CII) | ERREUR XPTY0004 (séquence de plusieurs éléments comparée par `ge`) | pass | oui |
| `cii-c5-two-due-dates-one-before-issue.xml` | deux échéances, l'une antérieure à l'émission (CII) | ERREUR XPTY0004 (séquence de plusieurs éléments comparée par `ge`) | BR-FR-CO-07_BT-9 | oui |
| `cii-c6-one-due-date-before-issue.xml` | une échéance antérieure à l'émission (CII), témoin | BR-FR-CO-07_BT-9 | BR-FR-CO-07_BT-9 | non |
| `cii-c7-empty-due-date.xml` | échéance vide (CII) | BR-FR-03_BT-9 | BR-FR-03_BT-9 | non |
| `cii-c8-b2-paid-nonnumeric.xml` | cadre B2, montant payé « abc » (CII) | BR-FR-CO-09_BT-23-1, BR-FR-DEC-01_BT-113 | ERREUR FORG0001 (conversion xs:decimal) | oui |
| `cii-c9-b2-paid-ok.xml` | cadre B2, montant payé = total (CII), témoin | pass | pass | non |
| `ubl-u1-issue-date-slash.xml` | date d'émission « 16/08/2026 » (UBL) | BR-FR-03_BT-2 | ERREUR FORG0001 (conversion xs:decimal) | oui |
| `ubl-u2-bar-note-split-two-notes.xml` | note BAR répartie sur deux cbc:Note (« #BAR#B2 » + « B# ») | pass | BR-FR-20_BT-21 | oui |
| `ubl-u2b-bar-b2cint.xml` | BAR=B2CINT (UBL) | pass | pass | non |
| `ubl-u2c-bar-b2c-endpoint-mismatch-type389.xml` | BAR=B2C, endpoint ≠ SIREN, type 389 | BR-FR-22_BT-34 | pass | oui |
| `ubl-u2c-bar-b2c-endpoint-mismatch.xml` | BAR=B2C, endpoint ≠ SIREN, type 380 | pass | pass | non |
| `ubl-u2d-bar-b2b-endpoint-mismatch-type389.xml` | BAR=B2B, endpoint ≠ SIREN, type 389 | BR-FR-22_BT-34 | BR-FR-22_BT-34 | non |
| `ubl-u2d-bar-b2b-endpoint-mismatch.xml` | BAR=B2B, endpoint ≠ SIREN, type 380 | pass | pass | non |
| `ubl-u2e-b1-type389-endpoint-ok.xml` | type 389, endpoint = SIREN, témoin | pass | pass | non |
| `ubl-u3-paymentduedate-before-issue-no-duedate.xml` | PaymentMeans/PaymentDueDate antérieure à l'émission, sans cbc:DueDate | pass | BR-FR-CO-07_BT-9 | oui |
| `ubl-u3b-paymentduedate-ok-no-duedate.xml` | PaymentMeans/PaymentDueDate valide, sans cbc:DueDate, témoin | pass | pass | non |
| `ubl-u3c-duedate-ok-paymentduedate-before.xml` | cbc:DueDate valide + PaymentDueDate antérieure | pass | BR-FR-CO-07_BT-9 | oui |
| `ubl-u4-b2-prepaid-nonnumeric.xml` | cadre B2, PrepaidAmount « abc » (UBL) | BR-FR-CO-09_BT-23-1, BR-FR-DEC-01_BT-113 | ERREUR FORG0001 (conversion xs:decimal) | oui |
| `ubl-u4b-b2-prepaid-ok.xml` | cadre B2, PrepaidAmount = total (UBL), témoin | pass | pass | non |

24 sondes, 10 écarts `.03` → `.04`.

## Lecture

- `.04` remplace `number()` par `xs:decimal()` pour les dates (année, mois, jour), les montants payé/à payer et les sommes de lignes : une valeur non numérique ou vide fait désormais **échouer la transformation** (FORG0001) là où `.03` produisait un `failed-assert`. Côté CII, une date au format local reste un `failed-assert BR-FR-03_*` ; côté UBL, la date d'émission au format local arrête la transformation.
- `.04` accepte plusieurs échéances en CII (`every $dt in $dueDate satisfies $dt ge $issueDate`) ; `.03` s'arrêtait sur XPTY0004.
- `.04` UBL lit aussi `cac:PaymentMeans/cbc:PaymentDueDate` comme échéance (`BR-FR-CO-07_BT-9`).
- `.04` UBL joint les `cbc:Note` avec `#` (`.03` : sans séparateur) : une note BAR répartie sur deux éléments est désormais refusée (`BR-FR-20_BT-21`).
- `.04` UBL ne contrôle l'endpoint SIREN (`BR-FR-22_BT-34`) que pour un traitement BAR `B2B`.
- B2CINT : accepté par `.03` comme par `.04` (aucun écart de verdict) ; en CII, le texte du message de `BR-FR-20` ajoute B2CINT.

## Non sondé

- Lignes `GROUP` (UBL, `DocumentStatusCode` `('DETAIL', 'GROUP')`) : demande un jeu EXTENDED-CTC-FR complet, absent des fixtures.
- Sommes des contrats spéciaux (cadres 8/9) en `xs:decimal` : même motif que ci-dessus, non rejoué.

## Rejouer

```bash
python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt
.venv/bin/python probes-v1.4.0.04/replay.py            # affiche le tableau
.venv/bin/python probes-v1.4.0.04/replay.py --write    # rafraîchit results.json
```

`scripts/validate.py` s'arrête sur la première erreur dynamique ; `replay.py` continue et note la ligne ERREUR.

Fichiers synthétiques uniquement, aucune facture client.
