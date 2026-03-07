import streamlit as st
import base64
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize model
model = ChatOpenAI(model="gpt-4o-mini")

st.set_page_config(page_title="AI Image Analyzer", layout="centered")

st.title("🖼️ AI Image Analyzer")
st.write("Upload an image and type what you want the AI to do with it.")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# # User custom prompt
prompt = st.text_input("Enter your prompt for the image:")

if uploaded_file is not None:

    # Show preview
    st.image(uploaded_file, caption="Uploaded Image", width=500)

#     # Convert to base64
    image_bytes = uploaded_file.read()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    if st.button("Analyze Image"):

        if not prompt.strip():
            st.warning("Please enter a prompt to analyze the image.")
        else:
            with st.spinner("Analyzing image..."):
                

                message = HumanMessage(
                    content=[
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                )

                response = model.invoke([message])

                st.subheader("🧠 AI Response")
                st.write(response.content)