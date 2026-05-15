from fastapi import APIRouter, HTTPException
import google.generativeai as genai
import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/sirius", tags=["Sirius"])

# Configuration Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None

class ChatRequest(BaseModel):
    message: str

SIRIUS_PROMPT = """
Tu es Sirius, l'Expert SEO et Visibilité de la boutique 'La Muchette'.
Ta personnalité : Analytique, méthodique, direct et orienté résultats. Tu ne fais pas de blabla, tu vises la première page de Google.
Ta mission : Optimiser le SEO des fiches produits (Harry Potter, Disney, Déco), analyser les performances Search Console et conseiller sur la stratégie de contenu.
Ton ton : Professionnel, technique mais accessible, et toujours tourné vers l'action.
Si on te pose une question générale, réponds en tant qu'expert SEO de la boutique.
"""

@router.get("/status")
async def get_status():
    return {"status": "online", "agent": "Sirius", "capability": "SEO Specialist"}

@router.post("/chat")
async def chat_with_sirius(req: ChatRequest):
    if not model:
        raise HTTPException(status_code=500, detail="Gemini API Key non configurée sur le serveur.")
    
    try:
        chat = model.start_chat(history=[])
        full_prompt = f"{SIRIUS_PROMPT}\n\nUtilisateur: {req.message}"
        response = chat.send_message(full_prompt)
        return {"reply": response.text}
    except Exception as e:
        print(f"Erreur Gemini Sirius: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération : {str(e)}")
