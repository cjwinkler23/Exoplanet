import streamlit as st
from openai import OpenAI
import base64
from PIL import Image
import io

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Exoplanet Drawing Enhancer")

uploaded_file = st.file_uploader("Upload your exoplanet drawing", type=["png", "jpg", "jpeg"])

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
                                "text": "Transform this exoplanet drawing into a hyper-realistic cinematic astrophysical scene. Keep structure but enhance realism, lighting, and atmosphere."
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

