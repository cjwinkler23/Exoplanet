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
    # Compress photo inside memory so it sends fast over networks
    drawing_image = Image.open(uploaded_file).convert("RGB")
    drawing_image.thumbnail((512, 512))
    
    img_byte_arr = io.BytesIO()
    drawing_image.save(img_byte_arr, format='JPEG')
    img_bytes = img_byte_arr.getvalue()

    if st.button("🚀 Transform Into Reality", type="primary"):
        with st.spinner("AI is transforming your drawing structure..."):
            try:
                # 1. Pull token securely from Streamlit Secrets
                token = st.secrets["HF_TOKEN"]
                
                # 2. Use an active model designed for native image transformation tasks
                API_URL = "https://huggingface.co"
                headers = {"Authorization": f"Bearer {token}"}
                
                # Send the raw compressed bytes straight to the active image handler
                response = requests.post(API_URL, headers=headers, data=img_bytes)
                
                # Render the final beautiful AI generation block on layout
                result_img = Image.open(io.BytesIO(response.content))
                st.image(result_img, caption="Your AI Transformed Exoplanet", use_container_width=True)
                st.balloons()
                
            except Exception as e:
                st.error("The network pipeline is busy. Please tap the button once more to compile!")
                st.caption(f"Details: {str(e)}")
