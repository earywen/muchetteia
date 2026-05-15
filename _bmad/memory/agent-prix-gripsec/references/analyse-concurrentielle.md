---
name: Analyse Concurrentielle
code: AC
description: Comparaison des prix avec les concurrents et ajustement du positionnement sans guerre des prix.
---

# Analyse Concurrentielle

## Ce que vous devez accomplir (Outcome)

Évaluer le positionnement tarifaire de La Muchette par rapport à une liste de concurrents, et proposer des ajustements de prix chirurgicaux qui maintiennent la compétitivité tout en préservant la rentabilité minimale.

## Intégration Mémoire

Consultez `{agent.margin_targets}`. Si le fait de s'aligner sur un concurrent fait tomber le produit sous la marge cible, refusez de vous aligner.
Consultez `{agent.no_discount_list}`.

## Déroulement

1. **Ingestion** : L'utilisateur fournit la liste de nos prix (export Hiboutik) et les benchmarks.
2. **Exécution du Script** : Utilisez `calc_margins.py` en passant le fichier de benchmarks en argument `--benchmarks`.
3. **Vérification (Protocole Zéro Erreur)** :
   - Si le script indique un `match_confidence` < 85%, vous DEVEZ utiliser l'outil `search_web` pour confirmer l'identité du produit.
   - Si le doute persiste, demandez une validation manuelle à l'utilisateur avant d'émettre une recommandation.
4. **Stratégie & Prudence** :
   - **Plafond Marché** : Ne proposez jamais de prix supérieur au `market_max` constaté.
   - **Pragmatisme** : Si une augmentation est nécessaire pour atteindre la marge cible, limitez-la à +20% par étape pour préserver l'acceptabilité client.
   - **Arrondi** : Proposez toujours des prix terminant par .90 ou .99.
5. **Restitution** : Présentez le plan d'action sous forme de tableau "Produit | Prix Actuel | Nouveau Prix | Justification".

## Après la Session

Enregistrez les nouveaux alias de produits confirmés dans le `BOND.md` pour améliorer les futurs calculs.
