# Diffs mutants — une ligne sémantique

Originaux dans `fixtures/` **jamais modifiés** après verrouillage (`fixtures/SHA256SUMS`).
Les ids ci-dessous sont l’attribut `id` des `svrl:failed-assert` produits par
`vendor/v1.4.0.03/.../BR-FR-Flux2-Schematron-*.xslt` (SaxonC-HE 13.0), 16 août 2026 PT.

| Mutant | Original | Changement (une ligne) | failed | ids SVRL |
|---|---|---|---:|---|
| `ubl-id-espace.xml` | `ubl-synth-S1-pass.xml` | BT-1 `SYNTH-BRFR-0001` → `SYNTH BRFR 0001` | 2 | `BR-FR-01_BT-1-2`, `BR-FR-02_BT-1` |
| `ubl-date-annee.xml` | `ubl-synth-S1-pass.xml` | BT-2 `2026-08-16` → `1999-08-16` | 1 | `BR-FR-03_BT-2` |
| `ubl-type-invalide.xml` | `ubl-synth-S1-pass.xml` | BT-3 `380` → `999` | 1 | `BR-FR-04_BT-3` |
| `ubl-note-pmt-absent.xml` | `ubl-synth-S1-pass.xml` | note `#PMT#FICTIF` → `#XXX#FICTIF` | 1 | `BR-FR-05_BT-22-1` |
| `ubl-profile-invalide.xml` | `ubl-synth-S1-pass.xml` | BT-23 `S1` → `XX` | 1 | `BR-FR-08_BT-23` |
| `ubl-siren-vendeur-court.xml` | `ubl-synth-S1-pass.xml` | BT-30 `000000000` → `00000000` | 2 | `BR-FR-10_BT-30`, `BR-FR-32-LEGALID` |
| `ubl-tva-taux.xml` | `ubl-synth-S1-pass.xml` | BT-119 `20.00` → `21.00` (ligne BT-152 inchangée) | 1 | `BR-FR-16_BT-119` |
| `cii-id-espace.xml` | `cii-synth-S1-pass.xml` | BT-1 `SYNTH-BRFR-C001` → `SYNTH BRFR C001` | 1 | `BR-FR-02_BT-1` |

SVRL : `mutants/receipts/v1.4.0.03/<stem>.svrl.xml`.
