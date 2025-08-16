from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv('.env.local')
from app.api.endpoints import router as api_router
app = FastAPI()
#CORS Config
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


# Load environment variables from .env/.env.local
load_dotenv()


