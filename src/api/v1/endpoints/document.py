"""Document Endpoint."""

import ast

from fastapi import APIRouter, File, HTTPException, UploadFile

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload")
async def analyze_source_code(files: list[UploadFile] = File(...)):
    """Upload Documents and analyze Source Code."""
    python_files = []
    skipped = []
    invalid_python_files = []

    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    for file in files:
        file_name = file.filename

        if not file_name:
            skipped.append("<No filename>")
            continue

        if not file_name.lower().endswith(".py"):
            skipped.append(file_name)
            continue

        content = await file.read()

        try:
            source_code = content.decode("utf-8")
        except UnicodeDecodeError:
            skipped.append(file_name)
            continue

        try:
            tree = ast.parse(source_code)
        except SyntaxError:
            invalid_python_files.append(file_name)
            continue

        python_files.append({"filename": file_name, "source": source_code, "ast": tree})

    return {
        "Python_files_count": len(python_files),
        "skipped": skipped,
        "Invalid Python files": invalid_python_files,
    }
