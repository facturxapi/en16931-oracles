# Sondes d'angles morts — copies seulement

XML mutés (une ligne) + recettes SVRL officielles. Les originaux restent dans `../fixtures/`.

- Lot principal : `*.xml` ici, recettes dans `receipts/`
- Notations scientifiques (FORG0001, pas de SVRL) : `engine-errors/`
- Rapport : `../GAPS.md`

**Modified work notice (EUPL 1.2, art. 5).** The XML files in this folder and in `engine-errors/` are modified copies of ConnectingEurope EN16931 validation examples (one line changed in each, see `../GAPS.md`), modified between 16 Aug 2026 and 10 Nov 2026. They stay under EUPL 1.2 (`../LICENSE-EUPL-1.2.txt`, `../NOTICE`).

Ne pas valider `engine-errors/*.xml` via `scripts/validate.py` : Saxon lève avant d'écrire un SVRL.
