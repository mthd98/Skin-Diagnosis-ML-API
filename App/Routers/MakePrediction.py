from fastapi import Depends, HTTPException, APIRouter, File, UploadFile,BackgroundTasks

from pathlib import Path
import os 
import time
from  Utils.Model import Model
from Utils.Preprocessing import PreprocessImages
from datetime import datetime
from Security.CheckAPIKey import check_api_key










AIP_PREDICT_ROUTE = os.environ.get('ML_PREDICT_ROUTE', '/predict')

BASE_DIR = Path(__file__).resolve().parent

ml_router = APIRouter(tags=['Make Prediction'])

model = Model()
preprocessor = PreprocessImages()


@ml_router.get("/health")
async def health_check(api_key_info: dict = Depends(check_api_key)):
    """Health check endpoint.

    Returns:
        dict: A dictionary indicating the service is running.
    """
    return {"status": "ok"}


@ml_router.post("/predict")
async def make_prediction(file: UploadFile = File(...), api_key_info: dict = Depends(check_api_key)):
    """Processes an uploaded image and returns a prediction.

    Args:
        file (UploadFile): The uploaded image file.

    Returns:
        dict: A dictionary containing the diagnosis result, 
              time taken for prediction, and timestamp.

    Raises:
        HTTPException: If the file is empty or invalid.
    """
    if api_key_info is None:
        raise HTTPException(status_code=400, detail="Invalid API Key.")
    
    start_time = time.time()

    try:
        # Read file bytes
        file_bytes = await file.read()

        if not file_bytes:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        # Preprocess the image
        data = preprocessor.preprocess_image_batch([file_bytes], (300, 300))

        # Ensure data is valid
        if data is None:
            raise HTTPException(status_code=400, detail="Error in image preprocessing.")

        # Perform prediction
        result = model.make_prediction(data)

        if result is None:
            raise HTTPException(status_code=500, detail="Prediction model failed.")

        end_time = time.time()
        return {
            "diagnosis": result,
            "time_taken": end_time - start_time,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
