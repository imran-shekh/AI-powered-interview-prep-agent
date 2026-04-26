from fastapi import APIRouter, UploadFile, File
from app.services.parser import extract_text_from_pdf

router = APIRouter()

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    text = extract_text_from_pdf(file.file)
    return {"text": text}