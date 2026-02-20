from os import getenv
import hmac
import hashlib
from typing import Optional
from aiohttp.web_request import Request
from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError

from .db_init import AsyncSessionLocal
from .db_models import IssuedToken
import os
import time

def make_hmac(token: str) -> str:
    return hmac.new(getenv("SECRET_KEY", "").encode('utf-8'), token.encode('utf-8'), hashlib.sha256).hexdigest()
