from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# List of allowed origins
origins = [
    "http://localhost:3000",  # Your frontend application
    "https://your-frontend-domain.com",
    "http://127.0.0.1:3000",
    "https://gf7ef8efb74e614-ys0k48631ld4v415.adb.us-phoenix-1.oraclecloudapps.com",
]

# Add the middleware to your application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Specifies which origins are allowed to make requests
    allow_credentials=True, # Allows cookies to be included in requests
    allow_methods=["GET", "POST", "PUT", "DELETE"], # Defines allowed HTTP methods
    allow_headers=["*"], # Allows all headers
)

# Your existing path operations...
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/items/")
def create_item():
    return {"message": "Item created!"}