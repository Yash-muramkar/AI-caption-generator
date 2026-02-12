import pytesseract
from PIL import Image

# Windows path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)

        return text.strip()

    except Exception as e:
        print("OCR ERROR:", e)
        return ""
