import streamlit as st
import cohere

# Initialize Cohere API client
COHERE_API_KEY = "RzWMNercdb7YX2sEYlJwetX5jHWINcBmX0PSN2Sm"  # Replace with your actual API key
co = cohere.Client(COHERE_API_KEY)

# Function to get response from Cohere
def get_cohere_response(input_text, no_words, blog_style):
    # Create a prompt for blog generation
    prompt = f"""
    Write a blog in the style of {blog_style} for the topic "{input_text}" within {no_words} words.
    The blog should be engaging, informative, and easy to understand.
    """
    
    # Generate the response using Cohere
    try:
        response = co.generate(
            model="command-xlarge-nightly",  # Use the desired Cohere model
            prompt=prompt,
            max_tokens=int(no_words),  # Adjust the output length
            temperature=0.7  # Control creativity
        )
        return response.generations[0].text.strip()
    except Exception as e:
        return f"Error: {e}"

# Streamlit UI
st.set_page_config(
    page_title="Generate Blogs",
    page_icon='🤖',
    layout='centered',
    initial_sidebar_state='collapsed'
)

st.header("Generate Blogs 🤖")

# Input fields
input_text = st.text_input("Enter the Blog Topic")

# Two columns for additional fields
col1, col2 = st.columns([5, 5])

with col1:
    no_words = st.text_input('No of Words', value="300")  # Default word count
with col2:
    blog_style = st.selectbox(
        'Writing the blog for',
        ('Researchers', 'Data Scientist', 'Common People'),
        index=0
    )

# Generate button
submit = st.button("Generate")

# Final response
if submit:
    if input_text and no_words.isdigit() and int(no_words) > 0:
        with st.spinner("Generating..."):
            response = get_cohere_response(input_text, no_words, blog_style)
            st.subheader("Generated Blog:")
            st.write(response)
    else:
        st.error("Please provide a valid blog topic and a positive number for word count.")