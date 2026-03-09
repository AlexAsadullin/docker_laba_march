import os
import uuid
from datetime import datetime, timedelta

from fastapi import FastAPI, File, Query, UploadFile, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database import FileRecord, get_db, init_db
from pdf_convert import convert_to_pdf

TEMP_DIR = "/temp"
EXPIRY_HOURS = 24

ALLOWED_WORD = (".doc", ".docx")
ALLOWED_EXCEL = (".xls", ".xlsx")
ALLOWED_PPT = (".ppt", ".pptx")

app = FastAPI(title="Office-to-PDF converter")


@app.on_event("startup")
def startup():
    os.makedirs(TEMP_DIR, exist_ok=True)
    init_db()


def _save_and_convert(upload: UploadFile, allowed_exts: tuple[str, ...], db: Session) -> str:
    ext = os.path.splitext(upload.filename)[1].lower()
    if ext not in allowed_exts:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed: {', '.join(allowed_exts)}",
        )

    stem = upload.filename.rsplit(".", 1)[0]
    unique_name = f"{stem}_{uuid.uuid4().hex[:8]}"
    src_name = f"{unique_name}{ext}"
    src_path = os.path.join(TEMP_DIR, src_name)

    with open(src_path, "wb") as f:
        f.write(upload.file.read())

    expires_at = datetime.utcnow() + timedelta(hours=EXPIRY_HOURS)

    db.add(FileRecord(filename=src_name, extension=ext, expires_at=expires_at))

    pdf_path = convert_to_pdf(src_path)
    pdf_name = os.path.basename(pdf_path)

    db.add(FileRecord(filename=pdf_name, extension=".pdf", expires_at=expires_at))
    db.commit()

    return pdf_path


@app.post("/convert_word")
def convert_word(file: UploadFile = File(...), db: Session = Depends(get_db)):
    pdf_path = _save_and_convert(file, ALLOWED_WORD, db)
    return FileResponse(pdf_path, media_type="application/pdf", filename=os.path.basename(pdf_path))


@app.post("/convert_excel")
def convert_excel(file: UploadFile = File(...), db: Session = Depends(get_db)):
    pdf_path = _save_and_convert(file, ALLOWED_EXCEL, db)
    return FileResponse(pdf_path, media_type="application/pdf", filename=os.path.basename(pdf_path))


@app.post("/convert_powerpoint")
def convert_powerpoint(file: UploadFile = File(...), db: Session = Depends(get_db)):
    pdf_path = _save_and_convert(file, ALLOWED_PPT, db)
    return FileResponse(pdf_path, media_type="application/pdf", filename=os.path.basename(pdf_path))


@app.get("/restore")
def restore(filename: str = Query(...), db: Session = Depends(get_db)):
    record = db.query(FileRecord).filter(FileRecord.filename == filename).first()
    if not record:
        raise HTTPException(status_code=404, detail="File not found in database")

    if datetime.utcnow() > record.expires_at:
        raise HTTPException(status_code=410, detail="File has expired")

    file_path = os.path.join(TEMP_DIR, filename)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")

    return FileResponse(file_path, filename=filename)
