from flask import Flask, request, jsonify
from flask_cors import CORS
import groq
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = groq.Groq(api_key=GROQ_API_KEY)

PROMPT = """Act as a professional Clinical Nutritionist and Pharmacologist. Analyze the provided image and follow these specific instructions based on the content:

### CASE 1: MEDICINE PACKET
If the image is a medicine packet/strip:
If the image contains medicine/supplements (e.g., Calcium tablets, Multivitamins):
1. **Active Ingredient Identification:** Identify the main components (e.g., Calcium Carbonate, Iron, etc.).
2. **Natural Food Alternatives/Boosters:** For the identified nutrients, suggest a list of 5-7 natural foods rich in that specific nutrient (e.g., if it's Calcium, suggest ragi, milk, almonds, spinach).
3. **Absorption Guide:** Suggest "Pairing Foods" that help absorb this medicine better (e.g., Vitamin C for Iron, Vitamin D for Calcium).
4. **Side Effects of Misuse:** Explain the risk of 'Overdose' (Toxicity) vs 'Underdose' (Deficiency) of these specific nutrients.

### CASE 2: FOOD PLATE / MEAL
If the image is a meal or specific food items:
1. **Macro Breakdown:** Estimate the Protein, Carbohydrates, Fats, and Fiber content.
2. **The "Good & Bad":** Identify which items are highly beneficial and which might be "harmful" or "less nutritious" based on common health goals.
3. **Limitations & Portions:** Provide the ideal serving size.
4. **Deficiency vs. Excess:** - Explain what happens if this food is eaten in **Excess** (e.g., toxicity, weight gain, specific diseases).
   - Explain what happens if there is a **Deficiency** of these specific nutrients (e.g., fatigue, muscle loss).

### GENERAL TONE
- Provide the output in a clear, professional, and structured format using tables and bullet points. 
- Always include a medical disclaimer.
"""

def analyze(image):

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role":"user",
                "content":[
                    {
                        "type":"image_url",
                        "image_url":{
                            "url":f"data:image/jpeg;base64,{image}"
                        }
                    },
                    {"type":"text","text":PROMPT}
                ]
            }
        ],
        max_tokens=1000
    )

    return response.choices[0].message.content


@app.route("/analyze/food", methods=["POST"])
def analyze_food():
    data = request.json
    image = data["image"]

    result = analyze(image)

    return jsonify({"result": result})


@app.route("/analyze/medicine", methods=["POST"])
def analyze_med():
    data = request.json
    image = data["image"]

    result = analyze(image)

    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(port=5000, debug=True)