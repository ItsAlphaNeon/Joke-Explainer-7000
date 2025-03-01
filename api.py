from flask import Flask, jsonify, request
from joke_explainer import explain_the_joke
import asyncio

app = Flask(__name__)

@app.route("/explain", methods=["POST"])
async def explain():
    try:
        data = request.get_json()
        url = data.get("url", "")
        print(f"Received URL: {url}")
        
        # Only allow YouTube URLs.
        if "youtube" not in url and "youtu.be" not in url:
            return jsonify({"error": "Only YouTube URLs are accepted."}), 400

        if "youtube" in url:
            # For youtube.com URLs, keep only the first query parameter
            if "?" in url:
                base, query = url.split("?", 1)
                if "&" in query:
                    query = query.split("&", 1)[0]
                url = f"{base}?{query}"
        elif "youtu.be" in url:
            # For youtu.be URLs, remove everything past the first "?"
            if "?" in url:
                url = url.split("?", 1)[0]
                
        print(f"Sanitized URL: {url}")
        explanation = await explain_the_joke(url)
        return jsonify({"joke": explanation})
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": "An error occurred while processing your request."}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)