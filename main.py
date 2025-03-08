#pip install pillow 
#uvicorn main:app --reload
#py client.py
# http://127.0.0.1:8000/detect_objects/ <- POST works
# http://127.0.0.1:8000/image <- GET works
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import random
import uvicorn
import math


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
        negative_count = random.randint(80, 100)  # Many negatives
        strong_active_count = random.randint(10, 15)  # Similar to negatives
        moderate_active_count = random.randint(5, 10)  # Half the strong active
        mild_active_count = random.randint(0, 5)  # Few mild actives
        total_cells = negative_count + strong_active_count + moderate_active_count + mild_active_count
        total_positive_cells = strong_active_count + moderate_active_count + mild_active_count
        positive_cells_ratio = math.ceil(total_positive_cells / total_cells * 100)
        mild_ratio = math.ceil(mild_active_count/total_cells * 100),
        moderate_ratio = math.ceil(moderate_active_count/total_cells * 100),
        strong_ratio = math.ceil(strong_active_count/total_cells * 100),
        negative_ratio = math.ceil(negative_count/total_cells * 100),
        results = {
            "positive_cells": total_positive_cells,
            "positive_cell_ratio": positive_cells_ratio,
            "mild_positive": mild_active_count,
            "mild_ratio": mild_ratio[0],
            "moderate_positive": moderate_active_count,
            "moderate_ratio": moderate_ratio[0],
            "strong_positive": strong_active_count,
            "strong_ratio": strong_ratio[0],
            "negative_cells": negative_count,
            "negative_ratio": negative_ratio[0],
            "total_cells": total_cells,
        }
        # Return JSON with image URL
        return JSONResponse(content={"data": results, "image_url": "/image"})
    except Exception as e:
        # Log the error
        print(f"Error in detect_objects: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Added a debug route to test connectivity
@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/image")
async def get_image():
    """Returns the image from the local directory."""
    img_path = "image.png"
    return FileResponse(img_path, media_type="image/png")

if __name__ == "__main__":
    print("Starting FastAPI server at http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)