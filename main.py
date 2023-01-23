from fastapi import FastAPI, File, UploadFile, HTTPException
import replicate
import json

import logging

logging.basicConfig(filename='app.log', filemode='w', level=logging.INFO)
logger = logging.getLogger()

model = replicate.models.get("sczhou/codeformer")
version = model.versions.get("7de2ea26c616d5bf2245ad0d5e24f0ff9a6204578a5c876db53142edd9d2cd56")


def getReplicateinputPayload(inputImage):
    # img_bytes = inputImage.read()
    return {
    # Input image
    'image': open("test image.jpg", "rb"),

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

app = FastAPI()


@app.post("/process-image/")
def process_image(file: UploadFile = File(...)):
    payload = getReplicateinputPayload(file)
    processed_image = version.predict(**payload)
    return {"processed_image":processed_image}
