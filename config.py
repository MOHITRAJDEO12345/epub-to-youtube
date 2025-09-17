import os

# --- Gemini API ---
GEMINI_API_KEY = "AIzaSyDC-unCg61JNhIQjhavSeJXwFiJHBgjYJY"  # Paste your key here

# --- File Paths ---
# Use os.path.join for cross-platform compatibility
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
EPUB_FILE_PATH = os.path.join(PROJECT_DIR, "Food_War...g_System.epub") # Change "my_book.epub" if needed
OUTPUT_DIR = os.path.join(PROJECT_DIR, "output")
YOUTUBE_SECRETS_FILE = os.path.join(PROJECT_DIR, "client_secrets.json")


TTS_AUDIO_SLOW = False # Set to True for slower speech, False for normal speed
TTS_AUDIO_TLD = 'com' # Top-level domain for accent (e.g., 'com', 'co.uk', 'co.in')

# --- Video Settings ---
# Set the range of chapters you want to process.
# These are based on the actual chapter numbers (starting from 1).

# These are now DEFAULTS for the interactive script.
# The script will ask you for these values when it runs.
DEFAULT_START_CHAPTER = 2    # Default chapter to start from.
DEFAULT_CHAPTER_COUNT = 100    # Default number of chapters to process in one video.

IMAGE_SIZE = (1920, 1080) # HD Resolution for YouTube
VIDEO_FPS = 24

# The title will now be generated automatically.
# Use {start} and {end} as placeholders for the chapter numbers.
VIDEO_TITLE_TEMPLATE = "Food Wars Audiobook - Chapters {start}-{end}"
VIDEO_DESCRIPTION = "An AI-generated audiobook experience. Created with Python, Google Gemini, and Vertex AI."
VIDEO_TAGS = ["audiobook", "ai", "gemini", "python", "story", "food wars"]
VIDEO_CATEGORY_ID = "24"  # "Entertainment" category.
VIDEO_PRIVACY_STATUS = "public" # Use "private" for testing, "public" for release

# --- YouTube Upload Settings (Additional Options) ---
VIDEO_DEFAULT_LANGUAGE = "en" # Default language of the video
VIDEO_MADE_FOR_KIDS = False   # Set to True if your video is made for kids
VIDEO_THUMBNAIL_PATH = None   # Optional: Path to a custom thumbnail image (e.g., "thumbnail.jpg")
                              # If None, YouTube will auto-generate one.

# --- Google Cloud & Vertex AI Settings ---
GCP_PROJECT_ID = "golden-context-472408-t3"  # <-- FILL THIS IN
GCP_LOCATION = "us-central1"           # <-- USE YOUR REGION, e.g., "us-central1"