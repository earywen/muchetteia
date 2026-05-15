from fastapi import APIRouter, UploadFile, File, HTTPException
from utils.bmad_bridge import run_agent_script
import shutil
import os
import tempfile

router = APIRouter(prefix="/gripsec", tags=["Gripsec"])

@router.post("/analyze-margins")
async def analyze_margins(file: UploadFile = File(...)):
    """
    Endpoint pour envoyer un export Hiboutik et obtenir un audit de marge immédiat.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Seuls les fichiers CSV sont acceptés.")
    
    # Création d'un fichier temporaire pour le script Python
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        # Chemins vers les fichiers de référence (à adapter selon votre structure)
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        fixed_costs = os.path.join(root, "docs", "pricing", "fixed_costs_matrix.csv")
        targets = os.path.join(root, "docs", "pricing", "margin_targets.md")
        benchmarks = os.path.join(root, "docs", "pricing", "competitor_benchmarks.csv")
        
        # Exécution du script Gripsec
        result = run_agent_script(
            "agent-prix-gripsec", 
            "calc_margins.py", 
            [tmp_path, fixed_costs, targets, "--benchmarks", benchmarks]
        )
        return result
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
