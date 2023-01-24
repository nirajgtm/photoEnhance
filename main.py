from fastapi import FastAPI, File, UploadFile, HTTPException
import replicate
import json
import uuid
from io import BytesIO
import logging

app = FastAPI()

# Get the model and version from Replicate
model = replicate.models.get("sczhou/codeformer")
version = model.versions.get("7de2ea26c616d5bf2245ad0d5e24f0ff9a6204578a5c876db53142edd9d2cd56")

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.StreamHandler()])
logger = logging.getLogger()

# Function to create the payload for Replicate
def getReplicateinputPayload(img_bytes: bytes):
    """
    Creates the payload for Replicate's predict function.
    This function takes in the image in bytes and creates a file-like object
    that can be passed to the predict function.
    """
    return {
    # Input image
    'image': BytesIO(img_bytes),

    # Balance the quality (lower number) and fidelity (higher number).
    # Range: 0 to 1
    'codeformer_fidelity': 0.5,

    # Enhance background image with Real-ESRGAN
    'background_enhance': True,

    # Upsample restored faces for high-resolution AI-created images
    'face_upsample': True,

    # The final upsampling scale of the image
    'upscale': 2,
    }

# Endpoint to process the image
@app.post("/process-image/")
async def process_image(file: UploadFile = File(...)):
    """
    Processes the image and returns the processed image.
    """
    try:
        # Read the image and create the payload
        img_bytes = await file.read()
        payload = getReplicateinputPayload(img_bytes)
        
        # Process the image using Replicate
        processed_image = version.predict(**payload)
        
        # Log the request and response
        logger.info(f"Processed image {file.filename} with Replicate")
        return {"processed_image": processed_image}
    except Exception as e:
        # Log the error and return a 500 error
        logger.exception(f"Error processing image {file.filename}")
        raise HTTPException(status_code=500, detail="Error processing image")
