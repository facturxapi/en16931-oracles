# Diffs sondes gaps-fr — une ligne sémantique

Originaux dans `fixtures/` **jamais modifiés** (`sha256sum -c fixtures/SHA256SUMS` : 4 × OK).
Moteur : Flux2 v1.4.0.03, SaxonC-HE 13.0, 16 Aug 2026 PT.

| Sonde | Original | Changement (une ligne) |
|---|---|---|
| `ubl-siren-123456789.xml` | S1-pass | BT-30 vendeur `000000000` → `123456789` |
| `ubl-siren-court.xml` | S1-pass | BT-30 vendeur → `12345678` |
| `ubl-siren-lettres.xml` | S1-pass | BT-30 vendeur → `AAAAAAAAA` |
| `ubl-siren-espaces.xml` | S1-pass | BT-30 vendeur → ` 000000000 ` |
| `cii-siren-123456789.xml` | CII-pass | BT-30 vendeur `000000000` → `123456789` |
| `cii-siren-lettres.xml` | CII-pass | BT-30 vendeur → `AAAAAAAAA` |
| `ubl-pmt-vide.xml` | S1-pass | `#PMT#FICTIF` → `#PMT#` |
| `ubl-pmt-dot.xml` | S1-pass | `#PMT#FICTIF` → `#PMT#.` |
| `ubl-pmt-na.xml` | S1-pass | `#PMT#FICTIF` → `#PMT#n/a` |
| `ubl-pmd-ws.xml` | S1-pass | `#PMD#FICTIF` → `#PMD#` + 3 espaces |
| `cii-pmt-vide.xml` | CII-pass | Content PMT `FICTIF` → vide |
| `cii-pmt-dot.xml` | CII-pass | Content PMT → `.` |
| `cii-pmt-na.xml` | CII-pass | Content PMT → `n/a` |
| `ubl-s1-type-381.xml` | S1-pass | BT-3 `380` → `381` |
| `ubl-vat-z-20.xml` | S1-pass | BT-118 `S` → `Z` (taux 20.00 inchangé) |
| `ubl-siren-meme.xml` | S1-pass | BT-47 acheteur `111111111` → `000000000` |
| `ubl-bt24-garbage.xml` | S1-pass | BT-24 URI CTC-FR → `urn:example:not-a-ctc-fr-profile` |
| `ubl-date-order.xml` | S1-pass | BT-9 `2026-09-15` → `2026-08-01` |
| `ubl-b4-acompte.xml` | S1-pass | BT-23 `S1` → `B4` et BT-3 `380` → `386` (paire) |
| `ubl-id-lead-space.xml` | S1-pass | BT-1 préfixe espace |
| `ubl-id-trail-space.xml` | S1-pass | BT-1 suffixe espace |
| `ubl-id-nbsp.xml` | S1-pass | BT-1 espaces → NBSP U+00A0 |
| `ubl-id-long.xml` | S1-pass | BT-1 36 caractères |
| `ubl-id-hyphen.xml` | S1-pass | BT-1 `SYNTH-BRFR-0001-OK` |
| `ubl-date-2026-02-31.xml` | S1-pass | BT-2 → `2026-02-31` |
| `cii-date-20260231.xml` | CII-pass | BT-2 → `20260231` |
| `cii-date-suffix.xml` | CII-pass | BT-2 → `20260816XX` |
| `cii-date-20260431.xml` | CII-pass | BT-9 → `20260431` |
| `ubl-bt128-espace.xml` | S1-bt128 | BT-128 `OBJET-FICTIF-001` → `OBJET FICTIF 001` |
| `ubl-vat-20-000.xml` | S1-pass | BT-119 `20.00` → `20.000` |
