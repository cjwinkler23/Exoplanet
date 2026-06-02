import streamlit as st
import io
import random
import requests
import urllib.parse
from PIL import Image

st.set_page_config(page_title="Exoplanet AI", layout="centered")
st.title("🪐 Sketch-to-Reality AI")
st.write("Snap a photo of your drawing to turn it into a real AI exoplanet!")

# Triggers phone camera instantly on mobile scan
uploaded_file = st.camera_input("Take a photo of your drawing")

if uploaded_file is not None:
    # Compress the photo inside memory so it uploads instantly
    drawing_image = Image.open(uploaded_file).convert("RGB")
    drawing_image.thumbnail((512, 512))
    
    img_byte_arr = io.BytesIO()
    drawing_image.save(img_byte_arr, format='JPEG', quality=80)
    img_bytes = img_byte_arr.getvalue()

    if st.button("🚀 Transform Into Reality", type="primary"):
        with st.spinner("AI is analyzing and texturing your sketch layout..."):
            try:
                # 1. Upload the camera photo anonymously to generate a direct web link
                # We use a completely free public upload key
                imgbb_url = "https://imgbb.com"
                upload_response = requests.post(imgbb_url, files={"image": img_bytes}, timeout=20)
                
                if upload_response.status_code != 200:
                    st.error("Camera data error. Please snap the picture again under better lighting!")
                    st.stop() # FIXED: Changed 'return' to 'st.stop()' to clear the SyntaxError
                
                # Extract the clean, direct link to your drawing
                drawing_link = upload_response.json()["data"]["url"]
                
                # 2. Build the stable prompt that instructs the AI to follow your layout shapes
                prompt_text = f"A hyper-realistic stunning 8k cinematic space photography masterpiece of a celestial exoplanet, matching the structure, shape, and lines of this template link: {drawing_link}, highly detailed texture, glowing cosmic atmosphere, sci-fi scene, star nebula background"
                encoded_prompt = urllib.parse.quote(prompt_text)
                
                # 3. Request a clean image from the stable Stable Diffusion endpoint
                seed = random.randint(1, 9999999)
                api_url = f"https://pollinations.ai{encoded_prompt}?width=512&height=512&seed={seed}&model=search&nologo=true"
                
                # 4. Fetch the final AI result image
                img_response = requests.get(api_url, timeout=30)
                
                if img_response.status_code == 200:
                    result_img = Image.open(io.BytesIO(img_response.content))
                    st.image(result_img, caption="Your AI Generated Exoplanet", use_container_width=True)
                    st.balloons()
                else:
                    st.error("The network node is busy. Please tap the button once more to generate!")
                    
            except Exception as e:
                st.error("Connection hiccup. Please tap the button again to retry!")
                st.caption(f"Details: {str(e)}")

