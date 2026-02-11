import os
import uuid
from aiohttp.web import HTTPBadRequest
import aiofiles
from PIL import Image, UnidentifiedImageError
import logging

def secure_filename(filename: str) -> str:
    _, ext = os.path.splitext(filename)
    ext = ext.lower()
    if ext not in (".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp"):
        ext = ".jpg"
    return f"{uuid.uuid4().hex}{ext}"

async def save_uploaded_image(content, filename, dest_dir):
    fname = filename or "upload"
    out_name = secure_filename(fname)
    out_path = os.path.join(dest_dir, out_name)

    # Сохраняем асинхронно
    async with aiofiles.open(out_path, "wb") as f:
        await f.write(content)

    # Проверка и получение размеров
    try:
        with Image.open(out_path) as im:
            im.verify()
        with Image.open(out_path) as im2:
            width, height = im2.size
    except (UnidentifiedImageError, OSError):
        try:
            os.remove(out_path)
        except Exception:
            pass
        raise HTTPBadRequest(text="Uploaded file is not a valid image")

    return out_name, width, height
