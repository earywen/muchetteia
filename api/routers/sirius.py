from fastapi import APIRouter
from utils.bmad_bridge import run_agent_script

router = APIRouter(prefix="/sirius", tags=["Sirius"])

@router.get("/status")
async def get_status():
    return {"status": "online", "agent": "Sirius", "capability": "SEO Specialist"}

@router.post("/chat")
async def chat_with_sirius(message: str):
    # Ici, nous pourrions appeler un script Sirius qui interroge le LLM avec le contexte GSC
    # Pour l'instant, c'est un placeholder pour l'intégration BMad
    return {"reply": f"Sirius a reçu votre message : {message}. L'analyse sémantique est en cours."}
