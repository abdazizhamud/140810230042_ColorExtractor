import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math
from PIL import Image
import color_extractor

st.write("## Color Extractor")
st.write("140810230042 - Hamud Abdul Aziz")
x = st.file_uploader("Masukan foto",accept_multiple_files=False)
n_colors = 0
pic_path = ""
if x:
    n_colors = st.number_input("Masukan jumlahgi output warna!", min_value=3, max_value=10)
    pic_path = "picture/pic1.jpg"
    pic = Image.open(x)
    pic.save(pic_path)
else:
    st.write()

button_start = st.button("Start Extracting")
if button_start and x:
    result = color_extractor.extract_colors(pic_path, n_colors=n_colors)
    
    st.write(f"🎯 Extracted in {result['duration']:.2f} seconds")

    # Show the color palette
    st.image(result["original_image"], caption="Original Image")

    # Palette visualization as bar (optional pretty version)
    import matplotlib.pyplot as plt
    import numpy as np

    palette = result["palette"]

    plt.figure(figsize=(8, 2))
    plt.imshow([palette.astype("uint8")])
    plt.title("Extracted Palette")
    plt.axis('off')
    st.pyplot(plt)

    # Show quanticized image
    st.image(result["quanticized_image"], caption=f"Quantized with {n_colors} colors")