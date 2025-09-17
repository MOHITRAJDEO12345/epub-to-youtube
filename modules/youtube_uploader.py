# modules/youtube_uploader.py
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# This scope allows for uploading and managing your YouTube videos.
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

def get_authenticated_service(client_secrets_file):
    """
    Authenticates with the YouTube API and returns a service object.
    Handles token storage and refresh.
    """
    creds = None
    token_pickle_file = 'token.pickle'

    if os.path.exists(token_pickle_file):
        with open(token_pickle_file, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_pickle_file, 'wb') as token:
            pickle.dump(creds, token)
            
    return build(API_SERVICE_NAME, API_VERSION, credentials=creds)

def upload_to_youtube(video_path, secrets_file, title, description, category_id, tags, privacy_status,
                      default_language=None, made_for_kids=False, thumbnail_path=None):
    """
    Uploads a video file to YouTube with extended options.
    """
    print(f"🚀 Uploading '{title}' to YouTube...")
    try:
        youtube = get_authenticated_service(secrets_file)
        
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": category_id,
                # New snippet options
                "defaultLanguage": default_language if default_language else "en" 
            },
            "status": {
                "privacyStatus": privacy_status,
                # New status option
                "madeForKids": made_for_kids 
            }
        }

        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
        
        request = youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=media
        )
        
        response = request.execute()
        video_id = response['id']
        print(f"✅ Video uploaded successfully! Video ID: {video_id}")

        # Upload thumbnail if provided
        if thumbnail_path and os.path.exists(thumbnail_path):
            print(f"🖼️ Uploading thumbnail from {thumbnail_path}...")
            thumbnail_media = MediaFileUpload(thumbnail_path)
            youtube.thumbnails().set(
                videoId=video_id,
                media_body=thumbnail_media
            ).execute()
            print("✅ Thumbnail uploaded successfully.")
        
        return video_id
    except Exception as e:
        print(f"❌ Failed to upload video: {e}")
        return None