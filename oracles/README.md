# oracles/

**Statut :** CANDIDAT. Pas une signature founder. Pas une publication.

Chaque fichier `oracle-candidate-*.md` porte en tête la bannière :

```
**machine-verified candidate — EN16931 1.3.16 official XSLT**
Statut : CANDIDAT. Pas une signature founder. Pas une publication.
```

La doctrine existante n'a pas été réécrite. Licence du *texte* :
**À-TRANCHER (founder)**. L'EUPL 1.2 couvre les XML/XSLT CEN, pas ces
markdowns.

`INDEX.md` est la copie de l'index des 10 candidats (16 août 2026).

## Recettes machine (`receipts/`)

Pour chaque fixture :

| Fichier | Contenu |
|---|---|
| `<stem>.svrl.xml` | SVRL brut, XSLT officiel 1.3.16, SaxonC-HE 13.0 |
| `<stem>.receipt.md` | SHA256 fixture, chemin + SHA256 XSLT, moteur, date 16 Aug 2026 PT, comptes `fired-rule` / `failed-assert`, phrase machine-verified |

Normatif pour la reproduction :

- `receipts/RESULTS.json` — tableau trié par nom de fichier ; clés
  triées ; **sans horloge murale**
- `receipts/RESULTS.sha256` — SHA256 du JSON canonique

Le verdict machine attendu : **10 × 0 `svrl:failed-assert`**.
`LIMITE` (index) reste 0 failed-assert.

Reproduire : voir `/scripts/README.md` et la commande du `/README.md`.
