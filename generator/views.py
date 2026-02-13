from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import random

from django.http import JsonResponse

from .blip_model import generate_blip_captions
from .ocr_utils import extract_text
from .models import GeneratedCaption
from .services.groq_service import generate_instagram_caption


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
# AJAX CAPTION GENERATOR
# ==================================================

def generate_caption(request):

    if request.method == "POST" and request.FILES.get("media"):

        file = request.FILES["media"]

        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        path = fs.path(filename)

        blip_captions = generate_blip_captions(path)
        raw_caption = "\n".join(blip_captions)

        ocr_text = extract_text(path)

        final_input = f"""
        VISUAL:
        {raw_caption}

        TEXT:
        {ocr_text}
        """

        caption = generate_instagram_caption(final_input)
        hashtags = generate_hashtags()

        return JsonResponse({
            "caption": caption,
            "hashtags": hashtags
        })

    return JsonResponse({"error": "Invalid request"})


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
# MAIN PAGE VIEW
# ==================================================

def upload(request):
    return render(request, "upload.html")
