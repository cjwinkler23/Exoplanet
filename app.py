import streamlit as st
from openai import OpenAI
import base64
from PIL import Image
import io

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Exoplanet Drawing Enhancer")

uploaded_file = st.file_uploader(
    "Take a photo of your exoplanet drawing",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=False
)

if uploaded_file:
    st.image(uploaded_file, caption="Your input", use_container_width=True)

    if st.button("Generate Hyper-Realistic Version"):

        image_bytes = uploaded_file.read()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        with st.spinner("Generating..."):

            response = client.responses.create(
                model="gpt-4.1-mini",
                input=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": "You are an exoplanet visualization assistant. When a user uploads a hand-drawn exoplanet sketch, create a scientifically plausible, photorealistic exoplanet based on the drawing. Preserve the overall shape, cloud bands, storms, colors, and major features while converting the sketch into a high-resolution space image. Place the planet in realistic space with physically consistent lighting and atmospheric detail."
                            },
                            {
                                "type": "input_image",
                                "image_url": f"data:image/png;base64,{base64_image}"
                            }
                        ]
                    }
                ]
            )

        # Depending on model output, you may need to adjust parsing
        st.write(response.output)

