# main.py
import os
from fastapi import FastAPI, Response
from docxtpl import DocxTemplate
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

origins = [
    "http://localhost:3000",  # Your frontend application
    "https://your-frontend-domain.com",
    "http://127.0.0.1:3000",
    "https://gf7ef8efb74e614-ys0k48631ld4v415.adb.us-phoenix-1.oraclecloudapps.com",
]

# Create a simple POST endpoint
@app.post("/generate-pdf")
async def generate_pdf(data: dict):
    try:
        # 1. Fill the Word template
        tpl = DocxTemplate("template.docx")
        context = data # Pass the data from the request directly as context
        tpl.render(context)

        # Save the filled document to a BytesIO object (in memory)
        filled_docx = BytesIO()
        tpl.save(filled_docx)
        filled_docx.seek(0)

        # 2. Convert DOCX to PDF using an external API
        # Replace with a real API key for production
        api_key = os.environ.get("CONVERTAPI_SECRET")
        if not api_key:
            return {"error": "API key not found. Please set CONVERTAPI_SECRET environment variable."}, 500

        # Use ConvertAPI or a similar service
        response = requests.post(
            "https://v2.convertapi.com/docx/to/pdf",
            data={ "Secret": api_key },
            files={ "file": filled_docx }
        )

        if response.status_code != 200:
            return {"error": f"Conversion failed with status code {response.status_code}"}, 500

        # 3. Return the PDF file as a response
        return Response(content=response.content, media_type="application/pdf",
                        headers={"Content-Disposition": "attachment; filename=generated.pdf"})

    except Exception as e:
        return {"error": str(e)}, 500

@app.get("/")
def read_root():
    return {"message": "API is running. Use the /generate-pdf endpoint."}

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# # List of allowed origins
# origins = [
#     "http://localhost:3000",  # Your frontend application
#     "https://your-frontend-domain.com",
#     "http://127.0.0.1:3000",
#     "https://gf7ef8efb74e614-ys0k48631ld4v415.adb.us-phoenix-1.oraclecloudapps.com",
# ]

# # Add the middleware to your application
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,  # Specifies which origins are allowed to make requests
#     allow_credentials=True, # Allows cookies to be included in requests
#     allow_methods=["GET", "POST", "PUT", "DELETE"], # Defines allowed HTTP methods
#     allow_headers=["*"], # Allows all headers
# )

# # Your existing path operations...
# @app.get("/")
# def read_root():
#     return {"message": "Hello, World!"}

# @app.post("/items/")
# def create_item():
#     return {"message": "Item created!"}