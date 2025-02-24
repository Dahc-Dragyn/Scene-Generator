from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os
import uuid
import google.generativeai as genai
import requests

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Configure Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL_NAME = os.environ.get("GEMINI_MODEL_NAME", "gemini-1.5-flash") # Make configurable
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(GEMINI_MODEL_NAME)

# Hugging Face API details
HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY")
STABLE_DIFFUSION_ENDPOINT = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3.5-large"

# Static image folder
STATIC_IMG_FOLDER = Path("static/images")
STATIC_IMG_FOLDER.mkdir(parents=True, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate-prompt")
async def generate_prompt(request: Request, scene: str = Form(...)):
    print(f"Length of received scene: {len(scene)} characters")
    max_length = 4001 # Set your desired limit
    if len(scene)>max_length:
        raise HTTPException(status_code=413,
        detail=f"Scene description is too long. Maximum length is {max_length} characters.")
    print(f"Received scene for prompt generation: {scene}")  # Debugging print
        
    
    try:
        # Enhanced Prompt Engineering for Gemini
        gemini_prompt = f"""
        You are a visual prompt generator for a text-to-image model. 
        Analyze the following book scene description and create a detailed text prompt that will be used to generate a realistic imag using 100-200 words.

        **Book Scene Description:**
        ```
        {scene}
        ```

        **Instructions:**

        1.  **Focus on Visual Details:** Extract all visual elements from the description: characters, objects, environment, setting, lighting, colors, actions, and overall mood.
        2.  **Be Specific and Descriptive:** Use concrete and precise language. Instead of "a man," say "a tall, thin man with a weathered face and a long, gray beard." Instead of "a dark room," say "a dimly lit room with dark wooden walls, illuminated by a single flickering candle."
        3. **Prioritize Accuracy:** The generated image should accurately reflect the details provided in the book scene description, even if it means being less creative.
        4. **Consider Composition:** If the scene implies a particular composition (e.g., "the character is in the foreground"), include that in the prompt.
        5. **Format for Text-to-Image:** Structure the output as a single, concise paragraph that describes the desired image in a way that a text-to-image model can understand.
        6. **Optional:** If the scene's description has any of the below, please add to the prompt.
            * **Art Style:** If the book or scene suggests a particular art style (e.g., "a watercolor painting," "a futuristic cyberpunk scene"), include that in the prompt.
            * **Aspect Ratio:** if the scene implies an aspect ratio (e.g., "a wide panoramic view"), add that to the prompt.
        7. **Content Restrictions (IMPORTANT): **DO NOT** include any nudity, suggestive content, or inappropriate elements. 

        **Example:**
        If you receive the description: "A young woman sits by a window, reading a book. Sunlight streams in, illuminating dust motes in the air."
        Your prompt could be: "A young woman with long, dark hair, wearing a simple blue dress, sits on a cushioned window seat in a cozy room. She is intently reading a large, leather-bound book. Warm sunlight streams in from a large, multi-paned window on the right side of the frame, illuminating motes of dust dancing in the air. The room is decorated with bookshelves and a comfortable armchair. The mood is peaceful and serene. The aspect ratio is 4:3. The style is photorealistic."

        **Output:**
        Generate a single paragraph 100 - 200 words that describes the scene in detail, suitable for a text-to-image model.
        """

        response = model.generate_content(gemini_prompt)
        prompt = response.text
        print(f"Generated prompt: {prompt}")  # Debugging print
        return JSONResponse({"prompt": prompt})

    except Exception as e:
        print(f"Error generating prompt: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate prompt")

@app.post("/generate-image")
async def generate_image(prompt: str = Form(...)):
    print(f"Received prompt for image generation: {prompt}") # Debugging print
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    try:
        response = requests.post(
            STABLE_DIFFUSION_ENDPOINT,
            headers=headers,
            json={"inputs": prompt, "options": {"wait_for_model": True}},
        )
        response.raise_for_status()

        image_bytes = response.content
        image_filename = f"image_{uuid.uuid4()}.png"
        image_path = STATIC_IMG_FOLDER / image_filename

        with open(image_path, "wb") as f:
            f.write(image_bytes)

        print(f"Image saved to: {image_path}") # Debugging print
        return JSONResponse({"image_path": f"static/images/{image_filename}"})
    except requests.exceptions.RequestException as e:
        print(f"Error during image generation: {e}")
        error_message = "Image generation failed."
        if e.response:
            try:
                error_data = e.response.json()
                error_message = error_data.get("error", error_message)
            except ValueError:
                pass  # Not a JSON response
        return JSONResponse(content={"error": error_message}, status_code=500)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))  # Use PORT from env variable
    uvicorn.run(app, host="0.0.0.0", port=port)
