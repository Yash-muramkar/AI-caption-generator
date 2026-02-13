from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch


print("🔥 Loading BLIP model... (only once)")

# Device auto-detect (GPU future ready)
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load processor & model globally (SINGLETON)
processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-large"
)

model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-large"
).to(device)

model.eval()   # VERY IMPORTANT → disables dropout



# ---------------------------------------------------
# IMAGE OPTIMIZATION
# ---------------------------------------------------

def resize_image(image: Image.Image, max_size=1024):
    """
    Resize large images before sending to BLIP.
    Saves RAM + speeds up inference massively.
    """
    image.thumbnail((max_size, max_size))
    return image



# ---------------------------------------------------
# MAIN BLIP ENGINE
# ---------------------------------------------------

def generate_blip_captions(image_path, num_captions=3):
    """
    Generates MULTIPLE captions for better scene understanding.

    Returns:
        List[str]
    """

    try:
        # Open image safely
        image = Image.open(image_path).convert("RGB")

        # Resize (performance booster)
        image = resize_image(image)

        # Process image
        inputs = processor(images=image, return_tensors="pt").to(device)

        # Inference without gradients (LOW MEMORY)
        with torch.no_grad():

            output = model.generate(
                **inputs,
                max_length=60,
                num_beams=5,                # better reasoning
                num_return_sequences=num_captions,
                early_stopping=True
            )

        captions = [
            processor.decode(o, skip_special_tokens=True)
            for o in output
        ]

        return captions


    except Exception as e:
        print("❌ BLIP ERROR:", str(e))
        return ["A visually appealing moment captured beautifully."]
 