import streamlit as x1
import os as x2
from PIL import Image as x3, ImageDraw as x4
import tempfile as x5
from fpdf import FPDF as x6

x1.set_page_config(page_title="🖼️", layout="wide", page_icon="🖼️")

x1.markdown("""<style>footer{visibility:hidden;}header{visibility:hidden;}</style>""", unsafe_allow_html=True)
x1.title("🖼️ Image Panel Maker")
x1.markdown("Create custom image panels with drag-and-drop layout, export options, and more!")

a1 = x1.file_uploader("Upload Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

x2 = x1.sidebar.slider("Cols", 1, 10, 3)
x3_ = x1.sidebar.slider("Pad", 0, 100, 10)
x4_ = x1.sidebar.checkbox("B")
x5_ = x1.sidebar.checkbox("R")
x6_ = x1.sidebar.selectbox("T", ["Light", "Dark"])
x7_ = x1.sidebar.selectbox("F", ["PNG", "JPG", "PDF"])
x8_ = x1.sidebar.checkbox("RS")
x9_ = x1.sidebar.selectbox("D", ["512x512", "256x256", "1024x1024"], index=0)

if x6_ == "Dark":
    x1.markdown("""<style>.main {background-color: #1e1e1e; color: white;}</style>""", unsafe_allow_html=True)

if a1:
    x1.subheader("🔍 Preview")
    a2 = []
    for f in a1:
        z1 = x3.open(f)
        if x8_:
            s = tuple(map(int, x9_.split("x")))
            z1 = z1.resize(s)
        a2.append(z1)

    z2 = x2
    z3 = (len(a2) + z2 - 1) // z2

    for i in range(z3):
        z4 = a2[i*z2:(i+1)*z2]
        z5 = x1.columns(len(z4))
        for j, z6 in enumerate(z4):
            if x5_:
                z6 = z6.convert("RGBA")
                z7 = Image.new('L', z6.size, 0)
                z8 = x4.Draw(z7)
                z8.rounded_rectangle([0, 0, z6.size[0], z6.size[1]], radius=20, fill=255)
                z6.putalpha(z7)
            with z5[j]:
                x1.image(z6, use_container_width=True)

    x1.markdown("---")
    x1.subheader("📤 Export Panel")
    if x1.button("Generate and Download"):
        with x5.TemporaryDirectory() as t:
            o = os.path.join(t, f"panel_output.{x7_.lower()}")

            w, h = zip(*(z.size for z in a2))
            mw = max(w)
            mh = max(h)
            pw = x2 * (mw + x3_)
            ph = z3 * (mh + x3_)
            z9 = x3.new('RGB', (pw, ph), color=(255,255,255))

            for k, z in enumerate(a2):
                r = k // x2
                c = k % x2
                x = c * (mw + x3_)
                y = r * (mh + x3_)
                z9.paste(z, (x, y))

            if x7_.lower() == "pdf":
                p = x6()
                tp = os.path.join(t, "tmp.jpg")
                z9.save(tp)
                p.add_page()
                p.image(tp, x=10, y=10, w=190)
                p.output(o)
            else:
                z9.save(o)

            with open(o, "rb") as q:
                x1.download_button(f"Download Panel ({x7_})", q, file_name=f"image_panel.{x7_.lower()}")

x1.markdown("""
---
### 👨‍💻 About the Developer
📧 [syedadnanshahn@yahoo.com](mailto:syedadnanshahn@yahoo.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/adnan-abbas-shah/)  
💻 [GitHub](https://github.com/adnanabbasshah)  

<a href="https://github.com/adnanabbasshah" target="_blank">
<img src="https://img.shields.io/github/stars/adnanabbasshah?style=social" alt="GitHub Stars"></a>

<small>© 2025 Adnan Abbas Shah – All rights reserved.</small>
""", unsafe_allow_html=True)
