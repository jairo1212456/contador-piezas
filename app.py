import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("?? Contador de Pernos y Volandas")
st.write("Sube una foto sobre una superficie clara para contar los objetos.")

foto = st.file_uploader("Sube tu foto aquí", type=["jpg", "png", "jpeg"])

if foto:
    img = np.array(Image.open(foto))
    if len(img.shape) == 3 and img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    
    gris = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    sensibilidad = st.slider("Ajustar sensibilidad (luz/sombras)", 10, 240, 120)
    
    _, umbral = cv2.threshold(cv2.GaussianBlur(gris, (7, 7), 0), sensibilidad, 255, cv2.THRESH_BINARY_INV)
    contornos, _ = cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    objetos = [c for c in contornos if cv2.contourArea(c) > 150]

    resultado = img.copy()
    for i, c in enumerate(objetos):
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(resultado, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.putText(resultado, f"#{i+1}", (x, max(y - 10, 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    st.success(f"?? Total detectado: {len(objetos)} piezas")
    st.image(resultado, use_container_width=True)