# core/__init__.py
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from fastapi import HTTPException

load_dotenv()

# Configuración común
load_dotenv()
DATA_FOLDER = os.getenv("DATA_FOLDER")
DATABASE_URL = os.getenv("DATABASE_URL")
API_KEY = os.getenv("API_KEY")

# Re-exportar dependencias
__all__ = ["Session", "HTTPException", "DATA_FOLDER", "DATABASE_URL", "API_KEY"]