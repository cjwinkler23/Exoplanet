import streamlit as st
from openai import OpenAI
from PIL import Image
import io
import base64

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Exoplanet Drawing Enhancer 🌌")

image_file = st.file_uploader(
    "Choose an image",
    type=["png", "jpg", "jpeg"]
)

def compress_and_resize(image_file):
    image = Image.open(image_file)

    if image.mode != "RGB":
        image = image.convert("RGB")

    # input cap (prevents huge uploads)
    image.thumbnail((1024, 1024))

    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=85)
    buffer.seek(0)

    return buffer


if image_file:

    st.image(image_file, caption="Input image", use_container_width=True)

    if st.button("Generate Exoplanet Visualization 🌠"):

        with st.spinner("Rendering exoplanet..."):

            compressed_image = compress_and_resize(image_file)
            base64_image = base64.b64encode(compressed_image.read()).decode("utf-8")

            response = client.images.edit(
                model="gpt-image-1",
                image=compressed_image,
                prompt=(
                    "You are an exoplanet visualization assistant. When a user uploads a hand-drawn exoplanet sketch, "
                    "create a scientifically plausible, photorealistic exoplanet based on the drawing. "
                    "Preserve the overall shape, cloud bands, storms, colors, and major features while converting the sketch "
                    "into a high-resolution space image. Place the planet in realistic space with physically consistent lighting "
                    "and atmospheric detail."
                ),
                size="1024x1024"
            )

        st.success("Done!")

        image_base64 = response.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)
        
        st.image(image_bytes, caption="Generated Exoplanet", use_container_width=True)
