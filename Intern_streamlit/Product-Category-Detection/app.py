# Import required libraries
import PIL
from pathlib import Path
from PIL import Image
from PIL import Image, ImageDraw, ImageFont


import streamlit as st
from ultralytics import YOLO

# Replace the relative path to your weight file
model_path = 'weights/bestV5.pt'

# Setting page layout
#st.set_page_config(

    
st.title("Product Category Finder")
st.subheader('Image Detection Side ')

#st.subheader('Thisis a subheader')
#st.text('Thi sis a header')

# Creating sidebar

    ### Adding in the Streamlit and Roboflow logos to the sidebar
image = Image.open("./images/1.jpg") #   one amz  logo ekle
st.sidebar.image(image, use_column_width=True) 
    #st.sidebar. image(image, width=50)

image = Image.open("./images/2.png") #  "./images/oneamz1.png"
st.sidebar.image(image, use_column_width=True)
    #st.sidebar. image(image, width=50)

st.sidebar.write("### Image Tunning")

    # Adding file uploader to sidebar for selecting images

source_img = st.file_uploader(
        "Upload an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

    # Model Options
confidence = float(st.sidebar.slider(
        "Select Model Confidence", 0, 100, 40)) / 100

#st.sidebar.write("### Select Analysis Type")
status = st.sidebar.radio("Select Analysis Type", ( "Image Detection "," Realtime Detection "))

options = st.sidebar.multiselect( 'Choose Category Type',
    ['Root Category', 'Subcategory', 'Sub-Subcategory'])


# Creating main page heading
#st.title("Object Detection")
#st.caption('Updload a photo with this :blue[hand signals]: :+1:, :hand:, :i_love_you_hand_sign:, and :spock-hand:.')
#st.markdown('Then click the :blue[Detect Objects] button and check the result.')
#st.markdown(":red[Para los instructores de Codigo Facilito este es el link de mi proyecto final le agregue cosas --->] [Object detection video and Webcam](https://objectdetectionwebcam.streamlit.app/)")
#st.markdown(":red[Lean mi blog por fa --->] [Object detection blog](https://lalodatos.medium.com/building-your-own-real-time-object-detection-app-roboflow-yolov8-and-streamlit-part-1-f577cf0aa6e5)")

# Creating two columns on the main page
col1, col2 = st.columns(2)

# Adding image to the first column if image is uploaded
with col1:
    if source_img:
        # Opening the uploaded image
        uploaded_image = PIL.Image.open(source_img)
        # Adding the uploaded image to the page with a caption
        st.image(source_img,
                 caption="Uploaded Image",
                 use_column_width=True
                 )

try:
    model = YOLO(model_path)
except Exception as ex:
    st.error(
        f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)

if st.button('Detect Objects'):
    res = model.predict(uploaded_image,
                        conf=confidence
                        )
    boxes = res[0].boxes
    res_plotted = res[0].plot()[:, :, ::-1]
    with col2:
        st.image(res_plotted,
                 caption='Detected Image',
                 use_column_width=True
                 )
        st.balloons()
        try:
           with st.expander("Detection Results"):
               for box in boxes:
                   st.write(box.xywh)    
        except Exception as ex:
               st.write("No image is uploaded yet!")