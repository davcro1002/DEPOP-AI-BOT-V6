from groq import Groq
import json
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

def handler(request):
    try:
        if request.method == "GET":
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"message": "✅ Depop AI Bot (Groq) is running!"})
            }

        if request.method == "POST":
            if client is None:
                return {
                    "statusCode": 500,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"success": False, "error": "Missing GROQ_API_KEY"})
                }

            data = json.loads(request.body)
            title = data.get("title", "")
            brand = data.get("brand", "")
            size = data.get("size", "")
            color = data.get("color", "")

            prompt = (
                "You are a Depop SEO and streetwear optimization expert.\n"
                "Create a search‑optimized product title under 60 characters and 10 top-performing tags.\n\n"
                f"Brand: {brand}\nTitle: {title}\nSize: {size}\nColor: {color}\n\n"
                "Respond only in this format:\nTitle: <optimized title>\nTags: tag1, tag2, ..."
            )

            result = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You optimize Depop listings."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )

            optimized_text = result.choices[0].message.content

            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"success": True, "optimized_output": optimized_text})
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"success": False, "error": str(e)})
        }
