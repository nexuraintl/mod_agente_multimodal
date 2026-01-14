import os
from dotenv import load_dotenv

# Load environment variables from env_vars/.env
load_dotenv("env_vars/.env")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.diagnosis_controller import diagnosis_router

app = FastAPI(
    title="AI Diagnosis Service",
    description="Pure AI diagnosis service for design tickets. Consumed by agents_mod.",
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


if __name__ == "__main__":
    import uvicorn
    # Read port from environment variable or use 8085 by default
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
