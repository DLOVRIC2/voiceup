import streamlit as st
from story_generation.story_generator import StoryGenerator
from voice_generation.voice_generator import VoiceGenerator
import tempfile
import os
from pydub.utils import mediainfo






def main():
    st.title("Welcome to VoiceUp!")
    st.header("This is a platform for creators to create short clips based on their own content.")
    with st.expander("About the App"):
            st.write("AI Video Genereration app with Video's Summary and voice cloned feature")

    # Instantiate some variables in the session state
    if "story" not in st.session_state:
        st.session_state.story = ""
    
    if "voice_generator" not in st.session_state:
        st.session_state.voice_generator = None
    
    # Create an instance of StoryGenerator
    openai_api_key = st.text_input("Enter your OpenAI API Key", type="password")
    elevenlabs_api_key = st.text_input("Enter your ElvenLabs API Key", type="password")

    if openai_api_key:  # only instantiate StoryGenerator after API key is entered
        generator = StoryGenerator(api_key=openai_api_key)

    if elevenlabs_api_key:
        voice_generator = VoiceGenerator(api_key=elevenlabs_api_key)

    # User can select to provide full story or generate it
    story_option = st.selectbox("Choose an option:", ["I will provide the full story", "Generate story based on my summary"])

    if story_option == "I will provide the full story":

        with st.form(key="story_upload_option"):

            user_story = st.text_area("Enter your story here:", key="user_story")

            submit_button = st.form_submit_button(label="Generate")
            if submit_button:
                if user_story in ("", "None", None):
                    st.error("Make sure you enter your story above..")
                st.session_state.story = user_story

    elif story_option == "Generate story based on my summary":
            with st.form(key="story_gen_option"):

                story_summary = st.text_input("Enter a short summary for your story")
                submit_button = st.form_submit_button(label='Generate Story')

                if submit_button:
                    try:
                        with st.spinner('Generating your story...'):
                            # Generate story
                            story = generator.generate_story(story_summary)
                            # TODO: Implement a clean output text method
                            st.session_state.story = story.lstrip()
                        st.text_area("AI Generated Story:", value=st.session_state.story)

                    except UnboundLocalError:  # Catch the specific error you're interested in
                        st.error("Please enter your OpenAI API Key to generate a story.")
        
    
    audio_option = st.selectbox("Choose an option:", ["Use default voices", "Custom voice!"])
    if audio_option == "Use default voices":
        with st.form(key="voice_form"):

            voice = st.selectbox("Choose a voice:", voice_generator.get_list_of_voices())
            model = st.selectbox("Choose a model:", ["eleven_multilingual_v1"])

            voice_submit_button = st.form_submit_button(label="Generate Audio")
            if voice_submit_button:
                try:
                    with st.spinner("Generating your audio..."):
                        # Generate audio
                        audio = voice_generator.generate_story_audio(
                            text=st.session_state.story,
                            voice=voice,
                            model=model
                        )
                        
                        print(audio)
                        st.audio(audio, format="audio/mp3")
                except UnboundLocalError:  # Catch the specific error you're interested in
                    st.error("Please enter your ElevenLabs API Key to generate a story.")

    elif audio_option == "Custom voice!":
        with st.form(key="clone_form"):
            
            voice_name = st.text_input("Voice name:", key="voice_name")
            voice_description = st.text_input(
                label="Voice description:",
                key="voice_description",
                placeholder="An old American male voice with a slight hoarseness in his throat. Perfect for news"
                )
            
            voice_file = st.file_uploader("Upload a voice sample for the custom voice", type=['mp3', 'wav'])

            clone_submit_button = st.form_submit_button(label="Generate Audio")

            if clone_submit_button and voice_file is not None:
                print(voice_file)

                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
                    # Write the uploaded audio bytes to temp file
                    tmpfile.write(voice_file.getvalue())
                    tmp_filename = tmpfile.name
                # Add validation for maximum length of the audio file
                audio_info = mediainfo(tmp_filename)
                if float(audio_info["duration"]) > 120:
                    st.error("Uploaded audio is too long. Please upload an audio of maximum 2 minutes.")

                try:
                    with st.spinner("Creating the story audio with custom voice..."):
                        custom_audio = voice_generator.generate_story_with_new_voice(
                            text=st.session_state.story,
                            name=st.session_state.voice_name,
                            description=st.session_state.voice_description,
                            files=[tmp_filename]
                        )
                        print(custom_audio)
                        st.audio(custom_audio, format="audio/mp3")
                except Exception as e:
                    print(e)
                    st.error("Cloning went wrong...")
                finally:
                    os.remove(tmp_filename)
                




if __name__ == "__main__":
    main()
