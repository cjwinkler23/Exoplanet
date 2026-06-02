import streamlit as st
import io
import random
import requests
from PIL import Image

st.set_page_config(page_title="Exoplanet AI", layout="centered")
st.title("🪐 Sketch-to-Reality AI")
st.write("Snap a photo of your drawing to turn it into a real AI exoplanet!")

uploaded_file = st.camera_input("Take a photo of your drawing")

if uploaded_file is not None:
    drawing_image = Image.open(uploaded_file).convert("RGB")
    drawing_image.thumbnail((512, 512))
    
    img_byte_arr = io.BytesIO()
    drawing_image.save(img_byte_arr, format='JPEG', quality=80)
    img_bytes = img_byte_arr.getvalue()

    if st.button("🚀 Transform Into Reality", type="primary"):
        with st.spinner("AI is rendering your drawing layout..."):
            try:
                seed = random.randint(1, 9999999)
                
                # Fixed destination URL with zero text paths to eliminate parsing glitches
                api_url = "https://pollinations.ai"
                
                # Data is sent safely inside a data dictionary instead of the URL string
                payload = {
                    "prompt": "Hyper-realistic stunning 8k cinematic space photography masterpiece of a celestial exoplanet, matching this exact shape layout, highly detailed texture, glowing cosmic atmosphere, sci-fi scene, star nebula background",
                    "width": 512,
                    "height": 512,
                    "seed": seed,
                    "nologo": True
                }
                
                files = {"image": ("sketch.jpg", img_bytes, "image/jpeg")}
                
                # Transmit safely to the cloud processing center
                response = requests.post(api_url, data=payload, files=files, timeout=30)
                
                if response.status_code == 200:
                    result_img = Image.open(io.BytesIO(response.content))
                    st.image(result_img, caption="Your AI Generated Exoplanet", use_container_width=True)
                    st.balloons()
                else:
                    st.error("The rendering node is adjusting. Tap the button once more to compile!")
                    st.caption(f"Status Code: {response.status_code}")
                    
            except Exception as e:
                st.error("Connection hiccup. Please tap the button again to retry!")
                st.caption(f"Details: {str(e)}")
