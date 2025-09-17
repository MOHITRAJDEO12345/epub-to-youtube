import os
import config
from modules import video_creator, youtube_uploader

def batch_merge_and_upload():
    """
    Finds existing chapter videos and merges/uploads them in batches.
    """
    video_dir = os.path.join(config.OUTPUT_DIR, "videos")
    
    if not os.path.isdir(video_dir):
        print(f"❌ Error: Video directory not found at '{video_dir}'.")
        print("Please run the main script first to generate chapter videos.")
        return

    # --- 1. Find and Sort All Existing Chapter Videos ---
    try:
        # Get all files starting with 'chapter_' and ending with '.mp4'
        all_chapter_files = [f for f in os.listdir(video_dir) if f.startswith('chapter_') and f.endswith('.mp4')]
        
        # Sort the files numerically based on the chapter number in the filename
        # This is crucial to ensure chapter_10.mp4 comes after chapter_9.mp4
        all_chapter_files.sort(key=lambda f: int(f.split('_')[1].split('.')[0]))
        
        if not all_chapter_files:
            print(f"❌ No pre-made chapter videos found in '{video_dir}'.")
            return
            
        highest_chapter = int(all_chapter_files[-1].split('_')[1].split('.')[0])
        print(f"✅ Found {len(all_chapter_files)} existing chapter videos (up to Chapter {highest_chapter}).")

    except (IndexError, ValueError):
        print("❌ Error: Could not parse chapter numbers from video filenames.")
        print("Ensure your video files are named correctly (e.g., 'chapter_1.mp4').")
        return

    # --- 2. Get User Input for Batching ---
    while True:
        try:
            start_chapter = int(input(f"➡️ Enter the starting chapter number to begin batching from [Default: 1]: ") or "1")
            if 1 <= start_chapter <= highest_chapter:
                break
            else:
                print(f"❌ Invalid input. Please enter a number between 1 and {highest_chapter}.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")

    while True:
        try:
            total_chapters_to_process = int(input(f"➡️ How many total chapters do you want to process from the start? [Default: 10]: ") or "10")
            if total_chapters_to_process > 0:
                break
            else:
                print("❌ Invalid input. Please enter a positive number.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")

    while True:
        try:
            batch_size = int(input(f"➡️ How many chapters per final video? (e.g., 5) [Default: 5]: ") or "5")
            if batch_size > 0:
                break
            else:
                print("❌ Invalid input. Please enter a positive number.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")

    # --- 3. Select the Files to Process Based on User Input ---
    start_index = start_chapter - 1
    end_index = start_index + total_chapters_to_process
    files_to_process = all_chapter_files[start_index:end_index]

    if not files_to_process:
        print("❌ No video files found in the specified range. Exiting.")
        return

    print(f"\n✅ OK! Preparing to process {len(files_to_process)} video files in batches of {batch_size}.")

    # --- 4. Loop Through the Files in Batches ---
    for i in range(0, len(files_to_process), batch_size):
        # Get the current chunk of files for this batch
        batch_files = files_to_process[i:i + batch_size]
        if not batch_files:
            continue

        # Determine the chapter numbers for this specific batch
        first_chap_num_in_batch = int(batch_files[0].split('_')[1].split('.')[0])
        last_chap_num_in_batch = int(batch_files[-1].split('_')[1].split('.')[0])
        
        print(f"\n--- Processing Batch: Chapters {first_chap_num_in_batch} to {last_chap_num_in_batch} ---")

        # Get the full, absolute paths for the video creator module
        batch_paths = [os.path.join(video_dir, f) for f in batch_files]

        # Define the output path and title for this merged video
        final_video_path = os.path.join(config.OUTPUT_DIR, f"final_video_{first_chap_num_in_batch}-{last_chap_num_in_batch}.mp4")
        final_video_title = config.VIDEO_TITLE_TEMPLATE.format(start=first_chap_num_in_batch, end=last_chap_num_in_batch)

        # A. Merge the videos for this batch
        if video_creator.merge_videos(batch_paths, final_video_path):
            # B. If merge is successful, upload to YouTube
            youtube_uploader.upload_to_youtube(
                video_path=final_video_path,
                secrets_file=config.YOUTUBE_SECRETS_FILE,
                title=final_video_title,
                description=config.VIDEO_DESCRIPTION,
                tags=config.VIDEO_TAGS,
                category_id=config.VIDEO_CATEGORY_ID,
                privacy_status=config.VIDEO_PRIVACY_STATUS
            )
        else:
            print(f"❌ Failed to merge batch for chapters {first_chap_num_in_batch}-{last_chap_num_in_batch}. Skipping upload.")

    print("\n🎉 All batches processed!")

if __name__ == "__main__":
    batch_merge_and_upload()