from elevenlabs import set_api_key
import os
from dotenv import load_dotenv
from elevenlabs import generate, play



# Load the environment variables
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
env_paht = os.path.join(project_root, ".env")
load_dotenv(env_paht)


class VoiceGenerator:

    def __init__(self, api_key: str = None):

        if os.environ.get("ELEVEN_LABS_KEY"):
            set_api_key(os.environ.get("ELEVEN_LABS_KEY"))
        else:
            if not api_key:
                raise ValueError("API Key must be provided if ELEVEN_LABS_KEY environment variable is not set")
            set_api_key(api_key)
        
        self.audio_file = "db/storage/audios"
    
    def generate_story_audio(self, text: str, voice: str = "Arnold", model: str = "eleven_multilingual_v1"):

        # TODO: Implement some kind of file naming protocol
        # Get the absolute path to the current script's directory
        current_script_dir = os.path.dirname(os.path.realpath(__file__))

        # Move two directories up ('voice_generation' -> 'app' -> 'voiceup')
        two_dirs_up = os.path.dirname(os.path.dirname(current_script_dir))

        # Define a relative path to the audio file from the current directory
        relative_path = "db/storage/audios/test.mp3"

        # Create the absolute path to the audio file
        audio_path = os.path.join(two_dirs_up, relative_path)

        audio = generate(
            text=text,
            voice=voice,
            model=model
        )
        
        try:
            with open(audio_path, 'wb') as f:
                f.write(audio)

            return audio_path
        
        except Exception as e:
            print(e)

            return ""


if __name__ == "__main__":

    voice_generator = VoiceGenerator()

    print(voice_generator.generate_story_audio("Hello, this is Arnold!"))

