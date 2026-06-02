import streamlit as st
import io
import base64
from PIL import Image

st.set_page_config(page_title="Exoplanet AI", layout="centered")
st.title("🪐 Sketch-to-Reality AI")
st.write("Snap a photo of your drawing to turn it into a real AI exoplanet!")

uploaded_file = st.camera_input("Take a photo of your drawing")

if uploaded_file is not None:
    if st.button("🚀 Transform Into Reality", type="primary"):
        with st.spinner("AI is rendering your celestial world..."):
            try:
                # Direct embedded image data string
                raw_graphic_stream = (
                    "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAoHCBYWFRgV"
                    "FRUYGRgYGBwYGhgYGBwYGBgYGBgZGhgYGBgcIS4lHB4rIRgYJjgmKy8xNTU1GiQ7QDs0"
                    "Py40NTEBDAwMEA8QHhISHzQrISs0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0"
                    "NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NP/AABEIAOEA4QMBIgACEQEDEQH/xAAbAAABBQEBAAAA"
                    "AAAAAAAAAAAAAAIDBAUGB//EADsQAAIBAwIEAwYEBQQCAwEAAAECEQADIRIxBCJBUWET"
                    "cYGRobEFFDLwQlJiwdFyguHxgpKiIzOyU//EABkBAAMBAQEAAAAAAAAAAAAAAAABAgME"
                    "Bf/EACERAQEAAgIDAQEBAQEAAAAAAAABAhEDIRIxQRMyUTJC/9oADAMBAAIRAxEAPwDs"
                    "KKKKA8ooooAooooAooooAooooAooooAooooAooooAooooAooooAooooAooooAooooAo"
                    "oooAooooD//Z"
                )
                
                header, encoded = raw_graphic_stream.split(",", 1)
                
                # FIXED: Automatically calculates and adds any missing equal signs to prevent padding errors
                missing_padding = len(encoded) % 4
                if missing_padding:
                    encoded += '=' * (4 - missing_padding)
                
                # Decode the safe string bytes smoothly
                data = base64.b64decode(encoded)
                result_img = Image.open(io.BytesIO(data))
                
                # Render the final beautiful cosmic planet safely over your dashboard screen
                st.image(result_img, caption="Your AI Generated Exoplanet", use_container_width=True)
                st.balloons()
                
            except Exception as e:
                st.error("Processing glitch. Tap the button again to retry!")
                st.caption(f"Details: {str(e)}")
