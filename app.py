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
    # Compress phone photo inside memory so it sends fast over networks
    drawing_image = Image.open(uploaded_file).convert("RGB")
    drawing_image.thumbnail((512, 512))
    
    img_byte_arr = io.BytesIO()
    drawing_image.save(img_byte_arr, format='JPEG')
    img_bytes = img_byte_arr.getvalue()

    if st.button("🚀 Transform Into Reality", type="primary"):
        with st.spinner("AI is terraforming your planet..."):
            
            # Reads the token securely from your Streamlit App settings
            HF_TOKEN = st.secrets["HF_TOKEN"]
            
            API_URL = "https://huggingface.co"
            headers = {"Authorization": f"Bearer {HF_TOKEN}"}
            
            payload = {
                "inputs": "A hyper-realistic stunning cinematic space photography version of this planet, 8k resolution, sci-fi scene",
                "image": img_bytes,
                "parameters": {"strength": 0.6}
            }
            
            try:
                response = requests.post(API_URL, headers=headers, json=payload)
                
                if response.status_code != 200:
                    response = requests.post(API_URL, headers=headers, data=img_bytes)
                
                result_img = Image.open(io.BytesIO(response.content))
                st.image(result_img, caption="Your AI Generated Exoplanet", use_container_width=True)
                st.balloons()
                
            except Exception as e:
                st.error("Server is busy loading the AI model. Tap the button again to retry!")
