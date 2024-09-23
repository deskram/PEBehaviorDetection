from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from handlers.pe_scanner import analyze_pe_file
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI(docs_url=None)

app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/pe_scan/")
async def pe_scan(file: UploadFile = File(...)):
    if not re.match(r'^.*\.(exe|dll)$', file.filename):
        raise HTTPException(status_code=400, detail="File must be of type .exe or .dll")

    try:
        results = analyze_pe_file(file.file)
        return JSONResponse(content={"results": results})
    except Exception as e:
        return JSONResponse(content={"error": f"Error processing PE file: {str(e)}"}, status_code=500)

@app.get("/")
async def home():
    version = "1.0.0"
    return {"message": f"Welcome to the PE Scanner API, version {version}"}
