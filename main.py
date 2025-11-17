
import os
import config
import time
from modules import epub_parser, tts_generator, image_generator, video_creator, youtube_uploader

def main():
    # 1. Parse the ePub file and get all chapters
    chapters = epub_parser.extract_chapters(config.EPUB_FILE_PATH)
    if not chapters:
        print("❌ No chapters found in the ePub file. Exiting.")
        return

    total_chapters = len(chapters)
    print(f"✅ Found {total_chapters} chapters in the book.")

    # --- INTERACTIVE CHAPTER SELECTION ---
    while True:
        prompt = f"➡️ Enter the starting chapter number to generate (1-{total_chapters}) [Default: {config.DEFAULT_START_CHAPTER}]: "
        start_chapter_input = input(prompt)
        if not start_chapter_input:
            start_chapter = config.DEFAULT_START_CHAPTER
            break
        try:
            start_chapter = int(start_chapter_input)
            if 1 <= start_chapter <= total_chapters:
                break
            else:
                print(f"❌ Invalid input. Please enter a number between 1 and {total_chapters}.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")

    while True:
        prompt = f"➡️ Enter how many individual chapter videos to generate [Default: {config.DEFAULT_CHAPTER_COUNT}]: "
        chapter_count_input = input(prompt)
        if not chapter_count_input:
            chapter_count = config.DEFAULT_CHAPTER_COUNT
            break
        try:
            chapter_count = int(chapter_count_input)
            if chapter_count > 0:
                break
            else:
                print("❌ Invalid input. Please enter a positive number.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")

    # 2. Calculate the exact chapter range to process
    start_index = start_chapter - 1
    end_index = min(start_index + chapter_count, total_chapters)
    chapters_to_process = chapters[start_index:end_index]
    actual_processed_count = len(chapters_to_process)
    final_chapter_number = start_chapter + actual_processed_count - 1

    if actual_processed_count == 0:
        print("❌ No chapters to process in the selected range. Exiting.")
        return

    print(f"\n✅ OK! Generating {actual_processed_count} individual videos: from chapter {start_chapter} to {final_chapter_number}.\n")

    # --- Main Processing Loop ---
    chapter_video_paths = []
    for i, (title, content) in enumerate(chapters_to_process, start=start_index):
        print(f"\n--- Processing Chapter {i+1}: {title} ---")
        
        # Introduce a delay to avoid rate-limiting
        print("  - Pausing for 5 seconds to avoid API rate-limiting...")
        time.sleep(5) 

        safe_title = f"chapter_{i+1}"
        audio_path = os.path.join(config.OUTPUT_DIR, "audio", f"{safe_title}.mp3")
        image_path = os.path.join(config.OUTPUT_DIR, "images", f"{safe_title}.png")
        video_path = os.path.join(config.OUTPUT_DIR, "videos", f"{safe_title}.mp4")

        try:
            # ... (Audio, Image, and Video creation for one chapter) ...
            print(f"  - Extracted chapter content length: {len(content)} characters")
            tts_generator.create_audio_file(content, audio_path)
            prompt = image_generator.generate_image_prompt(
                config.GCP_PROJECT_ID, config.GCP_LOCATION, config.GEMINI_API_KEY, content
            )
            image_generator.generate_image_with_vertex_ai(
                config.GCP_PROJECT_ID, config.GCP_LOCATION, prompt, image_path
            )
            if os.path.exists(audio_path) and os.path.exists(image_path):
                video_creator.create_chapter_video(image_path, audio_path, video_path, fps=config.VIDEO_FPS)
                chapter_video_paths.append(video_path)
            else:
                print("Skipping video creation for this chapter due to missing audio/image.")

        except Exception as e:
            print(f"🔥🔥🔥 An error occurred processing Chapter {i+1}: {e} 🔥🔥🔥")

    # --- MODIFICATION: REMOVED MERGING AND UPLOADING ---

    # The script's job is now done. It has created the individual chapter videos.
    # The batch_uploader.py script will handle the rest.
    
    if not chapter_video_paths:
        print("\n❌ No chapter videos were created.")
    else:
        print(f"\n🎉 Success! Created {len(chapter_video_paths)} individual chapter videos.")
        print("You can now run 'python batch_uploader.py' to merge and upload them in batches.")

if __name__ == "__main__":
    main()

