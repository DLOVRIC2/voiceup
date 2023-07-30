import os
from dotenv import load_dotenv
from typing import List, Optional
import shutil
from mutagen.mp3 import MP3
from moviepy import editor
from PIL import Image
from moviepy.editor import TextClip, CompositeVideoClip, ImageClip
from moviepy.editor import *

from moviepy.video.io.VideoFileClip import VideoFileClip
import glob



# Load the environment variables
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), '.env')
load_dotenv(env_path)


class VideoGenerator:

    video_storage_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "db/storage/videos")
    image_storage_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "db/storage/images")
    audio_storage_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "db/storage/audios")
    subtitle_storage_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "db/storage/subtitles")

    def __init__(self, 
                 src: List[str] | str, 
                 video_path: str = video_storage_path,
                 audio_path: str = audio_storage_path,
                 image_path: str = image_storage_path,
                 subtitle_path: str = subtitle_storage_path,
                 openai_api_key: Optional[str] = None, 
                 stable_diff_api_key: Optional[str] = None):
        """
        :param src: List[str] would be a list of image file locations [db/storage/images/image1.png, ] or it can be
        a string "generate" which would use DALLE or Stable diffusion to generate new sets of images.

        :param video_path: Where the newly generated video is stored
        :param audio_path: Where the newly generated audio is stored
        :param image_path: Where the newly generated audio is stored
        :param openai_api_key - api key for OpenAI
        :param stable_diff_api_key - api key for Stable Diffusion
        """

        self.src = src
        self.video_path = video_path
        self.audio_path = audio_path
        self.image_path = image_path
        self.subtitle_path = subtitle_path
        
    def upload_images(self, image_files: List[str], destination_folder: str):
        """
        :param image_files: List of paths of images to upload
        :param destination_folder: Folder to which images will be uploaded
        """
        for image_file in image_files:
            shutil.copy(image_file, destination_folder)


    def read_audio_file(self, audio_file_path: str):
        """
        :param audio_file_path: Path of the audio file to read
        :return: Length of the audio file in seconds
        """
        audio = MP3(audio_file_path)
        return audio.info.length

    def create_video(self, image_files: List[str], audio_file_path: str, output_video_path: str):
        """
        :param image_files: List of paths of images to use for the video
        :param audio_file_path: Path of the audio file to use for the video
        :param output_video_path: Path of the output video file
        """
        # Calculate duration per image
        audio_length = self.read_audio_file(audio_file_path)
        duration_per_image = audio_length / len(image_files)
        
        # Open, resize and save images as gif
        images = [Image.open(image).resize((800, 800), Image.ANTIALIAS) for image in image_files]
        images[0].save("temp.gif", save_all=True, append_images=images[1:], duration=int(duration_per_image)*1000)
        
        # Combine audio and gif to create video
        video = editor.VideoFileClip("temp.gif")
        audio = editor.AudioFileClip(audio_file_path)
        final_video = video.set_audio(audio)
        final_video.write_videofile(output_video_path, fps=30, codec="libx264")
        
        # Delete temporary gif
        os.remove("temp.gif")
    
    def generate_video_static(self, audio_file_path: str, static_image: Optional[str] = None):
        """
        :param audio_file_path: Path of the audio file to use for the video
        :param static_image: Path of the static image, defaults to black
        """
        # Check static image
        if not static_image:
            static_image = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "db/storage/images/black_image.png")

        # Load the audio file
        audio = AudioFileClip(audio_file_path)

        # Load the static image file and convert it to a clip with the duration of the audio
        img_clip = ImageClip(static_image, duration=audio.duration)

        # Set the audio of the video to the audio clip
        video = img_clip.set_audio(audio)

        # Create file output path
        audio_name = os.path.splitext(os.path.basename(audio_file_path))[0] + ".mp4"
        video_file_path = os.path.join(self.video_path, audio_name)

        # Write the final video file
        video.write_videofile(video_file_path, codec='libx264', temp_audiofile='temp-audio.m4a', remove_temp=True, audio_codec='aac', fps=24)
        

    def generate_subtitles(self, auido_file_path: str, subtitle_file_path: str, language='en'):
        """
        :param language: Language code of the audio file's language (default is 'en' for English)
        """
        # Generate a subtitle file name (without path) from audio file
        subtitle_file_name = os.path.splitext(os.path.basename(subtitle_file_path))[0] + ".srt"

        # If subtitle file does not exist in the directory, generate it
        if not glob.glob(f"{self.subtitle_storage_path}/{subtitle_file_name}"):
            # TODO: Figure out how to generate subtitles. This seems to be the fix
            # https://stackoverflow.com/questions/66977227/could-not-load-dynamic-library-libcudnn-so-8-when-running-tensorflow-on-ubun
            pass


if __name__ == "__main__":

    img = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "db/storage/images/black_image.png")
    aud = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "db/storage/audios/test.mp3")
    vg = VideoGenerator(src=[img])
    vg.generate_video_static(aud, img)
