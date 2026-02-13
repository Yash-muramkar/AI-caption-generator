from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import cv2
import os

print("Loading BLIP model once...")

device = "cuda" if torch.cuda.is_available() else "cpu"

processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-large"
)

model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-large"
).to(device)

model.eval()


# -------------------------------------------------
# SMART IMAGE LOADER (IMAGE + VIDEO SUPPORT)
# -------------------------------------------------

def load_image(file_path):

    video_extensions = (".mp4", ".mov", ".avi", ".mkv")

    # ✅ VIDEO CASE
    if file_path.lower().endswith(video_extensions):

        cap = cv2.VideoCapture(file_path)

        success, frame = cap.read()
        cap.release()

        if not success:
            raise ValueError("Could not read frame from video.")

        # Convert BGR → RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert to PIL
        image = Image.fromarray(frame)

        return image

    # ✅ IMAGE CASE
    return Image.open(file_path).convert("RGB")


# -------------------------------------------------
# IMAGE RESIZE
# -------------------------------------------------

def resize_image(image, max_size=1024):
    image.thumbnail((max_size, max_size))
    return image


# -------------------------------------------------
# MULTI CAPTION GENERATOR
# -------------------------------------------------

def generate_blip_captions(image_path, num_captions=3):

    image = load_image(image_path)
    image = resize_image(image)

    inputs = processor(images=image, return_tensors="pt").to(device)

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_length=60,
            num_beams=5,
            num_return_sequences=num_captions,
            early_stopping=True
        )

    captions = [
        processor.decode(o, skip_special_tokens=True)
        for o in outputs
    ]

    return captions
