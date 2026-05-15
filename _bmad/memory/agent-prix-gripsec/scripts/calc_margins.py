# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Gripsec - Margin Calculator Script
Reads a Hiboutik CSV and calculates real margins taking fixed costs and competitor prices into account.
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

def get_fuzzy_match(name, benchmarks, threshold=0.6):
    best_match = None
    highest_score = 0
    for bench in benchmarks:
        score = difflib.SequenceMatcher(None, name.lower(), bench.get('Nom', '').lower()).ratio()
        if score > highest_score:
            highest_score = score
            best_match = bench
    
    if highest_score >= threshold:
        return best_match, highest_score
    return None, 0

def main():
    parser = argparse.ArgumentParser(description="Calcule les marges réelles à partir d'un export Hiboutik.")
    parser.add_argument("inventory_csv", help="Chemin vers le CSV d'export produits (Hiboutik)")
    parser.add_argument("fixed_costs_csv", help="Chemin vers le CSV de la matrice des coûts fixes")
    parser.add_argument("margin_targets_md", help="Chemin vers le fichier MD de la grille de marge")
    parser.add_argument("--benchmarks", help="Chemin vers le CSV des benchmarks concurrents", default=None)
    
    args = parser.parse_args()
    
    try:
        inventory = load_csv_data(args.inventory_csv)
        fixed_costs = load_csv_data(args.fixed_costs_csv, delimiter=',')
        benchmarks = load_csv_data(args.benchmarks) if args.benchmarks else []
        
        # Calculate variable fixed costs from matrix
        var_cost_pct = 0
        fixed_cost_sum = 0
        for cost in fixed_costs:
            if cost['type'] == 'percentage':
                var_cost_pct += float(cost['value'])
            elif cost['type'] == 'fixed':
                fixed_cost_sum += float(cost['value'])

        alerts = []
        processed_count = 0
        
        for item in inventory:
            try:
                name = item.get('Libellé', 'Inconnu')
                sku = item.get('Code-barres', 'N/A')
                category = item.get('Catégorie', 'Default')
                
                # Conversion des prix
                purchase_price_ht = float(item.get("Prix d'achat HT", 0).replace(',', '.'))
                selling_price_ttc = float(item.get("Prix de vente", 0).replace(',', '.'))
                tax_rate = float(item.get("Taxe", 0).replace(',', '.'))
                
                if purchase_price_ht <= 0:
                    continue
                
                selling_price_ht = selling_price_ttc / (1 + tax_rate)
                current_coeff = selling_price_ttc / purchase_price_ht
                
                # Real margin after transaction fees and fixed costs
                real_margin_ht = selling_price_ht * (1 - var_cost_pct) - purchase_price_ht - (fixed_cost_sum / 10) # Prorated fixed cost
                
                # Matching concurrent
                bench, score = get_fuzzy_match(name, benchmarks)
                market_avg = float(bench.get('Prix Moyen Marché', 0).replace(',', '.')) if bench else None
                market_max = float(bench.get('Prix Max Marché', 0).replace(',', '.')) if bench else None
                
                # Target check (Default to 2.5)
                target_coeff = 2.5 
                # (Simple category matching logic here or load from MD in future version)
                if "Friandises" in category: target_coeff = 2.2
                if "Baguettes" in category: target_coeff = 2.8
                
                if current_coeff < target_coeff or (market_avg and selling_price_ttc < market_avg * 0.9):
                    alerts.append({
                        "name": name,
                        "sku": sku,
                        "category": category,
                        "current_price": selling_price_ttc,
                        "current_coeff": round(current_coeff, 2),
                        "target_coeff": target_coeff,
                        "real_margin_ht": round(real_margin_ht, 2),
                        "market_avg": market_avg,
                        "market_max": market_max,
                        "match_confidence": round(score * 100, 1) if bench else 0,
                        "status": "Warning" if current_coeff < target_coeff else "Opportunity"
                    })
                
                processed_count += 1
            except (ValueError, TypeError):
                continue

        result = {
            "status": "success",
            "summary": {
                "scanned_items": processed_count,
                "alerts_found": len(alerts)
            },
            "alerts": alerts[:50] # Limit output size
        }
        
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        import traceback
        error_result = {
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()
