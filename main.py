from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn

# 2. Create a FastAPI app instance
app = FastAPI()

# 3. Define an endpoint for the root URL ("/") to serve the HTML file
@app.get("/")
async def read_root():
    """
    This endpoint serves the main HTML page for the frontend.
    """
    return FileResponse('index.html')

# 4. Define an API endpoint to provide data to the frontend
@app.get("/api/message")
async def get_message():
    """
    This endpoint returns a simple JSON message.
    The frontend will call this to get data.
    """
    return {"message": "Hello from the FastAPI backend! 👋"}

# 5. Add a main block to run the app with uvicorn
#    This allows you to run the script directly with `python main.py`
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)