import streamlit as st
import cohere
from PIL import Image

# Initialize the Cohere client
COHERE_API_KEY = "RzWMNercdb7YX2sEYlJwetX5jHWINcBmX0PSN2Sm"  # Replace with your actual Cohere API key
cohere_client = cohere.Client(COHERE_API_KEY)

# Function to simulate image processing and extract food items
def extract_food_items(image):
    """
    Placeholder function to simulate food item extraction from an image.
    Replace this with a real image processing model if available.
    """
    # Simulated food items (e.g., detected using an ML model in practice)
    return ["Apple", "Banana", "Grilled Chicken", "Salad"]

# Function to generate a nutrition analysis using Cohere
def generate_nutrition_analysis(food_items):
    """
    Generate nutrition analysis using the Cohere API.
    """
    # Create a formatted food list for the prompt
    food_list = "\n".join([f"{i+1}. {item}" for i, item in enumerate(food_items)])
    prompt = f"""
    You are a professional nutritionist. Based on the following list of food items:
    {food_list}
    
    Provide:
    1. Total calorie count.
    2. Detailed calorie breakdown for each food item.
    """

    try:
        # Generate response using Cohere
        response = cohere_client.generate(
            model="command-xlarge-nightly",
            prompt=prompt,
            max_tokens=300,
            temperature=0.7,
        )
        return response.generations[0].text.strip()
    except Exception as e:
        return f"Error generating response: {e}"

# Streamlit app configuration
st.set_page_config(page_title="Cohere Nutrition Analyzer", layout="centered")

st.title("🍎 Nutrition Analysis with Cohere 🤖")
st.write("Upload an image of your meal to get its nutrition breakdown!")

# File uploader for the image
uploaded_file = st.file_uploader("Upload an image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Analyze button
if st.button("Analyze Meal"):
    if image:
        with st.spinner("Analyzing your meal..."):
            try:
                # Simulate food item extraction from the image
                food_items = extract_food_items(image)

                # Generate the Cohere response
                nutrition_response = generate_nutrition_analysis(food_items)

                # Display the nutrition analysis
                st.subheader("Nutrition Analysis")
                st.write(nutrition_response)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.error("Please upload an image of your meal.")
