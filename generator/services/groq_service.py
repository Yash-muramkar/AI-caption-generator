from groq import Groq
from django.conf import settings
import os


def generate_instagram_caption(raw_caption, ocr_text=""):


    try:

        client = Groq(api_key=settings.GROQ_API_KEY)

        # ✅ PROMPT FIRST (UNCHANGED)
        prompt = f"""
You are a top-tier Instagram caption strategist.

FIRST — understand the image deeply.

Classify the image into ONE category silently:

1. Institute / Educational
2. Marketing / Business / Branding
3. Person / Portrait
4. Other

Do NOT output the category.

----------------------------------

NOW FOLLOW THE WRITING DNA:

👉 If it is an INSTITUTE image:

Write like an industry leader.
Tone should feel educational, future-focused, and insightful.

Sound intelligent but not robotic.
Make the reader feel they are looking at the future.

Avoid cringe motivation.

Length: 4–5 lines.



👉 If it is a MARKETING / BRANDING image:

Write like a premium branding agency.

Confident.
Strategic.
Authority-driven.

Make businesses feel they NEED this.

Include light persuasion naturally.

You MAY include relevant hashtags.



👉 If it is a PERSON:

Write an aspirational caption.

Confident.
Growth-oriented.
Success-focused.

Make it feel powerful but natural.

Length: 3–5 lines.



----------------------------------

GLOBAL RULES:

❗ The caption must feel written specifically for THIS image.

If it can fit any random image → rewrite it.

Avoid generic AI phrases like:
"future", "unlock", "supercharge", "game changer".

No philosophical lectures.

Sound human.
Sound premium.

----------------------------------
Write like a professional social media manager with 10+ years of experience.

VISUAL SIGNALS:
{raw_caption}

TEXT IN IMAGE:
{ocr_text}
"""

        # ✅ Messages format (IMPORTANT — warna model confuse hota hai)
        messages = [
            {"role": "user", "content": prompt}
        ]

        try:
            model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

            chat = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
            )

        # ✅ Fallback model (agar Groq fir drama kare 😄)
        except Exception as model_error:

            print("⚠️ Primary model failed:", model_error)

            chat = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=messages,
                temperature=0.7,
                max_tokens=500,
            )

        result = chat.choices[0].message.content.strip()

        print("✅ GROQ SUCCESS")

        return result

    except Exception as e:

        print("❌ GROQ TOTAL FAILURE:", e)

        # User ko crash mat dikha
        return "⚠️ Caption generation is temporarily unavailable. Please try again."
