import streamlit as st
from story_generation.story_generator import StoryGenerator
from voice_generation.voice_generator import VoiceGenerator


def main():
    st.title("Welcome to VoiceUp!")
    st.header("This is a platform for creators to create short clips based on their own content.")

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
        user_story = st.text_area("Enter your story here:")
        if st.button("Submit Story"):
            st.text_area("Your Story:", value=user_story, max_chars=None)
            st.session_state.story = user_story

    else: # story_option == "Generate story based on my summary"
        with st.form(key='my_form'):
            story_summary = st.text_input("Enter a short summary for your story")
            submit_button = st.form_submit_button(label='Generate Story')

            if submit_button:
                try:
                    with st.spinner('Generating your story...'):
                        # Generate story
                        story = generator.generate_story(story_summary)
                        st.session_state.story = story
                    # TODO: Implement a clean output text method
                    st.text_area("AI Generated Story:", value=story.lstrip())

                except UnboundLocalError:  # Catch the specific error you're interested in
                    st.error("Please enter your OpenAI API Key to generate a story.")

        
        with st.form(key="voice_form"):
            voice = st.selectbox("Choose a voice:", ["Arnold", "Adam"])
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


if __name__ == "__main__":
    main()
