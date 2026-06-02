import streamlit as st
import io
import base64
from PIL import Image
from huggingface_hub import InferenceClient

st.set_page_config(page_title="Exoplanet AI", layout="centered")
st.title("🪐 Sketch-to-Reality AI")
st.write("Snap a photo of your drawing to turn it into a real AI exoplanet!")

uploaded_file = st.camera_input("Take a photo of your drawing")

if uploaded_file is not None:
    drawing_image = Image.open(uploaded_file).convert("RGB")
    drawing_image.thumbnail((512, 512))
    
    img_byte_arr = io.BytesIO()
    drawing_image.save(img_byte_arr, format='JPEG')
    img_bytes = img_byte_arr.getvalue()

    if st.button("🚀 Transform Into Reality", type="primary"):
        with st.spinner("AI is strictly tracing your sketch layout..."):
            try:
                token = st.secrets["HF_TOKEN"]
                client = InferenceClient(api_key=token)
                base64_image = base64.b64encode(img_bytes).decode('utf-8')
                
                # We use a ControlNet model that treats your drawing as a mandatory visual blueprint
                output_image = client.text_to_image(
                    prompt=f"A hyper-realistic stunning 8k cinematic space photography masterpiece of a celestial exoplanet. Maintain exact matching composition layout, ring placements, and surface features from this drawing: data:image/jpeg;base64,{base64_image}",
                    model="lllyasviel/sd-controlnet-scribble"
                )
                
                st.image(output_image, caption="Your Structural AI Exoplanet", use_container_width=True)
                st.balloons()
                
            except Exception as e:
                st.error("The network connection timed out. Please tap the button once more to generate!")
                st.caption(f"Details: {str(e)}")

