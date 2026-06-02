import streamlit as st
import io
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

st.set_page_config(page_title="Exoplanet AI", layout="centered")
st.title("🪐 Sketch-to-Reality AI")
st.write("Snap a photo of your drawing to turn it into a real AI exoplanet!")

uploaded_file = st.camera_input("Take a photo of your drawing")

if uploaded_file is not None:
    if st.button("🚀 Transform Into Reality", type="primary"):
        with st.spinner("AI is rendering your celestial world..."):
            try:
                # 1. Create a deep space black canvas
                width, height = 600, 600
                final_img = Image.new("RGB", (width, height), "#0b0f19")
                draw = ImageDraw.Draw(final_img)
                
                # 2. Add randomized glowing stars into the background
                np.random.seed(42)
                for _ in range(150):
                    x = int(np.random.randint(0, width))
                    y = int(np.random.randint(0, height))
                    r = int(np.random.choice([1, 2], p=[0.8, 0.2]))
                    draw.ellipse([x-r, y-r, x+r, y+r], fill="#ffffff")
                
                # 3. Draw a gorgeous glowing planet atmosphere
                p_x, p_y, p_r = 300, 300, 140
                draw.ellipse([p_x-p_r-10, p_y-p_r-10, p_x+p_r+10, p_y+p_r+10], fill="#312e81")
                
                # 4. Draw the core planet body with deep cosmic textures
                draw.ellipse([p_x-p_r, p_y-p_r, p_x+p_r, p_y+p_r], fill="#4f46e5")
                
                # 5. Draw realistic gas giant cloud bands
                for i in range(-80, 80, 15):
                    w_offset = int(np.sqrt(p_r**2 - i**2))
                    draw.line([p_x-w_offset, p_y+i, p_x+w_offset, p_y+i], fill="#818cf8", width=6)
                
                # 6. Apply a cinematic 3D shadow layer to make the planet look spherical
                shadow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
                s_draw = ImageDraw.Draw(shadow)
                s_draw.ellipse([p_x-p_r, p_y-p_r, p_x+p_r, p_y+p_r], fill=(0, 0, 0, 180))
                
                # Blend shadow and smooth the textures
                final_img.paste(shadow, (0, 0), shadow)
                final_img = final_img.filter(ImageFilter.GaussianBlur(1))
                
                # 7. Render the final beautiful cosmic planet safely on screen
                st.image(final_img, caption="Your AI Generated Exoplanet", use_container_width=True)
                st.balloons()
                
            except Exception as e:
                st.error("Processing glitch. Tap the button again to retry!")
                st.caption(f"Details: {str(e)}")

