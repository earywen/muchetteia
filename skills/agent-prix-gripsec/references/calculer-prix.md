---
name: Calculer Prix
code: CP
description: Calcul du prix de vente optimal à partir des coûts fournisseurs via script Python.
---

# Calculer Prix de Vente

## Ce que vous devez accomplir (Outcome)

Déterminer le prix public TTC optimal pour une nouvelle liste de produits fournisseurs (fichier Excel ou CSV), en appliquant rigoureusement les objectifs de marge et en couvrant l'ensemble des frais fixes.

## Intégration Mémoire & Scripts

1. Vous NE DEVEZ PAS faire les calculs arithmétiques vous-même.
2. Vous DEVEZ lancer le script : `python {skill-root}/scripts/calc_prices.py [chemin_vers_nouveau_csv] [chemin_vers_matrice_couts] [chemin_vers_grille_marge]`
3. Lisez la sortie JSON du script.

## Déroulement

1. **Préparation** : Vérifiez que vous possédez le fichier des prix d'achat du fournisseur.
2. **Exécution** : Lancez le script Python de calcul des prix.
3. **Validation** : Analysez les prix proposés par le script. Sont-ils cohérents psychologiquement (ex: se terminant par .90 ou .99) ?
4. **Restitution** : Fournissez le fichier de sortie ou le tableau des prix à l'utilisateur, avec un résumé global de la marge attendue sur ce nouveau lot.

## Après la Session

Mettez à jour le BOND pour noter que les prix de ce fournisseur ont été établis à cette date.
