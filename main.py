#pip install fastapi
#pip install uvicorn
#uvicorn main:app --reload
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import random
import uvicorn

app = FastAPI()

# Configure CORS to allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, adjust as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint to verify server is running"""
    return {"message": "Server is running. Use POST /detect_objects/ to get detection results."}

@app.post("/detect_objects/")
async def detect_objects():
    """
    Hardcoded object detection results.
    """
    try:
        # Hardcoded counts with the desired distribution
        negative_count = random.randint(50, 70)  # Many negatives
        strong_active_count = random.randint(40, 60)  # Similar to negatives
        moderate_active_count = random.randint(20, 30)  # Half the strong active
        mild_active_count = random.randint(5, 15)  # Few mild actives
        
        results = {
            "negative": negative_count,
            "strong_active": strong_active_count,
            "moderate_active": moderate_active_count,
            "mild_active": mild_active_count,
        }
        
        return results
    except Exception as e:
        # Log the error
        print(f"Error in detect_objects: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Added a debug route to test connectivity
@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    print("Starting FastAPI server at http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)