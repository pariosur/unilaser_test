import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
from  PIL import Image, ImageEnhance

st.title('Unilaser Hair Counter')


image = Image.open('data/logo.jpg') #Brand logo image (optional)

#Create two columns with different width
col1, col2 = st.columns( [0.8, 0.2])
with col1:               # To display the header text using css style
    st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;}
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Upload your photo here...</p>', unsafe_allow_html=True)

with col2:               # To display brand logo
    st.image(image,  width=150)

#Add a header and expander in side bar
st.sidebar.markdown('<p class="font">My First Photo Converter App</p>', unsafe_allow_html=True)
with st.sidebar.expander("About the App"):
     st.write("""
        Use this simple app to convert your favorite photo to a pencil sketch, a grayscale image or an image with blurring effect.  \n  \nThis app was created by Sharone Li as a side project to learn Streamlit and computer vision. Hope you enjoy!
     """)


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
        gray = cv2.cvtColor(converted_img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(15,15),0)
        canny = cv2.Canny(blur, 20, 20,3)
        dilated = cv2.dilate(canny, (1,1), iterations=2)
        (cnt, heirarchy) = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        rgb = cv2.cvtColor(converted_img, cv2.COLOR_BGR2RGB)
        cv2.drawContours(rgb, cnt, -1,(0,255,0),2)
        count = len(cnt)
        st.image(rgb, width=300)

        count_str = f'Hairs in image: {count}'
        st.markdown(count_str, unsafe_allow_html=True)


        # return f'Hairs in image: {count}'
