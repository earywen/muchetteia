# Capabilities

## Built-in

| Code | Name | Description | Source |
|------|------|-------------|--------|
| [AC] | Analyse Concurrentielle | Comparaison des prix avec les concurrents et ajustement du positionnement sans guerre des prix. | `./references/analyse-concurrentielle.md` |
| [AM] | Auditer Marges | Analyse d'exports Hiboutik via script Python pour lever des alertes sur les marges faibles. | `./references/auditer-marges.md` |
| [CP] | Calculer Prix | Calcul du prix de vente optimal à partir des coûts fournisseurs via script Python. | `./references/calculer-prix.md` |
| [SD] | Stratégies de Déstockage | Création de stratégies de déstockage intelligentes pour les produits dormants. | `./references/strategies-destockage.md` |

## Learned

_Capabilities added by the owner over time. Prompts live in `capabilities/`._

| Code | Name | Description | Source | Added |
|------|------|-------------|--------|-------|

## How to Add a Capability

Tell me "I want you to be able to do X" and we'll create it together.
I'll write the prompt, save it to `capabilities/`, and register it here.
Next session, I'll know how.
Load `./references/capability-authoring.md` for the full creation framework.

## Tools

Prefer crafting your own tools over depending on external ones. A script you wrote and saved is more reliable than an external API. Use the file system creatively.

### User-Provided Tools

_MCP servers, APIs, or services the owner has made available. Document them here._
