from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="WAHID Platform API",
    description="API principale de la plateforme WAHID - Module Transport",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "🚀 WAHID Platform API - Bienvenue!",
        "version": "1.0.0",
        "module": "Transport",
        "status": "active",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "WAHID Backend"}

@app.get("/api/v1/info")
async def api_info():
    return {
        "name": "WAHID Platform",
        "version": "1.0.0",
        "modules": ["Transport", "CRM", "Marketplace"],
        "phase": "Development"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
