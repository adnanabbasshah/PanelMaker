import streamlit as st
from PIL import Image
import os
import io
import base64
from fpdf import FPDF
import numpy as np

st.set_page_config(page_title="🖼️ Image Panel Maker", layout="wide")

st.sidebar.title("⚙️ Settings")

theme = st.sidebar.radio("Theme", ["Light", "Dark"])
if theme == "Dark":
    st.markdown("""
        <style>
        body {background-color: #1e1e1e; color: white;}
        .stButton>button {background-color: #444; color: white;}
        </style>
    """, unsafe_allow_html=True)

sort_option = st.sidebar.selectbox("Sort Images By", ["Upload Order", "Filename"])
padding = st.sidebar.slider("Panel Padding (px)", 0, 50, 10)
border = st.sidebar.checkbox("Add Image Borders")
corner_radius = st.sidebar.slider("Corner Radius", 0, 30, 5)

export_format = st.sidebar.selectbox("Export Format", ["PNG", "JPG", "PDF"])
resize_images = st.sidebar.checkbox("Resize All Images")
if resize_images:
    target_width = st.sidebar.number_input("Width (px)", 100, 2000, 512)
    target_height = st.sidebar.number_input("Height (px)", 100, 2000, 512)
    lock_aspect = st.sidebar.checkbox("Lock Aspect Ratio")

st.sidebar.markdown("🚧 Save & Share (Coming Soon)")

st.title("🖼️ Image Panel Generator")
st.write("Built by Adnan Abbas Shah")

uploaded_files = st.file_uploader("Upload Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    if sort_option == "Filename":
        uploaded_files = sorted(uploaded_files, key=lambda x: x.name)

    cols = st.columns(4)
    images = []

    for idx, file in enumerate(uploaded_files):
        image = Image.open(file).convert("RGBA")
        if resize_images:
            if lock_aspect:
                image.thumbnail((target_width, target_height))
            else:
                image = image.resize((target_width, target_height))
        if border:
            border_size = 5
            new_img = Image.new("RGBA", (image.width + 2*border_size, image.height + 2*border_size), (0, 0, 0, 0))
            new_img.paste(image, (border_size, border_size))
            image = new_img

        images.append(image)
        cols[idx % 4].image(image, use_container_width=True, caption=file.name)

    if st.button("Generate Panel"):
        widths, heights = zip(*(i.size for i in images))
        total_width = sum(widths) + padding * (len(images) - 1)
        max_height = max(heights)
        panel = Image.new("RGBA", (total_width, max_height), (255, 255, 255, 0))
        x_offset = 0
        for im in images:
            panel.paste(im, (x_offset, (max_height - im.size[1]) // 2))
            x_offset += im.size[0] + padding

        st.image(panel, caption="Final Panel", use_container_width=True)

        buffered = io.BytesIO()
        if export_format == "PNG":
            panel.save(buffered, format="PNG")
            mime = "image/png"
            file_ext = "png"
        elif export_format == "JPG":
            panel.convert("RGB").save(buffered, format="JPEG")
            mime = "image/jpeg"
            file_ext = "jpg"
        else:
            pdf = FPDF()
            panel_rgb = panel.convert("RGB")
            temp_path = "temp_image.jpg"
            panel_rgb.save(temp_path)
            pdf.add_page()
            pdf.image(temp_path, x=10, y=10, w=190)
            pdf.output("panel.pdf")
            with open("panel.pdf", "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                href = f'<a href="data:application/pdf;base64,{b64}" download="panel.pdf">📄 Download PDF</a>'
                st.markdown(href, unsafe_allow_html=True)
            os.remove(temp_path)
            st.stop()

        b64 = base64.b64encode(buffered.getvalue()).decode()
        href = f'<a href="data:{mime};base64,{b64}" download="panel.{file_ext}">💾 Download Panel</a>'
        st.markdown(href, unsafe_allow_html=True)
else:
    st.info("👆 Upload some images to begin.")

st.markdown("""
---
### 👨‍💻 About the Developer  
📧 [syedadnanshahn@yahoo.com](mailto:syedadnanshahn@yahoo.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/adnan-abbas-shah/)  
💻 [GitHub](https://github.com/adnanabbasshah)

<a href="https://github.com/adnanabbasshah" target="_blank">
<img src="https://img.shields.io/github/stars/adnanabbasshah?style=social" alt="GitHub Stars"></a>
""", unsafe_allow_html=True)
