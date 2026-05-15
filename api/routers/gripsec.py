from fastapi import APIRouter, HTTPException
import google.generativeai as genai
import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/gripsec", tags=["Gripsec"])

# Configuration Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    # Utilisation du modèle 1.5 Flash (plus moderne et stable)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

class ChatRequest(BaseModel):
    message: str

GRIPSEC_PROMPT = """
Tu es Gripsec, le Garde-Manger et Expert Rentabilité de la boutique 'La Muchette'.
Ta personnalité : Obsédé par les chiffres, protecteur des marges, rigoureux et un peu austère. Pour toi, un centime est un centime.
Ta mission : Surveiller la rentabilité de la boutique, analyser les coefficients de marge (cible 2.5x), identifier les fuites de profit et optimiser les prix d'achat/revente.
Ton ton : Sec, précis, financier. Tu n'es pas là pour être aimable, mais pour que la boutique soit riche.
Si on te pose une question sur les prix ou les marges, réponds avec précision.
"""

@router.get("/status")
async def get_status():
    return {"status": "online", "agent": "Gripsec", "capability": "Profitability Expert"}

@router.post("/chat")
async def chat_with_gripsec(req: ChatRequest):
    if not model:
        raise HTTPException(status_code=500, detail="Gemini API Key non configurée sur le serveur.")
    
    try:
        chat = model.start_chat(history=[])
        full_prompt = f"{GRIPSEC_PROMPT}\n\nUtilisateur: {req.message}"
        response = chat.send_message(full_prompt)
        return {"reply": response.text}
    except Exception as e:
        print(f"Erreur Gemini Gripsec: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération : {str(e)}")
