from fastapi import APIRouter, UploadFile, File, HTTPException
from utils.bmad_bridge import run_agent_script
from pydantic import BaseModel
import shutil
import os
import tempfile

router = APIRouter(prefix="/gripsec", tags=["Gripsec"])

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat_with_gripsec(req: ChatRequest):
    return {"reply": f"Gripsec a bien reçu votre demande : {req.message}. Je prépare les registres."}

@router.post("/analyze-margins")
async def analyze_margins(file: UploadFile = File(...)):
    """
    Endpoint pour envoyer un export Hiboutik et obtenir un audit de marge immédiat.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Seuls les fichiers CSV sont acceptés.")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        fixed_costs = os.path.join(root, "docs", "pricing", "fixed_costs_matrix.csv")
        targets = os.path.join(root, "docs", "pricing", "margin_targets.md")
        benchmarks = os.path.join(root, "docs", "pricing", "competitor_benchmarks.csv")
        
        result = run_agent_script(
            "agent-prix-gripsec", 
            "calc_margins.py", 
            [tmp_path, fixed_costs, targets, "--benchmarks", benchmarks]
        )
        return result
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
