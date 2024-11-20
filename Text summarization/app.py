import streamlit as st
import cohere

# Initialize Cohere API client
API_KEY = "RzWMNercdb7YX2sEYlJwetX5jHWINcBmX0PSN2Sm"  # Replace with your Cohere API key
co = cohere.Client(API_KEY)

# Streamlit App
st.set_page_config(page_title="Text Summarization with Cohere", page_icon="📝", layout="centered")
st.title("📝 Text Summarization with Cohere API")
st.markdown("### Enter the text you want to summarize:")

# Apply custom CSS for styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f5f5; /* Light grey background */
        padding: 2rem; /* Add padding */
        border-radius: 10px; /* Rounded corners */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Add shadow */
    }
    textarea, .stButton>button {
        font-size: 1rem; /* Increase font size */
    }
    .stButton>button {
        background-color: #007bff; /* Bootstrap primary color */
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #0056b3; /* Darker shade on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Text input from user
user_input = st.text_area("Input Text", height=200)

# Summarize button
if st.button("Summarize"):
    if not user_input.strip():
        st.error("Please enter text to summarize.")
    else:
        with st.spinner("Summarizing..."):
            try:
                # Call the Cohere API for summarization
                response = co.summarize(
                    text=user_input,
                    length="medium",  # Options: "short", "medium", "long"
                    format="paragraph",  # Options: "paragraph", "bullets"
                    model="summarize-xlarge",  # Choose the model
                )
                summary = response.summary
                st.subheader("Summary:")
                st.write(summary)
            except Exception as e:
                st.error(f"An error occurred: {e}")
