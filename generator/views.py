from fileinput import filename
from importlib.resources import path
from optparse import Option
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from PIL import Image
import cv2
import random
import uuid
from .blip_model import processor, model, device
from .ocr_utils import extract_text
import caption_generator.settings as settings
from .models import GeneratedCaption
from .services.groq_service import generate_instagram_caption

from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

raw_caption = "a man working on laptop"

 
# ==================================================
# LOAD BLIP MODEL (ONLY ONCE)
# ==================================================

device = "cuda" if torch.cuda.is_available() else "cpu"

processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-large"
)

model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-large"
)




# ==================================================
# SMART HASHTAG GENERATOR
# ==================================================

def generate_hashtags():
    base_tags = [
        "technology", "learning", "upskilling", "career",
        "future", "ai", "programming", "growth",
        "developers", "techlife", "digital",
        "skills", "education", "innovation"
    ]
     
    tags = random.sample(base_tags, 7)
    return " ".join(f"#{tag}" for tag in tags)


# ==================================================
# HISTORY VIEW
# ==================================================

def caption_history(request):
    captions = GeneratedCaption.objects.order_by("-created_at")[:10]

    return render(
        request,
        "history.html",
        {"captions": captions}
    )


# ==================================================
# MAIN UPLOAD VIEW
# ==================================================

def upload(request):

    caption = None
    hashtags = None

    if request.method == "POST" and request.FILES.get("media"):

        file = request.FILES["media"]

        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        path = fs.path(filename)

        image = Image.open(path).convert("RGB")

        inputs = processor(image, return_tensors="pt")
        output = model.generate(**inputs)

        raw_caption = processor.decode(
            output[0],
            skip_special_tokens=True
        )

        ocr_text = extract_text(path)

        final_input = f"""
        VISUAL:
        {raw_caption}

        POSTER TEXT:
        {ocr_text}
        """

        caption = generate_instagram_caption(final_input)
        hashtags = generate_hashtags()

        GeneratedCaption.objects.create(
        media=filename,
        raw_caption=raw_caption,
        final_caption=caption,   # ✅ FIXED
        hashtags=hashtags
    )


        return render(
            request,
            "upload.html",
            {
                "caption": caption,
                "hashtags": hashtags
            }
        )
 
    return render(request, "upload.html")
