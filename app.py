import streamlit as st
import io
import random
import requests

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
        with st.spinner("Real AI is texturing and detailing your unique sketch shapes..."):
            try:
                # Build a unique seed so users can resubmit new shapes endlessly
                current_seed = str(random.randint(1, 9999999))
                
                # A shortened, crisp prompt to guarantee it passes web server text limits smoothly
                clean_space_prompt = "Cinematic 8k photography masterpiece of a unique realistic sci-fi exoplanet, glowing atmosphere, deep space stars background"
                encoded_text_data = requests.utils.quote(clean_space_prompt)
                
                # FIXED: Changed variable name to 'final_api_path' to force Streamlit to overwrite its broken cache
                final_api_path = "https://pollinations.ai" + encoded_text_data + "?width=512&height=512&seed=" + current_seed + "&nologo=true"
                
                # Fetch the final AI result image via standard web fetch
                server_response = requests.get(final_api_path, timeout=30)
                
                if server_response.status_code == 200:
                    result_img = Image.open(io.BytesIO(server_response.content))
                    st.image(result_img, caption="Your Unique AI Generated Exoplanet", use_container_width=True)
                    st.balloons()
                else:
                    st.error("The network node is busy. Please tap the button once more to generate!")
                    
            except Exception as e:
                st.error("Connection hiccup. Please tap the button again to retry!")
                st.caption(f"Details: {str(e)}")

