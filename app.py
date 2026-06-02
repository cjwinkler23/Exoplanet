import streamlit as st
import requests
import io
from PIL import Image

st.set_page_config(page_title="Exoplanet AI", layout="centered")
st.title("🪐 Sketch-to-Reality AI")
st.write("Snap a photo of your drawing to turn it into a real AI exoplanet!")

# Triggers phone camera instantly on mobile scan
uploaded_file = st.camera_input("Take a photo of your drawing")

if uploaded_file is not None:
    # 1. Compress phone photo inside memory so it sends fast
    drawing_image = Image.open(uploaded_file).convert("RGB")
    drawing_image.thumbnail((512, 512))
    
    img_byte_arr = io.BytesIO()
    drawing_image.save(img_byte_arr, format='JPEG')
    img_bytes = img_byte_arr.getvalue()

    if st.button("🚀 Transform Into Reality", type="primary"):
        with st.spinner("AI is terraforming your planet..."):
            
            # Fast, free Hugging Face Serverless API URL
            API_URL = "https://huggingface.co"
            
            payload = {
                "inputs": "A hyper-realistic stunning cinematic space photography version of this planet, 8k resolution, sci-fi scene",
                "image": img_bytes,
                "parameters": {"strength": 0.6} # 0.6 means it keeps your drawing layout shape
            }
            
            try:
                response = requests.post(API_URL, json=payload)
                
                # Show the real AI image directly on screen
                result_img = Image.open(io.BytesIO(response.content))
                st.image(result_img, caption="Your AI Generated Exoplanet", use_container_width=True)
                st.balloons()
                
            except Exception as e:
                st.error("Server glitch. Tap the button again to retry!")
