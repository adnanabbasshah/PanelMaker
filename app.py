import streamlit as st
from PIL import Image
import os
import io
from zipfile import ZipFile

st.set_page_config(page_title="Image Panel Maker", layout="centered", page_icon="🖼️", initial_sidebar_state="expanded")

st.markdown(
    "<h1 style='text-align: center;'>🖼️ Image Panel Maker</h1>"
    "<h4 style='text-align: center;'>Designed by Adnan Abbas Shah (GIS Developer)</h4>",
    unsafe_allow_html=True
)

# --- Sidebar Controls ---
st.sidebar.header("🔧 Panel Settings")
rows = st.sidebar.number_input("Rows", min_value=1, value=2, step=1)
cols = st.sidebar.number_input("Columns", min_value=1, value=2, step=1)

# --- File Upload ---
uploaded_files = st.file_uploader("Upload JPG/PNG images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# --- Image Panel Generation ---
if uploaded_files and st.button("🧩 Generate Panel"):
    images = [Image.open(file).convert("RGB") for file in uploaded_files]

    if len(images) != rows * cols:
        st.error(f"Please upload exactly {rows * cols} images for a {rows}×{cols} panel.")
    else:
        # Resize all images to match the first one
        base_width, base_height = images[0].size
        resized_images = [img.resize((base_width, base_height)) for img in images]

        # Create blank panel
        panel = Image.new("RGB", (cols * base_width, rows * base_height))

        # Paste images
        for idx, img in enumerate(resized_images):
            x = (idx % cols) * base_width
            y = (idx // cols) * base_height
            panel.paste(img, (x, y))

        st.image(panel, caption="Generated Panel", use_column_width=True)

        # Save to BytesIO and let user download
        buffer = io.BytesIO()
        panel.save(buffer, format="PNG")
        buffer.seek(0)
        st.download_button("⬇️ Download Panel", buffer, file_name="image_panel.png", mime="image/png")

---

