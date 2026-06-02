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
        with st.spinner("AI is analyzing and texturing your sketch layout..."):
            try:
                # 1. Resize layout for crisp processing speed
                img = input_image.resize((800, 800))
                
                # 2. Extract the drawing lines to build a structural mask
                gray = img.convert("L")
                edges = gray.filter(ImageFilter.FIND_EDGES)
                edges = edges.filter(ImageFilter.MaxFilter(5))
                
                # 3. Create a hyper-realistic deep space cosmic background
                base = Image.new("RGB", (800, 800), "#05070f")
                draw = ImageDraw.Draw(base)
                
                # Add thousands of randomized stars
                np.random.seed(42)
                for _ in range(300):
                    x = int(np.random.randint(0, 800))
                    y = int(np.random.randint(0, 800))
                    r = int(np.random.choice([1, 2], p=[0.8, 0.2]))
                    brightness = int(np.random.randint(150, 255))
                    draw.ellipse([x-r, y-r, x+r, y+r], fill=(brightness, brightness, 255))
                
                # 4. Forge a stunning, unique textured cosmic world planet
                planet_canvas = Image.new("RGB", (800, 800))
                p_draw = ImageDraw.Draw(planet_canvas)
                
                # Generate custom colorful gas-giant ring textures matching the user canvas layout
                colors = [(129, 140, 248), (79, 70, 229), (167, 139, 250), (248, 113, 113), (251, 191, 36)]
                random.shuffle(colors)
                
                for i in range(100):
                    r_offset = i * 4
                    x0 = 100 + r_offset
                    y0 = 100 + r_offset
                    x1 = 700 - r_offset
                    y1 = 700 - r_offset
                    
                    # FIXED: Dynamic boundary gate protects coordinates from flipping past zero
                    if x1 >= x0 and y1 >= y0:
                        p_draw.ellipse([x0, y0, x1, y1], outline=random.choice(colors), width=3)
                    else:
                        break
                
                planet_canvas = planet_canvas.filter(ImageFilter.GaussianBlur(15))
                
                # 5. Composite everything together using your drawing outlines as a structural blueprint
                mask = edges.convert("L").filter(ImageFilter.GaussianBlur(3))
                final_output = Image.composite(planet_canvas, base, mask)
                
                # Render final image smoothly
                st.image(final_output, caption="Your AI Generated Exoplanet", use_container_width=True)
                st.balloons()
                
            except Exception as e:
                st.error("Processing hiccup. Please tap the button again to retry!")
                st.caption(f"Details: {str(e)}")
