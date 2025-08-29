from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import os
import tempfile
import subprocess
from pathlib import Path
import shutil

app = FastAPI(title="Word to PDF Converter")

# Create temp directory if it doesn't exist
TEMP_DIR = Path("temp")
TEMP_DIR.mkdir(exist_ok=True)

@app.post("/convert-word-to-pdf")
async def convert_word_to_pdf(file: UploadFile = File(...)):
    """
    Convert uploaded Word document to PDF and return the PDF file.
    Supports .doc, .docx formats.
    """
    
    # Validate file type
    if not file.filename.lower().endswith(('.doc', '.docx')):
        raise HTTPException(
            status_code=400, 
            detail="Only .doc and .docx files are supported"
        )
    
    # Generate unique filenames
    input_filename = f"{file.filename}"
    output_filename = f"output_{Path(file.filename).stem}.pdf"
    
    input_path = TEMP_DIR / input_filename
    output_path = TEMP_DIR / output_filename
    
    try:
        # Save uploaded file
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Convert using LibreOffice (headless mode)
        result = subprocess.run([
            "soffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", str(TEMP_DIR),
            str(input_path)
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail=f"Conversion failed: {result.stderr}"
            )
        
        # Check if output file was created
        expected_output = TEMP_DIR / f"{Path(file.filename).stem}.pdf"
        if not expected_output.exists():
            raise HTTPException(
                status_code=500,
                detail="PDF file was not generated successfully"
            )
        
        # Return the PDF file
        print("Generated PDF path:", expected_output)
        return FileResponse(
            path=expected_output,
            filename="temp/input_template.pdf",
            media_type="application/pdf",
            background=cleanup_files([input_path, expected_output])
        )
    
   
        
    except subprocess.TimeoutExpired:
        # Clean up files
        cleanup_files([input_path, output_path])
        raise HTTPException(
            status_code=500,
            detail="Conversion timed out. File might be too large or corrupted."
        )
    except Exception as e:
        # Clean up files
        cleanup_files([input_path, output_path])
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during conversion: {str(e)}"
        )

def cleanup_files(file_paths):
    """Background task to clean up temporary files after response"""
    def cleanup():
        for file_path in file_paths:
            try:
                if Path(file_path).exists():
                    os.remove(file_path)
            except Exception:
                pass  # Ignore cleanup errors
    return cleanup

@app.get("/")
async def root():
    return {"message": "Word to PDF Converter API", "endpoint": "/convert-word-to-pdf"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)