import streamlit as st
import io
import random
import requests
from PIL import Image

st.set_page_config(page_title="Exoplanet AI", layout="centered")
st.title("🪐 Sketch-to-Reality AI")
st.write("Snap a photo of your drawing to turn it into a real AI exoplanet!")

# Triggers phone camera instantly on mobile scan
uploaded_file = st.camera_input("Take a photo of your drawing")

if uploaded_file is not None:
    # 1. Compress the phone image down inside local memory so it sends instantly
    drawing_image = Image.open(uploaded_file).convert("RGB")
    drawing_image.thumbnail((512, 512))
    
    img_byte_arr = io.BytesIO()
    drawing_image.save(img_byte_arr, format='JPEG', quality=80)
    img_bytes = img_byte_arr.getvalue()

    if st.button("🚀 Transform Into Reality", type="primary"):
        with st.spinner("AI is rendering your drawing layout..."):
            try:
                # 2. Build a unique seed so users can resubmit new shapes endlessly
                seed = random.randint(1, 9999999)
                
                # 3. Create the hyper-realistic target prompt parameters
                prompt_text = "Hyper-realistic stunning 8k cinematic space photography masterpiece of a celestial exoplanet, matching this exact shape layout, highly detailed texture, glowing cosmic atmosphere, sci-fi scene, star nebula background"
                
                # 4. Route through the active image-to-image endpoint 
                api_url = f"https://pollinations.ai{requests.utils.quote(prompt_text)}?width=512&height=512&seed={seed}&nologo=true"
                
                # 5. Package the camera snap as a standard form upload stream
                files = {"image": ("sketch.jpg", img_bytes, "image/jpeg")}
                
                # Transmit directly to the processing server grid
                response = requests.post(api_url, files=files, timeout=30)
                
                if response.status_code == 200:
                    result_img = Image.open(io.BytesIO(response.content))
                    st.image(result_img, caption="Your AI Generated Exoplanet", use_container_width=True)
                    st.balloons()
                else:
                    st.error("The rendering node is adjusting. Tap the button once more to compile!")
                    
            except Exception as e:
                st.error("Connection hiccup. Please tap the button again to retry!")
                st.caption(f"Details: {str(e)}")
