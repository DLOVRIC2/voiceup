import streamlit as st
from story_generation.story_generator import StoryGenerator

def main():
    st.title("Welcome to VoiceUp!")
    st.header("This is a platform for creators to create short clips based on their own content.")

    # Create an instance of StoryGenerator
    generator = StoryGenerator()

    # User can select to provide full story or generate it
    story_option = st.selectbox("Choose an option:", ["I will provide the full story", "Generate story based on my summary"])

    if story_option == "I will provide the full story":
        user_story = st.text_area("Enter your story here:")
        if st.button("Submit Story"):
            st.text_area("Your Story:", value=user_story, max_chars=None)

    else: # story_option == "Generate story based on my summary"
        with st.form(key='my_form'):
            story_summary = st.text_input("Enter a short summary for your story")
            submit_button = st.form_submit_button(label='Generate Story')

            if submit_button:
                with st.spinner('Generating your story...'):
                    # Generate story
                    story = generator.generate_story(story_summary)
                # TODO: Implement a clean output text method
                st.text_area("AI Generated Story:", value=story.lstrip())

if __name__ == "__main__":
    main()
