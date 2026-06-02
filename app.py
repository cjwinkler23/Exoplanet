import streamlit as st
from openai import OpenAI
from PIL import Image
import io
import base64

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Exoplanet Drawing Enhancer 🌌")

st.write("Take a photo or upload your exoplanet drawing")

# Camera-first UX for QR scans
image_file = st.camera_input("Take a photo")

if image_file is None:
    image_file = st.file_uploader("Or upload an image", type=["png", "jpg", "jpeg"])


def compress_and_resize(image_file):
    image = Image.open(image_file)

    # Convert RGBA → RGB if needed (avoids errors)
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Resize while keeping aspect ratio (max 1024px)
    image.thumbnail((1024, 1024))

    # Compress image
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=85)
    buffer.seek(0)

    return buffer


if image_file:

    st.image(image_file, caption="Input image", use_container_width=True)

    if st.button("Generate Hyper-Realistic Exoplanet"):

        with st.spinner("Compressing image and sending to AI..."):

            compressed_image = compress_and_resize(image_file)

            base64_image = base64.b64encode(compressed_image.read()).decode("utf-8")

            response = client.responses.create(
                model="gpt-4.1-mini",
                input=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": (
                                    "You are an exoplanet visualization assistant. When a user uploads a hand-drawn exoplanet sketch, "
                                    "create a scientifically plausible, photorealistic exoplanet based on the drawing. "
                                    "Preserve the overall shape, cloud bands, storms, colors, and major features while converting the sketch "
                                    "into a high-resolution space image. Place the planet in realistic space with physically consistent lighting "
                                    "and atmospheric detail."
                                )
                            },
                            {
                                "type": "input_image",
                                "image_url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        ]
                    }
                ]
            )

        st.success("Done!")
        st.write(response.output)

