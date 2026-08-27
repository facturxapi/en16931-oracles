# mapping/fixtures/ — synthétiques

**Date :** 16 août 2026 (Europe/Paris) — 16 Aug 2026 PT

Copies **mutées** d'exemples officiels CEN EN16931 validation-1.3.16.
Pas des factures privées. Les fixtures CEN racine (`fixtures/`) n'ont pas été modifiées.

| Fichier | Base officielle | Mutation |
|---|---|---|
| `CII-SR-470-no-bt84.xml` | `fixtures/CII_example3.xml` | un seul `SpecifiedTradeSettlementPaymentMeans` TypeCode 30, **sans** `IBANID` ni `ProprietaryID` |
| `CII-SR-467-divergent-bt81.xml` | `fixtures/CII_example3.xml` | second TypeCode `30` → `58` (BT-84 conservé) |
| `CII-BR-CO-25-absent.xml` | `fixtures/CII_example3.xml` | suppression de `SpecifiedTradePaymentTerms` (BT-9 / BT-20), BT-115 reste 1125 |
| `ubl-SR-47-divergent-bt81.xml` | `fixtures/ubl-tc434-creditnote1.xml` | second `PaymentMeans` code 30 (BT-84 présent) |
| `ubl-BR-61-no-bt84.xml` | `fixtures/ubl-tc434-creditnote1.xml` | code `1` → `30`, `PayeeFinancialAccount` retiré |

Empreintes : `SHA256SUMS` (ce dossier).
Licence des bases : EUPL 1.2 (ConnectingEurope / eInvoicing-EN16931).
