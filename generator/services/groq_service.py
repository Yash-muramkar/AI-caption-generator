from groq import Groq
from django.conf import settings
import os
from .ollama_service import generate_with_ollama


def generate_instagram_caption(raw_caption, ocr_text=""):


    try:

        client = Groq(api_key=settings.GROQ_API_KEY)

        # ✅ PROMPT FIRST (UNCHANGED)
        prompt = f"""
You are an elite Instagram caption strategist.

Your job is to write captions that feel human, specific to the image, emotionally aligned, and ready to post without editing.

--------------------------------------------------

FIRST — deeply understand the image.

Silently classify it into ONE category:

1. Institute / Educational
2. Marketing / Business / Branding
3. Person / Portrait
4. Lifestyle / Casual / Travel / Emotional
5. Other

Do NOT output the category.

Before writing, detect the emotional energy of the image and let that guide your tone.

Observe — do NOT assume.

--------------------------------------------------

WRITING DNA:

👉 If it is an INSTITUTE image:

Write like a credible industry leader.

Tone should feel educational, insightful, and trustworthy — never overly corporate.

Sound intelligent but natural.
Avoid buzzwords and exaggerated motivation.

Make the reader feel confidence and clarity.

Length: 4–5 lines.



👉 If it is a MARKETING / BRANDING image:

Write like a premium branding expert.

Confident.
Strategic.
Authority-driven.

Make businesses feel they NEED this — without sounding salesy.

Use persuasion subtly and intelligently.

You MAY include relevant hashtags only if they feel organic.



👉 If it is a PERSON:

Match the person’s vibe — not a default personality.

If casual → sound natural.  
If stylish → sound confident.  
If emotional → sound warm.  
If professional → sound aspirational.  

Do NOT default to corporate language.

Make it feel real, personal, and authentic — never manufactured.

Length: 3–5 lines.



👉 If it is LIFESTYLE / CASUAL / TRAVEL / EMOTIONAL:

Write like a real human sharing a moment.

Prioritize relatability over professionalism.

Sound effortless and natural.

Avoid business or corporate language completely.

Make the caption feel alive.



--------------------------------------------------

GLOBAL RULES:

The caption MUST strictly reflect what is visible in the image.

Never invent context that is not visible.

Do NOT assume profession, industry, success, or business intent unless clearly shown.

Match the emotional energy of the image BEFORE choosing the writing style.

If the image feels personal, candid, fun, or lifestyle-focused — prioritize relatability over professionalism.

❗ The caption must feel written specifically for THIS image.
If it can fit any random image → rewrite it.

Avoid generic AI phrases like:
"future", "unlock", "supercharge", "game changer".

No philosophical lectures.
No motivational fluff.

Sound human.
Sound premium — but NEVER robotic.



--------------------------------------------------

EMOJI INTELLIGENCE:

Use emojis only when they naturally fit the tone.

Do NOT overuse emojis.
Limit emojis to 1–3 per caption unless the emotional tone genuinely calls for more.

For professional captions → keep emojis minimal and refined.  
For lifestyle or personal captions → emojis may enhance emotion.

Prefer placing emojis at the end of sentences rather than inside them.

Emojis must feel intentional — never decorative.



--------------------------------------------------

STYLE CONTROL:

Write like an elite social media writer who adapts tone perfectly to the image.
Start captions with a thought, emotion, insight, or strong statement — NOT a visual description.

Be corporate ONLY when the image demands it.
Otherwise sound natural and human.

Prioritize clarity, emotional resonance, and authenticity.



--------------------------------------------------

VISUAL SIGNALS:
{raw_caption}

TEXT IN IMAGE:
{ocr_text}



--------------------------------------------------

FINAL TASK:
Write the caption now.



OUTPUT RULES (CRITICAL):

Return ONLY the final caption.

Do NOT explain anything.
Do NOT describe the image.
Do NOT mention the category.
Do NOT justify your writing.
Do NOT add notes or summaries.
Do NOT describe the image literally.
Avoid starting the caption by explaining what is visible.

Assume the viewer can already see the image — your role is to add meaning, emotion, or perspective.

Transform the scene into a feeling or story rather than a visual narration.
Only include hashtags when they genuinely add value. Otherwise, skip them.

Your response must contain ONLY the caption text.
Nothing else.
HUMANIZATION RULE:

The caption must feel like it was written by a real person — not an AI.

Avoid overly polished or perfectly structured sentences.

Allow slight natural imperfections in phrasing.

Write the way people actually speak and post on Instagram.

Prioritize authenticity over perfection.

"""
        

        # ✅ Messages format (IMPORTANT — warna model confuse hota hai)
        messages = [
            {"role": "user", "content": prompt}
        ]
# 🔥 TRY LOCAL FIRST
        local_result = generate_with_ollama(prompt)

        if local_result and len(local_result) > 40:
            print("✅ OLLAMA SUCCESS")
            return local_result

        print("⚠️ Falling back to GROQ...")

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
