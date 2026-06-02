import streamlit as st
import io
import base64
import requests
import random
from PIL import Image

st.set_page_config(page_title="Exoplanet AI", layout="centered")
st.title("🪐 Sketch-to-Reality AI")
st.write("Snap a photo of your drawing to turn it into a real AI exoplanet!")

uploaded_file = st.camera_input("Take a photo of your drawing")

if uploaded_file is not None:
    # Compress photo locally inside memory so it handles perfectly on mobile networks
    drawing_image = Image.open(uploaded_file).convert("RGB")
    drawing_image.thumbnail((512, 512))
    
    img_byte_arr = io.BytesIO()
    drawing_image.save(img_byte_arr, format='JPEG', quality=75)
    img_bytes = img_byte_arr.getvalue()

    if st.button("🚀 Transform Into Reality", type="primary"):
        with st.spinner("Decentralized AI is rendering your sketch shapes..."):
            try:
                # Convert drawing bytes into standard text string for the processing server payload
                base64_image = base64.b64encode(img_bytes).decode('utf-8')
                
                # Public stable endpoint for instant crowdsourced transformations
                api_url = "https://stablehorde.net"
                
                # Payload designed to force the AI to follow your drawing shapes and colors
                payload = {
                    "prompt": "Hyper-realistic stunning 8k cinematic space photography masterpiece of a celestial exoplanet, highly detailed texture, glowing cosmic atmosphere, sci-fi scene, star nebula background ### drawing, sketch, lines, cartoon, text, words, bad anatomy, blurry",
                    "params": {
                        "cfg_scale": 7.5,
                        "width": 512,
                        "height": 512,
                        "steps": 20,
                        "seed": random.randint(1, 9999999),
                        "source_image": base64_image,
                        "source_processing": "img2img",
                        "denoising_strength": 0.6 # 0.6 forces the AI to strictly keep your drawing layout
                    }
                }
                
                # Free public access header
                headers = {"apikey": "0000000000", "Client-Agent": "exoplanetapp:1.0:streamlit"}
                
                # 1. Submit the image transformation job
                response = requests.post(api_url, json=payload, headers=headers, timeout=30)
                
                if response.status_code == 202:
                    id_data = response.json()
                    id_code = id_data["id"]
                    
                    # 2. Check the cluster loop until the image is painted
                    check_url = f"https://stablehorde.net{id_code}"
                    
                    # Quick short delay loop to wait for processing to finish
                    import time
                    for _ in range(10):
                        time.sleep(2)
                        status_response = requests.get(check_url, timeout=20)
                        status_data = status_response.json()
                        
                        if status_data.get("done") == True:
                            # 3. Pull the finished image out of the data payload
                            img_url = status_data["generations"][0]["img"]
                            final_response = requests.get(img_url)
                            result_img = Image.open(io.BytesIO(final_response.content))
                            
                            st.image(result_img, caption="Your AI Generated Exoplanet", use_container_width=True)
                            st.balloons()
                            break
                    else:
                        st.error("The network is congested. Please tap the button once more to submit!")
                else:
                    st.error("The grid node is re-routing. Please tap the button again!")
                    
            except Exception as e:
                st.error("Connection hiccup. Please tap the button again to retry!")
                st.caption(f"Details: {str(e)}")
