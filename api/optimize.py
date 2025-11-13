from groq import Groq
import json
import os

# -----------------------------
# 1️⃣ Load Groq API Key
# -----------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY environment variable is missing.")

client = Groq(api_key=GROQ_API_KEY)

# -----------------------------
# 2️⃣ Serverless handler
# -----------------------------
def handler(request):
    try:
        # ---------------------
        # Health check (GET)
        # ---------------------
        if request.method == "GET":
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"message": "✅ Depop AI Bot (Groq) is running!"})
            }

        # ---------------------
        # Optimize listing (POST)
        # ---------------------
        if request.method == "POST":
            data = json.loads(request.body)
            title = data.get("title", "")
            brand = data.get("brand", "")
            size = data.get("size", "")
            color = data.get("color", "")

            if not title or not brand:
                return {
                    "statusCode": 400,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"success": False, "error": "Title and brand are required."})
                }

            # ---------------------
            # Prompt for optimization
            # ---------------------
            prompt = (
                "You are a Depop SEO and streetwear optimization expert.\n"
                "Create a search‑optimized product title under 60 characters and 10 top-performing tags.\n\n"
                f"Brand: {brand}\nTitle: {title}\nSize: {size}\nColor: {color}\n\n"
                "Respond only in this format:\nTitle: <optimized title>\nTags: tag1, tag2, ..."
            )

            # ---------------------
            # Chat call to Groq
            # ---------------------
            result = client.chat.completions.create(
                model="llama-3.1-8b",  # Make sure this model exists on your plan
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

        # ---------------------
        # Method not allowed
        # ---------------------
        return {
            "statusCode": 405,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"success": False, "error": "Method not allowed"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"success": False, "error": str(e)})
        }
