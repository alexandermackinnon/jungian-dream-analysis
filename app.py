from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Securely load API key

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    image_url = None
    if request.method == "POST":
        prompt = request.form["prompt"]
        try:
            # Generate dream interpretation using GPT-4o
            response = openai.chat.completions.create(
                model="gpt-4o",  
                messages=[
                    {"role": "system", "content": "You are an insightful Jungian dream analyst. Provide symbolic interpretations based on Carl Jung's theories, referencing archetypes, the collective unconscious, and individuation."}, 
                    {"role": "user", "content": f"I had this dream: {prompt}. What does it mean?"}
                ],
                temperature=0.8,
                max_tokens=150
            )
            result = response.choices[0].message.content

            # Construct image prompt based on dream analysis
            image_prompt = f"A surreal and symbolic dreamscape illustrating the dream: '{prompt}', interpreted through Jungian archetypes such as the Shadow, the Anima/Animus, or the Wise Old Man. The scene reflects the journey of individuation and the hidden depths of the unconscious."  
            
            # Generate image using DALL·E
            image_response = openai.OpenAI().images.generate(
                model="dall-e-2",
                prompt=image_prompt,
                size="512x512",
                quality="standard",
                n=1,
            )
            image_url = image_response.data[0].url
        except Exception as e:
            result = f"Error: {str(e)}"
    return render_template("index.html", result=result, image_url=image_url)

if __name__ == "__main__":
    app.run(debug=True)  # Run locally for testing
