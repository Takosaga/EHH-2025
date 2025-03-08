#pip install fastapi
#pip install uvicorn
#uvicorn main:app --reload
from fastapi import FastAPI, Body 
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

# Configure CORS to allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, adjust as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/detect_objects/")
async def detect_objects():
    """
    Hardcoded object detection results.
    """
    # Hardcoded counts with the desired distribution
    negative_count = random.randint(50, 70)  # Many negatives
    strong_active_count = random.randint(40, 60) # Similar to negatives
    moderate_active_count = random.randint(20, 30) # Half the strong active
    mild_active_count = random.randint(5, 15)  # Few mild actives

    results = {
        "negative": negative_count,
        "strong_active": strong_active_count,
        "moderate_active": moderate_active_count,
        "mild_active": mild_active_count,
    }

    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)