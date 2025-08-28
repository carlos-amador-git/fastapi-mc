from fastapi import FastAPI

# Create an instance of the FastAPI class
app = FastAPI()

# Define a path operation decorator for the root URL ("/")
@app.get("/")
def read_root():
    # Define the function that will be executed when the URL is accessed
    return {"message": "Hello, Elvy!"}

# You can define other routes as well
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}