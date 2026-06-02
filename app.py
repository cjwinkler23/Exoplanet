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
    drawing_image.save(img_byte_arr, format='JPEG', quality=80)
    img_bytes = img_byte_arr.getvalue()

    if st.button("🚀 Transform Into Reality", type="primary"):
        with st.spinner("AI is terraforming your planet layout..."):
            try:
                # 1. Pull your token securely from Streamlit Secrets
                token = st.secrets["HF_TOKEN"]
                
                # 2. Use the official client to talk to Hugging Face safely
                client = InferenceClient(api_key=token)
                
                # 3. Use the stable v1-5 model but FORCE a reliable cloud provider
                # This keeps the URL tiny and completely prevents parsing glitches!
                output_image = client.image_to_image(
                    img_bytes,
                    prompt="A hyper-realistic stunning 8k cinematic space photography version of this planet, highly detailed, beautiful cosmic stars background, sci-fi scene",
                    model="runwayml/stable-diffusion-v1-5",
                    provider="together" # FORCES a fast, open server to process your drawing bytes
                )
                
                # Display the authentic generated picture smoothly
                st.image(output_image, caption="Your AI Generated Exoplanet", use_container_width=True)
                st.balloons()
                
            except Exception as e:
                st.error("The AI provider network is busy. Please tap the button one more time to compile!")
                st.caption(f"Details: {str(e)}")
