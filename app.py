import streamlit as st
import io
import base64
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
        with st.spinner("AI is aligning textures to your drawing structure..."):
            try:
                # 1. Pull token securely from Streamlit Secrets
                token = st.secrets["HF_TOKEN"]
                
                # 2. Use the official client to bypass manual server routing blocks
                client = InferenceClient(api_key=token)
                
                # Convert the image bytes into a clean text-based data stream the API can read
                base64_image = base64.b64encode(img_bytes).decode('utf-8')
                
                # 3. We use the working SDXL model but inject strict text styling boundaries
                output_image = client.text_to_image(
                    prompt=f"Make this image of an exoplanet look slightly more realistic but keep it a sphere and make sure it looks like a planet: data:image/jpeg;base64,{base64_image}",
                    negative_prompt="different layout, modified composition, ignoring the source drawing, changing the shape, text, labels, words, bad anatomy, deformed planet",
                    model="stabilityai/stable-diffusion-xl-base-1.0"
                )
                
                # Display the authentic generated picture smoothly
                st.image(output_image, caption="Your Aligned AI Exoplanet", use_container_width=True)
                st.balloons()
                
            except Exception as e:
                st.error("The network connection timed out. Please tap the button once more to generate!")
                st.caption(f"Details: {str(e)}")

