import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = "AIzaSyDQARt8mvfip0pnFyIMg2EXxfWDt24fdRE" # Utilisation directe pour le test
genai.configure(api_key=api_key)

print("--- Liste des modèles disponibles ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Modèle: {m.name}")
except Exception as e:
    print(f"Erreur: {e}")
