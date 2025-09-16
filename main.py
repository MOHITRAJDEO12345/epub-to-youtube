import os
import config
from modules import epub_parser, tts_generator, image_generator, video_creator, youtube_uploader

def main():
    # 1. Parse the ePub file
    chapters = epub_parser.extract_chapters(config.EPUB_FILE_PATH)
    if not chapters:
        print("No chapters found. Exiting.")
        return

    chapter_video_paths = []
    
    # Use a slice to process only the desired number of chapters
    chapters_to_process = chapters[:config.CHAPTERS_TO_PROCESS]

    # Loop through each chapter to create its components
    for i, (title, content) in enumerate(chapters_to_process):
        print(f"\n--- Processing Chapter {i+1}: {title} ---")
        
        # Define file paths for this chapter
        safe_title = f"chapter_{i+1}" # A filename-safe name
        audio_path = os.path.join(config.OUTPUT_DIR, "audio", f"{safe_title}.mp3")
        image_path = os.path.join(config.OUTPUT_DIR, "images", f"{safe_title}.png")
        video_path = os.path.join(config.OUTPUT_DIR, "videos", f"{safe_title}.mp4")

        try:
        # ADD THIS LINE TO CHECK THE CHAPTER'S LENGTH
            print(f"  - Extracted chapter content length: {len(content)} characters")

            # 2. Generate Audio
            # We can cycle through voices by using the chapter index
            voice_choice = i % 4 
            # This is the correct call for the new gTTS function
            tts_generator.create_audio_file(content, audio_path)

            # 3. Generate Image Prompt and then the Image
            prompt = image_generator.generate_image_prompt(config.GEMINI_API_KEY, content)
            image_generator.create_placeholder_image(prompt, image_path, size=config.IMAGE_SIZE)

            # 4. Create Chapter Video
            if os.path.exists(audio_path) and os.path.exists(image_path):
                video_creator.create_chapter_video(image_path, audio_path, video_path, fps=config.VIDEO_FPS)
                chapter_video_paths.append(video_path)
            else:
                print("Skipping video creation for this chapter due to missing audio/image.")

        except Exception as e:
            print(f"🔥🔥🔥 An error occurred processing Chapter {i+1}: {e} 🔥🔥🔥")
            print("Moving to the next chapter.")

    # 5. Merge all chapter videos into one
    if not chapter_video_paths:
        print("No chapter videos were created. Exiting.")
        return
        
    final_video_path = os.path.join(config.OUTPUT_DIR, "final_video.mp4")
    video_creator.merge_videos(chapter_video_paths, final_video_path)

    # 6. Upload to YouTube
    if os.path.exists(final_video_path):
        youtube_uploader.upload_to_youtube(
            video_path=final_video_path,
            secrets_file=config.YOUTUBE_SECRETS_FILE,
            title=config.VIDEO_TITLE,
            description=config.VIDEO_DESCRIPTION,
            tags=config.VIDEO_TAGS,
            category_id=config.VIDEO_CATEGORY_ID,
            privacy_status=config.VIDEO_PRIVACY_STATUS
        )

if __name__ == "__main__":
    main()