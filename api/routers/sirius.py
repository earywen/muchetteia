from fastapi import APIRouter, HTTPException
import google.generativeai as genai
import os
import pandas as pd
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/sirius", tags=["Sirius"])

# Configuration Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-3-flash-preview')
else:
    model = None

class ChatRequest(BaseModel):
    message: str

def get_seo_context():
    """Récupère un résumé des données SEO réelles pour le contexte de l'IA."""
    try:
        pages_path = "data/export SEO/Pages.csv"
        queries_path = "data/export SEO/Requêtes.csv"
        
        context = "DONNÉES RÉELLES DE LA MUCHETTE (SEO):\n"
        
        if os.path.exists(pages_path):
            df_pages = pd.read_csv(pages_path)
            top_pages = df_pages.head(10)[['Pages les plus populaires', 'Clics', 'Position']].to_string(index=False)
            context += f"\nTOP 10 PAGES:\n{top_pages}\n"
            
        if os.path.exists(queries_path):
            df_queries = pd.read_csv(queries_path)
            top_queries = df_queries.head(10)[['Requêtes les plus fréquentes', 'Clics', 'Position']].to_string(index=False)
            context += f"\nTOP 10 REQUÊTES GOOGLE:\n{top_queries}\n"
            
        return context
    except Exception as e:
        return f"Erreur lors de la lecture des données : {str(e)}"

SIRIUS_PROMPT = """
Tu es Sirius, l'Expert SEO de la boutique 'La Muchette'. 
IMPORTANT : Tu as accès aux données réelles de la boutique ci-dessous. Ne parle plus de Disney ou de généralités si ce n'est pas dans les données.
Ton but est d'analyser CES chiffres et de donner des conseils chirurgicaux pour améliorer le trafic.

Tes piliers actuels : Harry Potter, Minalima, Le Seigneur des Anneaux, Papeterie et Artisanat.
Cible prioritaire : Monter en page 1 sur 'boutique harry potter' (actuellement en page 2).

Données actuelles à utiliser pour tes réponses :
{seo_data}
"""

@router.post("/chat")
async def chat_with_sirius(req: ChatRequest):
    if not model:
        raise HTTPException(status_code=500, detail="Gemini API Key non configurée.")
    
    seo_data = get_seo_context()
    full_system_prompt = SIRIUS_PROMPT.format(seo_data=seo_data)
    
    try:
        chat = model.start_chat(history=[])
        # On injecte le prompt système mis à jour avec les vraies datas
        response = chat.send_message(f"{full_system_prompt}\n\nUtilisateur: {req.message}")
        return {"reply": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
