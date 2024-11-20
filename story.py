import cohere
import streamlit as st

# Set up your Cohere API key
cohere_api_key = "w0MZoCA0uGdMpLYoE6URut4S8FJEgGB1wRWOTYXj"  # Replace with your actual Cohere API key
co = cohere.Client(cohere_api_key)

# Function to generate a story using Cohere API
def generate_story(prompt):
    # Crafting a detailed prompt to ensure a full story
    detailed_prompt = (
        f"Write a detailed and engaging story based on the following idea: {prompt}\n\n"
        "The story should include vivid descriptions, character development, and an exciting plot. "
        "Ensure the story has an introduction, a conflict or challenge, and a resolution."
    )
    
    # Generate the story
    response = co.generate(
        model='command-xlarge-nightly',  # The model to use
        prompt=detailed_prompt,
        max_tokens=600,  # Increased token limit for more detailed output
        temperature=0.9,  # Higher creativity for storytelling
        stop_sequences=["--END--"]  # Ensure it doesn't end abruptly
    )
    
    # Return the generated story
    return response.generations[0].text.strip()

# Streamlit UI for generating story
st.set_page_config(page_title="Text to Story Generator", layout="centered")

st.title("Generate a Story from a Prompt")

# Text input for prompt
prompt = st.text_area("Enter your story prompt", placeholder="Once upon a time...")

# Button to generate the story
if st.button("Generate Story"):
    if prompt:
        with st.spinner("Generating your story..."):
            try:
                # Generate story
                story = generate_story(prompt)
                st.subheader("Generated Story")
                st.write(story)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a prompt to generate the story.")

# Footer
st.markdown("---")
st.caption("Created with ❤ using Streamlit and Cohere.")