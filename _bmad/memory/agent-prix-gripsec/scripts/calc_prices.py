# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Gripsec - Retail Price Calculator Script
Calculates optimal retail prices based on margin targets, market caps, and prudence rules.
"""

import sys
import json
import argparse
import csv
import difflib
import os

def load_csv_data(filepath, delimiter=';', encoding='cp1252'):
    data = []
    if not os.path.exists(filepath):
        return data
    try:
        with open(filepath, mode='r', encoding=encoding) as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            for row in reader:
                data.append(row)
    except Exception as e:
        print(f"Error loading {filepath}: {e}", file=sys.stderr)
    return data

def get_fuzzy_match(name, benchmarks, threshold=0.7):
    best_match = None
    highest_score = 0
    for bench in benchmarks:
        score = difflib.SequenceMatcher(None, name.lower(), bench.get('Nom', '').lower()).ratio()
        if score > highest_score:
            highest_score = score
            best_match = bench
    return best_match, highest_score

def smooth_price(price):
    """Rounds price to .90 or .99 for retail aesthetics."""
    base = int(price)
    if price - base < 0.45:
        return base - 0.10 # e.g. 9.90
    else:
        return base + 0.99 # e.g. 10.99

def main():
    parser = argparse.ArgumentParser(description="Calcule les prix publics optimaux.")
    parser.add_argument("supplier_file", help="Fichier fournisseur (CSV)")
    parser.add_argument("fixed_costs_csv", help="Matrice des coûts fixes")
    parser.add_argument("margin_targets_md", help="Grille de marge")
    parser.add_argument("--benchmarks", help="Benchmarks concurrents", default=None)
    parser.add_argument("--max_increase", type=float, default=0.20, help="Augmentation max autorisée (20%)")
    
    args = parser.parse_args()
    
    try:
        new_items = load_csv_data(args.supplier_file)
        benchmarks = load_csv_data(args.benchmarks) if args.benchmarks else []
        
        recommendations = []
        
        for item in new_items:
            try:
                # Normalisation des noms de colonnes (souvent variables selon les fournisseurs)
                name = item.get('Libellé', item.get('Title', item.get('Nom', 'Inconnu')))
                cost_price_ht = float(str(item.get("Prix d'achat HT", item.get("Cost", 0))).replace(',', '.'))
                current_price = float(str(item.get("Prix de vente", 0)).replace(',', '.'))
                
                if cost_price_ht <= 0: continue
                
                # Logic Target
                target_coeff = 2.5
                raw_target_price = cost_price_ht * target_coeff
                
                # Apply Market Cap
                bench, score = get_fuzzy_match(name, benchmarks)
                market_max = float(bench.get('Prix Max Marché', 0).replace(',', '.')) if bench else None
                
                final_price = raw_target_price
                reason = "Objectif Coeff 2.5"
                
                if market_max and final_price > market_max:
                    final_price = market_max
                    reason = f"Plafonnement au Prix Max Marché ({market_max})"
                
                # Apply Prudence Rule (Max increase)
                if current_price > 0:
                    max_allowed = current_price * (1 + args.max_increase)
                    if final_price > max_allowed:
                        final_price = max_allowed
                        reason = f"Limitation de hausse (+{int(args.max_increase*100)}% max)"

                # Smoothing
                final_price = smooth_price(final_price)
                
                recommendations.append({
                    "name": name,
                    "cost_price_ht": cost_price_ht,
                    "recommended_price_ttc": final_price,
                    "projected_coeff": round(final_price / cost_price_ht, 2),
                    "reason": reason,
                    "match_confidence": round(score * 100, 1) if bench else 0
                })
            except Exception:
                continue

        result = {
            "status": "success",
            "processed": len(recommendations),
            "recommendations": recommendations
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
