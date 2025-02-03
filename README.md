# FastAPI Image Generation API

## Overview
This FastAPI application provides an interface for generating image prompts using Google's Gemini model and creating images using Hugging Face's Stable Diffusion API. The app includes an HTML frontend using Jinja2 templates.

## Features
- Accepts a book scene description and generates a detailed prompt using the Gemini API.
- Sends the generated prompt to Hugging Face's Stable Diffusion API to create an image.
- Serves static files and renders templates using Jinja2.
- Stores generated images in a static folder.

## Requirements
Ensure you have Python 3.8+ installed. Install the required dependencies using:

```bash
pip install -r requirements.txt
```

### Environment Variables
Create a `.env` file or set the following environment variables:
- `GEMINI_API_KEY`: Your Google Gemini API key.
- `GEMINI_MODEL_NAME`: (Optional) The Gemini model name (default: `gemini-1.5-flash`).
- `HUGGINGFACE_API_KEY`: Your Hugging Face API key.

## Running the Application
Start the FastAPI server with:

```bash
uvicorn main:app --reload
```

## API Endpoints
### `GET /`
- Returns the homepage with an HTML interface.

### `POST /generate-prompt`
- **Input:** `scene` (form data) - A book scene description.
- **Output:** JSON containing the generated text-to-image prompt.

### `POST /generate-image`
- **Input:** `prompt` (form data) - The generated prompt.
- **Output:** JSON with the image file path.

## File Structure
```
project_root/
│── main.py
│── requirements.txt
│── templates/
│   └── index.html
│── static/
│   └── images/
└── .env
```

## Notes
- Ensure API keys are valid before running the application.
- The generated images are stored in `static/images/`.

## License
This project is licensed under the MIT License.

