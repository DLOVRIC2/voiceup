from elevenlabs import set_api_key, generate, voices, clone
import os
from dotenv import load_dotenv
from typing import List
import logging

# Load the environment variables
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), '.env')
load_dotenv(env_path)


class VoiceGenerator:

    def __init__(self, api_key: str = None):

        # Try to use the environment variable, if not present use the provided key
        key = os.environ.get("ELEVEN_LABS_KEY", api_key)
        if not key:
            raise ValueError("API Key must be provided if ELEVEN_LABS_KEY environment variable is not set")
        set_api_key(key)

        # Define the path to the audio file storage directory (db is copied into app folder in docker)
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        storage_dir = "app/db/storage" if os.path.exists(os.path.join(root_dir, "app/db/storage")) else "db/storage"
        self.audio_file_dir = os.path.join(storage_dir, "audios")

        # Create the directory and its parent directories if they don't exist
        if not os.path.exists(self.audio_file_dir):
            os.makedirs(self.audio_file_dir, exist_ok=True)
            
    def generate_story_audio(self, text: str, voice: str = "Arnold", model: str = "eleven_multilingual_v1"):

        # TODO: Implement some kind of file naming protocol
        audio_path = os.path.join(self.audio_file_dir, 'test.mp3')

        audio = generate(text=text, voice=voice, model=model)

        try:
            with open(audio_path, 'wb') as f:
                f.write(audio)

            return audio_path

        except Exception as e:
            print(e)
            return ""

    def generate_story_with_new_voice(self, text: str, name: str, description: str, files: List[str]):

        audio_path = os.path.join(self.audio_file_dir, f"{name}.mp3")

        voice = clone(
            name=name,
            description=description,
            files=files
        )

        audio = generate(text=text, voice=voice)

        try:
            with open(audio_path, "wb") as f:
                f.write(audio)
            return audio_path

        except Exception as e:
            print(e)
            return ""
    
    @staticmethod
    def get_list_of_voices():
        return [v.name for v in voices()]


if __name__ == "__main__":

    voice_generator = VoiceGenerator()

    # print(voice_generator.generate_story_audio("Hello, this is Arnold!"))
    print(voice_generator.get_list_of_voices())
