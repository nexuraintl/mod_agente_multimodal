import os
from dotenv import load_dotenv

# Load environment variables from env_vars/.env
load_dotenv("env_vars/.env")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.diagnosis_controller import diagnosis_router

app = FastAPI(
    title="Nexura AI Multimodal Service",
    description="PServicio especializado en diagnóstico visual y diseño de bloques (bloqueEditor, bloqueLayout, bloqueDynamic).",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the diagnosis router
app.include_router(diagnosis_router)

@app.get("/health")
def health():
    return {
        "status": "UP"
    }


@app.get("/version")
def version():
    return {
        "service": "ms_ia_multimodalagent",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    # Read port from environment variable or use 8085 by default
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
    # cambio de puertopor pausa en el servicio

