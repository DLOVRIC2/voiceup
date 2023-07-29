from elevenlabs import set_api_key, generate
import os
from dotenv import load_dotenv

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

        # Define the path to the audio file storage directory
        self.audio_file_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), 'db', 'storage', 'audios')
        # Create the directory and its parent directories if they don't exist
        if not os.path.exists(self.audio_file_dir):
            os.makedirs(self.audio_file_dir)
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
    
    @staticmethod
    def generate_list_of_voices():
        pass




if __name__ == "__main__":

    voice_generator = VoiceGenerator()

    print(voice_generator.generate_story_audio("Hello, this is Arnold!"))
