import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
from  PIL import Image, ImageEnhance

logo = Image.open('data/logo.jpg') #Brand logo image (optional)
st.image(logo,  width=300)
st.title('Hair Counting System for the Quantitative Evaluation of Laser Hair Removal')


uploaded_file = st.file_uploader("", type=['jpg','png','jpeg'])

#Add 'before' and 'after' columns
if uploaded_file is not None:
    image = Image.open(uploaded_file)

    col1, col2 = st.columns( [0.5, 0.5])

    with col1:
        st.markdown('<p style="text-align: center;">Before</p>',unsafe_allow_html=True)
        st.image(image,width=300)

    with col2:
        st.markdown('<p style="text-align: center;">After</p>',unsafe_allow_html=True)
        converted_img = np.array(image.convert('RGB'))
        gray = cv2.cvtColor(converted_img , cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(13,13),0)
        canny = cv2.Canny(blur, 20, 30,3)
        dilated = cv2.dilate(canny, (1,1), iterations=2)
        (cnt, heirarchy) = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        rgb = cv2.cvtColor(converted_img, cv2.COLOR_BGR2RGB)
        cv2.drawContours(rgb, cnt, -1,(0,255,0),2)
        count = len(cnt)
        st.image(rgb, width=300)


    count_str = f"""
                <style>
                p.a {{
                font: bold 35px sans-serif;
                }}
                </style>
                <p class="a">Hairs in image: {count}</p>
                """



    st.markdown(count_str, unsafe_allow_html=True)
