from dotenv import load_dotenv

# Cargar variables de entorno desde env_vars/.env
load_dotenv("env_vars/.env")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.agent_controller import agent_router

app = FastAPI(
    title="Znuny Agent API",
    description="FastAPI application for Znuny webhook processing with AI diagnostics",
    version="2.0.0"
)

# CORS middleware (opcional, ajustar según necesidades)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar el router
app.include_router(agent_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
