from groq import Groq
from django.conf import settings


def generate_instagram_caption(raw_caption, ocr_text=""):

    try:

        client = Groq(api_key=settings.GROQ_API_KEY)

        # ✅ PROMPT FIRST (MOST IMPORTANT)
        prompt = f"""
You are an elite social media copywriter for a premium EdTech brand.

Write a HIGH-CONVERSION Instagram caption.

⚠️ IMPORTANT:
- DO NOT describe the poster
- DO NOT explain anything
- DO NOT say "this poster shows"
- DO NOT analyze

Write like a top marketing expert.

Tone:
- Premium
- Confident
- Career-focused
- Future-oriented
- Professional but human

Rules:
- 4 to 6 lines ONLY
- No emojis
- No hashtags
- No bullet points
- No numbering

GOAL:
Make the reader feel that upgrading their skills is necessary for career growth.

VISUAL UNDERSTANDING:
{raw_caption}

POSTER TEXT:
{ocr_text}
"""

        chat = client.chat.completions.create(

            model="llama-3.1-8b-instant",  # ⭐ VERY IMPORTANT

            messages=[
                {"role": "user", "content": prompt}
            ],

            temperature=0.6,
            max_tokens=200,
        )

        result = chat.choices[0].message.content.strip()

        print("✅ GROQ SUCCESS")

        return result


    except Exception as e:
     raise Exception(f"GROQ FAILED: {e}")
