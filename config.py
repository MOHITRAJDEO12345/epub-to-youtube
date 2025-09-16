import os

# --- Gemini API ---
GEMINI_API_KEY = "AIzaSyDC-unCg61JNhIQjhavSeJXwFiJHBgjYJY"  # Paste your key here

# --- File Paths ---
# Use os.path.join for cross-platform compatibility
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
EPUB_FILE_PATH = os.path.join(PROJECT_DIR, "IllegalFileName.epub") # Change "my_book.epub" if needed
OUTPUT_DIR = os.path.join(PROJECT_DIR, "output")
YOUTUBE_SECRETS_FILE = os.path.join(PROJECT_DIR, "client_secrets.json")

# --- Video Settings ---
CHAPTERS_TO_PROCESS = 31 # How many chapters to include in the final video
IMAGE_SIZE = (1920, 1080) # HD Resolution for YouTube
VIDEO_FPS = 24

# --- YouTube Upload Settings ---
VIDEO_TITLE = "My Awesome Audiobook - Chapters 1-30"
VIDEO_DESCRIPTION = "An AI-generated audiobook experience. Created with Python and Gemini."
VIDEO_TAGS = ["audiobook", "ai", "gemini", "python", "story"]
VIDEO_CATEGORY_ID = "24"  # "Entertainment" category. Find others online.
VIDEO_PRIVACY_STATUS = "private" # Use "private" for testing, "public" for release