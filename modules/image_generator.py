import os
import base64
import vertexai
# Import the google.generative_ai library for text generation
import google.generativeai as genai 
from vertexai.preview.vision_models import ImageGenerationModel 

# Assuming your config.py has GEMINI_API_KEY and GCP_PROJECT_ID, GCP_LOCATION
# from config import GEMINI_API_KEY, GCP_PROJECT_ID, GCP_LOCATION

def generate_image_prompt(project_id, location, gemini_api_key, chapter_text):
    """
    Uses a Google AI Gemini model (via google-generative-ai SDK) to generate a descriptive image prompt.
    """
    print("✍️ Generating image prompt with Google AI Gemini...")
    try:
        # Configure the genai library with your API key
        genai.configure(api_key=gemini_api_key)
        
        # Using a model suitable for text generation with the genai SDK
        # 'gemini-1.5-flash' is often a good choice for speed and cost.
        model = genai.GenerativeModel("gemini-1.5-flash") 
        
        prompt_template = f"""
        Based on the following chapter text from a story, create a single, concise, and vivid text-to-image prompt 
        that captures the main scene, mood, and key elements. The prompt should be in English. 
        Do not include any introductory text like "Prompt:" or use quotation marks.

        Chapter Text:
        ---
        {chapter_text[:6000]} 
        ---
        """
        
        response = model.generate_content(prompt_template)
        image_prompt = response.text.strip()
        print(f"  - Generated Prompt: {image_prompt}")
        return image_prompt
    except Exception as e:
        print(f"❌ Error generating image prompt with Google AI: {e}")
        return "A fantasy book cover with an intriguing design."


def generate_image_with_vertex_ai(project_id, location, prompt, output_filename, aspect_ratio="16:9"):
    """
    Generates a real AI image using Vertex AI's Imagen model.
    """
    print(f"🎨 Generating real AI image with Vertex AI for: {os.path.basename(output_filename)}")
    try:
        vertexai.init(project=project_id, location=location)

        model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")
        
        print("  - Sending prompt to Imagen model...")
        response = model.generate_images(
            prompt=prompt,
            number_of_images=1,
            aspect_ratio=aspect_ratio,
        )
        
        print("  - Image received, saving...")
        
        # --- FIX ---
        # The _image_bytes attribute already contains the raw decoded image data.
        # We do not need to decode it again.
        image_bytes = response.images[0]._image_bytes
        # --- END OF FIX ---
        
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        
        with open(output_filename, "wb") as f:
            f.write(image_bytes)
            
        print(f"✅ AI image saved successfully to {output_filename}")
        return True
    except Exception as e:
        print(f"❌ Error generating image with Vertex AI: {e}")
        return False