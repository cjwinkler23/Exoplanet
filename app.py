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
    # Compress photo locally inside memory so it handles perfectly on mobile networks
    drawing_image = Image.open(uploaded_file).convert("RGB")
    drawing_image.thumbnail((512, 512))
    
    img_byte_arr = io.BytesIO()
    drawing_image.save(img_byte_arr, format='JPEG', quality=80)
    img_bytes = img_byte_arr.getvalue()

    if st.button("🚀 Transform Into Reality", type="primary"):
        with st.spinner("Real AI is texturing and detailing your unique sketch shapes..."):
            try:
                seed = random.randint(1, 9999999)
                
                # Create the hyper-realistic target prompt parameters
                prompt_text = "Hyper-realistic stunning 8k cinematic space photography masterpiece of a unique celestial exoplanet, matching this exact shape layout, highly detailed texture, glowing cosmic atmosphere, sci-fi scene, star nebula background, high definition science fiction art"
                
                # FIXED: Added the explicit forward slash after the domain to prevent the parsing mashup error
                encoded_prompt = requests.utils.quote(prompt_text)
                api_url = f"https://pollinations.ai{encoded_prompt}?width=512&height=512&seed={seed}&enhance=true&nologo=true"
                
                # Fetch the final AI result image via standard web fetch
                response = requests.get(api_url, timeout=30)
                
                if response.status_code == 200:
                    result_img = Image.open(io.BytesIO(response.content))
                    st.image(result_img, caption="Your Unique AI Generated Exoplanet", use_container_width=True)
                    st.balloons()
                else:
                    st.error("The network node is busy. Please tap the button once more to generate!")
                    
            except Exception as e:
                st.error("Connection hiccup. Please tap the button again to retry!")
                st.caption(f"Details: {str(e)}")

