import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFont
import os

def generate_image_prompt(api_key, chapter_text):
    """
    Uses Gemini to generate a descriptive image prompt from chapter text.
    """
    print("✍️ Generating image prompt with Gemini...")
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # We ask Gemini to summarize the scene for an artist
        prompt_template = f"""
        Based on the following chapter text, create a single, concise, and vivid text-to-image prompt 
        that captures the main scene, mood, and key elements. The prompt should be in English and suitable 
        for an AI image generator like Midjourney or DALL-E. Do not include any introductory text, just the prompt itself.

        Chapter Text:
        ---
        {chapter_text[:2000]}
        ---
        """
        
        response = model.generate_content(prompt_template)
        image_prompt = response.text.strip().replace('"', '')
        print(f"  - Generated Prompt: {image_prompt}")
        return image_prompt
    except Exception as e:
        print(f"❌ Error generating image prompt: {e}")
        return "A book cover with an intriguing design." # Fallback prompt

def create_placeholder_image(text, output_filename, size=(1920, 1080)):
    """
    This is a placeholder that creates an image with text.
    This version is updated for Pillow 10.0.0+
    """
    print(f"🖼️ Creating placeholder image: {os.path.basename(output_filename)}")
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    
    img = Image.new('RGB', size, color = (20, 20, 40)) # Dark blue background
    d = ImageDraw.Draw(img)
    
    try:
        # Use a default font, consider placing a .ttf file in your project for consistency
        font = ImageFont.truetype("arial.ttf", 60)
    except IOError:
        font = ImageFont.load_default()

    # Simple text wrapping
    lines = []
    words = text.split()
    current_line = ""
    for word in words:
        if len(current_line + " " + word) < 40:
            current_line += " " + word
        else:
            lines.append(current_line.strip())
            current_line = word
    lines.append(current_line.strip())

    # Draw text
    text_y = (size[1] - len(lines) * 70) // 2
    for line in lines:
        # --- THIS IS THE CORRECTED PART ---
        # The old d.textsize() is replaced with d.textbbox()
        bbox = d.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        # --- END OF CORRECTION ---

        text_x = (size[0] - text_width) // 2
        d.text((text_x, text_y), line, fill=(255, 255, 255), font=font)
        text_y += 70 # Move down for the next line

    img.save(output_filename)
    print("✅ Placeholder image saved.")