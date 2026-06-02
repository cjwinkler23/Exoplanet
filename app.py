import streamlit as st
import io
import random
import requests
import base64
import urllib.parse
from PIL import Image

st.set_page_config(page_title="Exoplanet AI", layout="centered")
st.title("🪐 Sketch-to-Reality AI")
st.write("Snap a photo of your drawing to turn it into a real AI exoplanet!")

# Triggers phone camera instantly on mobile scan
uploaded_file = st.camera_input("Take a photo of your drawing")

if uploaded_file is not None:
    # Compress the photo inside memory so it converts fast
    drawing_image = Image.open(uploaded_file).convert("RGB")
    drawing_image.thumbnail((400, 400)) # Sized perfectly for inline web encoding
    
    img_byte_arr = io.BytesIO()
    drawing_image.save(img_byte_arr, format='JPEG', quality=70)
    img_bytes = img_byte_arr.getvalue()

    if st.button("🚀 Transform Into Reality", type="primary"):
        with st.spinner("AI is analyzing and texturing your sketch layout..."):
            try:
                # 1. Convert the drawing bytes straight into a clean text data stream
                base64_string = base64.b64encode(img_bytes).decode('utf-8')
                inline_data_uri = f"data:image/jpeg;base64,{base64_string}"
                
                # 2. Build the stable text instructions telling the AI to copy the layout
                prompt_text = f"A hyper-realistic stunning 8k cinematic space photography masterpiece of a celestial exoplanet, matching the exact composition, shape, and structure of this image: {inline_data_uri}, highly detailed texture, glowing cosmic atmosphere, sci-fi scene, star nebula background"
                encoded_prompt = urllib.parse.quote(prompt_text)
                
                # 3. Direct endpoint URL targeting the search model tier
                seed = random.randint(1, 9999999)
                api_url = f"https://pollinations.ai{encoded_prompt}?width=512&height=512&seed={seed}&model=search&nologo=true"
                
                # 4. Fetch the final AI result image via standard web fetch
                img_response = requests.get(api_url, timeout=30)
                
                if img_response.status_code == 200:
                    result_img = Image.open(io.BytesIO(img_response.content))
                    st.image(result_img, caption="Your AI Generated Exoplanet", use_container_width=True)
                    st.balloons()
                else:
                    st.error("The network node is busy. Please tap the button once more to generate!")
                    
            except Exception as e:
                st.error("The processing node timed out. Please tap the button again to retry!")
                st.caption(f"Details: {str(e)}")
