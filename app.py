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
        with st.spinner("AI is analyzing your sketch shapes..."):
            try:
                token = st.secrets["HF_TOKEN"]
                client = InferenceClient(api_key=token)
                
                base64_image = base64.b64encode(img_bytes).decode('utf-8')
                image_url = f"data:image/jpeg;base64,{base64_image}"
                
                messages = [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Look closely at the composition layout, lines, and shapes in this planet drawing. Write a 1-sentence description detailing what a hyper-realistic, 8k cinematic space photography masterpiece version of this exact layout would look like. Describe the placement of the planet, rings, and surface features exactly as drawn. Output ONLY the description sentence."},
                            {"type": "image_url", "image_url": {"url": image_url}}
                        ]
                    }
                ]
                
                # FIXED: Changed client.chat.completion to client.chat_completion
                chat_completion = client.chat_completion(
                    model="Qwen/Qwen2.5-VL-7B-Instruct",
                    messages=messages,
                    max_tokens=100
                )
                
                analyzed_prompt = chat_completion.choices[0].message.content
                
                output_image = client.text_to_image(
                    prompt=f"{analyzed_prompt.strip()}, stunning photorealistic celestial exoplanet, highly detailed texture, epic deep space stars background, masterpiece sci-fi movie scene",
                    negative_prompt="cartoon, drawing, sketch, writing, words, text, lines, notebook paper, bad composition, blurry, low quality",
                    model="stabilityai/stable-diffusion-xl-base-1.0"
                )
                
                st.image(output_image, caption="Your Reimagined AI Exoplanet", use_container_width=True)
                st.balloons()
                
            except Exception as e:
                st.error("The network connection timed out. Please tap the button once more to generate!")
                st.caption(f"Details: {str(e)}")

