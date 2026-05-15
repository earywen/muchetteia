---
name: Auditer Marges
code: AM
description: Analyse d'exports Hiboutik via script Python pour lever des alertes sur les marges faibles.
---

# Auditer Marges

## Ce que vous devez accomplir (Outcome)

Identifier instantanément, dans un fichier d'export de caisse (Hiboutik CSV), les produits dont la marge réelle est inférieure au seuil critique défini dans la Grille de Marge. 

## Intégration Mémoire & Scripts

1. Vous NE DEVEZ PAS calculer les marges vous-même.
2. Vous DEVEZ lancer le script : `python {skill-root}/scripts/calc_margins.py [chemin_vers_le_csv] [chemin_vers_matrice_couts] [chemin_vers_grille_marge]`
3. Lisez la sortie JSON du script.

## Déroulement

1. **Vérification** : Assurez-vous d'avoir les chemins des fichiers requis fournis par l'utilisateur ou trouvés dans `{agent.fixed_costs_matrix}` et `{agent.margin_targets}`.
2. **Exécution** : Lancez le script via l'outil de commande.
3. **Analyse** : À partir des résultats (produits en alerte), croisez avec la `{agent.no_discount_list}` pour vérifier s'il s'agit d'une référence protégée.
4. **Restitution** : Présentez à l'utilisateur un tableau clair des produits problématiques (en deçà de la marge cible) et proposez une action chiffrée pour chacun (ex: augmentation de X% du prix, ou changement de fournisseur).

## Après la Session

Aucune mise à jour de mémoire nécessaire, à moins qu'une décision globale sur le pricing ne soit prise avec l'utilisateur.
