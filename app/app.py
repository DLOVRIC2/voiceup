import streamlit as st

def main():
    st.title("Welcome to VoiceUp!")
    st.header("This is a platform for creators to create short clips based on their own content.")

    # taking user inputs
    story_summary = st.text_input("Enter a short summary for your story")
    story_keywords = st.text_input("Enter up to 5 keywords for your story, separated by commas")

    if st.button("Generate Story"):
        # replace the following line with the actual functions to generate story, voice and video
        st.write("Story, voice and video will be generated here!")

if __name__ == "__main__":
    main()
