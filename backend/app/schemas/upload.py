from typing import Optional, Any, List

from pydantic import BaseModel, EmailStr, ValidationError, validator
from fastapi import HTTPException
import datetime


class UploadText(BaseModel):
    text: str
    user_name: str
