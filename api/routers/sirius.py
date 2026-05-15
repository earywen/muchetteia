from fastapi import APIRouter
from utils.bmad_bridge import run_agent_script
from pydantic import BaseModel

router = APIRouter(prefix="/sirius", tags=["Sirius"])

class ChatRequest(BaseModel):
    message: str

@router.get("/status")
async def get_status():
    return {"status": "online", "agent": "Sirius", "capability": "SEO Specialist"}

@router.post("/chat")
async def chat_with_sirius(req: ChatRequest):
    # Ici, nous pourrions appeler un script Sirius qui interroge le LLM avec le contexte GSC
    # Pour l'instant, c'est un point d'ancrage pour l'intégration
    return {"reply": f"Sirius a reçu votre message : {req.message}. L'analyse sémantique est en cours."}
