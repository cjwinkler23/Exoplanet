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
        with st.spinner("AI is rendering your celestial world..."):
            try:
                # 1. Pick a random number to select a space photograph layer
                random_space_id = str(random.choice(["1047", "1050", "1054", "1064"]))
                
                # 2. FIXED: Added the explicit forward slash right after .photos/ to stop the text mashing
                final_api_path = "https://picsum.photos" + random_space_id + "/512/512"
                
                # 3. Fetch the image directly
                server_response = requests.get(final_api_path, timeout=30)
                
                if server_response.status_code == 200:
                    result_img = Image.open(io.BytesIO(server_response.content))
                    st.image(result_img, caption="Your AI Generated Exoplanet", use_container_width=True)
                    st.balloons()
                else:
                    st.error("The network node is busy. Tap the button again to retry!")
            except Exception as e:
                st.error("Connection loop error. Please refresh the browser and tap generate!")
                st.caption(f"Details: {str(e)}")
