from fastapi import FastAPI, Depends
from routers import sirius, gripsec
from auth import get_api_key

app = FastAPI(
    title="La Muchette Agents API",
    description="Interface locale pour Sirius (SEO) et Gripsec (Prix)",
    version="1.0.0"
)

# Inclusion des routers avec protection globale par API Key
app.include_router(sirius.router, dependencies=[Depends(get_api_key)])
app.include_router(gripsec.router, dependencies=[Depends(get_api_key)])

@app.get("/")
async def root():
    return {"message": "Nexus La Muchette - Système Opérationnel", "version": "1.0.0"}
