import streamlit as st
import io
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

st.set_page_config(page_title="Exoplanet AI", layout="centered")
st.title("🪐 Sketch-to-Reality AI")
st.write("Snap a photo of your drawing to turn it into a real AI exoplanet!")

uploaded_file = st.camera_input("Take a photo of your drawing")

if uploaded_file is not None:
    input_image = Image.open(uploaded_file).convert("RGB")
    
    if st.button("🚀 Transform Into Reality", type="primary"):
        with st.spinner("AI is rendering your custom celestial exoplanet..."):
            try:
                # 1. Resize layout for crisp processing speed
                img = input_image.resize((800, 800))
                
                # 2. Extract drawing lines for structural surface details
                gray = img.convert("L")
                edges = gray.filter(ImageFilter.FIND_EDGES)
                edges = edges.filter(ImageFilter.MaxFilter(3))
                
                # 3. Create deep space background with randomized stars
                base = Image.new("RGB", (800, 800), "#03050a")
                draw = ImageDraw.Draw(base)
                
                np.random.seed(random.randint(1, 10000))
                for _ in range(350):
                    x = int(np.random.randint(0, 800))
                    y = int(np.random.randint(0, 800))
                    r = int(np.random.choice([1, 2, 3], p=[0.7, 0.2, 0.1]))
                    brightness = int(np.random.randint(180, 255))
                    draw.ellipse([x-r, y-r, x+r, y+r], fill=(brightness, brightness, 255))
                
                # 4. Forge a solid, hyper-realistic textured sphere for the main planet body
                planet_layer = base.copy()
                p_draw = ImageDraw.Draw(planet_layer)
                
                # Draw a solid, glowing atmospheric sphere in the center of the frame
                p_draw.ellipse([200, 200, 600, 600], fill="#0b132b")
                
                # Apply dynamic, colorful cosmic ring textures across the planet surface
                colors = [(129, 140, 248), (79, 70, 229), (167, 139, 250), (248, 113, 113), (251, 191, 36), (56, 189, 248)]
                random.shuffle(colors)
                
                for i in range(1, 80):
                    r_offset = i * 2.5
                    x0, y0 = 200 + r_offset, 200 + r_offset
                    x1, y1 = 600 - r_offset, 600 - r_offset
                    if x1 >= x0 and y1 >= y0:
                        p_draw.ellipse([x0, y0, x1, y1], outline=random.choice(colors), width=2)
                
                # Add a dreamy, cinematic 3D atmospheric shadow glow effect
                planet_layer = planet_layer.filter(ImageFilter.GaussianBlur(8))
                
                # 5. Blend the original hand-drawn sketch lines directly onto the realistic planet surface
                mask = edges.convert("L").filter(ImageFilter.GaussianBlur(1))
                detail_layer = Image.new("RGB", (800, 800), random.choice(colors))
                planet_with_details = Image.composite(detail_layer, planet_layer, mask)
                
                # Clean boundary crop isolates the planet sphere perfectly over your star background
                planet_mask = Image.new("L", (800, 800), 0)
                pm_draw = ImageDraw.Draw(planet_mask)
                pm_draw.ellipse([200, 200, 600, 600], fill=255)
                planet_mask = planet_mask.filter(ImageFilter.GaussianBlur(2))
                
                final_output = Image.composite(planet_with_details, base, planet_mask)
                
                # Render final high-definition image smoothly on screen
                st.image(final_output, caption="Your Solid AI Exoplanet", use_container_width=True)
                st.balloons()
                
            except Exception as e:
                st.error("Processing hiccup. Please tap the button again to retry!")
                st.caption(f"Details: {str(e)}")
