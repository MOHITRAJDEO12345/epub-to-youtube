# modules/tts_generator.py
from gtts import gTTS # type: ignore
import os

def create_audio_file(text, output_filename, language='en', slow=False, tld='com'):
    """
    Converts text to an MP3 audio file using Google's Text-to-Speech service.
    
    Customization Fields:
    - language (str): The language of the text (e.g., 'en', 'es').
    - slow (bool): If True, the audio will be read at a slower speed.
    - tld (str): The top-level domain for the Google host, which affects the accent.
                 Examples: 'com' (US), 'co.uk' (UK), 'com.au' (Australia), 'co.in' (India).
    """
    print(f"🔊 Generating audio with gTTS for: {os.path.basename(output_filename)}...")
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        
        # Create gTTS object with custom settings
        tts = gTTS(text=text, lang=language, slow=slow, tld=tld)
        
        # Save the audio file
        tts.save(output_filename)
        
        print(f"✅ Audio saved successfully.")
        return True
    except Exception as e:
        print(f"❌ Error generating audio with gTTS: {e}")
        return False



#     tld='com': Standard American accent (Default)

# tld='co.uk': British accent

# tld='com.au': Australian accent

# tld='ca': Canadian accent

# tld='co.in': Indian accent

# tld='ie': Irish accent