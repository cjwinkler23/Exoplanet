import streamlit as st
import io
from PIL import Image
from huggingface_hub import InferenceClient

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
        with st.spinner("AI is terraforming your planet..."):
            try:
                # 1. Pull token securely from Streamlit Secrets
                token = st.secrets["HF_TOKEN"]
                
                # 2. Use the official client to bypass manual server routing blocks
                client = InferenceClient(api_key=token)
                
                # 3. Use the highly active, fully supported v1-5 model
                output_image = client.image_to_image(
                    img_bytes,
                    prompt="A hyper-realistic stunning cinematic space photography version of this planet, highly detailed, beautiful cosmic stars background, 8k resolution, sci-fi scene",
                    model="runwayml/stable-diffusion-v1-5"
                )
                
                # Display the authentic generated picture smoothly
                st.image(output_image, caption="Your AI Generated Exoplanet", use_container_width=True)
                st.balloons()
                
            except Exception as e:
                st.error("The AI network is resetting. Please tap the button one more time to compile!")
                st.caption(f"Details: {str(e)}")
