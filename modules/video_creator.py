from moviepy import ImageClip, AudioFileClip, concatenate_videoclips, VideoFileClip
import os
import multiprocessing

def create_chapter_video(image_path, audio_path, output_path, fps=24):
    """
    Creates a video clip from a single image and an audio file.
    """
    print(f"🎬 Creating video for: {os.path.basename(output_path)}...")
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        if not os.path.exists(audio_path) or not os.path.exists(image_path):
            print("❌ Audio or image file not found. Skipping video creation.")
            return False

        audio_clip = AudioFileClip(audio_path)
        image_clip = ImageClip(image_path, duration=audio_clip.duration)
        
        image_clip.audio = audio_clip
        
        # --- OPTIMIZATION ADDED ---
        # Get number of available CPU cores, use all but one for safety
        num_threads = multiprocessing.cpu_count() - 1 if multiprocessing.cpu_count() > 1 else 1
        
        image_clip.write_videofile(
            output_path, 
            fps=fps, 
            codec='libx264', 
            temp_audiofile='temp-audio.mp3', 
            remove_temp=True,
            threads=num_threads,
            preset='superfast'
        )
        # --- END OF OPTIMIZATION ---
        
        print("✅ Chapter video created.")
        return True
    except Exception as e:
        print(f"❌ Error creating chapter video: {e}")
        return False

def merge_videos(video_files, final_output_path):
    """
    Merges a list of video files into a single video.
    """
    print(f"🎞️ Merging {len(video_files)} clips into final video...")
    try:
        clips = [VideoFileClip(file) for file in video_files if os.path.exists(file)]
        
        if not clips:
            print("❌ No valid video clips found to merge.")
            return False
            
        final_clip = concatenate_videoclips(clips, method="compose")

        # --- OPTIMIZATION ADDED ---
        num_threads = multiprocessing.cpu_count() - 1 if multiprocessing.cpu_count() > 1 else 1
        
        final_clip.write_videofile(
            final_output_path, 
            fps=24, 
            codec='libx264',
            threads=num_threads,
            preset='superfast'
        )
        # --- END OF OPTIMIZATION ---

        print(f"✅ Final video saved to {final_output_path}")
        return True
    except Exception as e:
        print(f"❌ Error merging videos: {e}")
        return False