# Python In-built packages
from ultralytics import YOLO
from pathlib import Path
import PIL

from PIL import Image
from PIL import Image, ImageDraw, ImageFont





# External packages
import streamlit as st

# Local Modules
import settings
import helper

# Replace the relative path to your weight file
model_path = 'weights/bestV5.pt'

# Setting page layout
st.set_page_config(
    page_title="OneAMZ SELLER GUIDE",
    page_icon="🤖",
   # layout="wide",
    initial_sidebar_state="expanded"
)


# Main page heading
st.title("PRODUCT CATEGORY FINDER")
st.markdown('Updload a photo, select a video, open webcam or paste a url from Youtube ')
st.markdown('Then click the Detect Product Category button and check the result.')


# Creating sidebar

    ### Adding in the Streamlit and Roboflow logos to the sidebar
image = Image.open("./images/1.jpg") #   one amz  logo ekle
st.sidebar.image(image, use_column_width=True) 
    #st.sidebar. image(image, width=50)

image = Image.open("./images/2.png") #  "./images/oneamz1.png"
st.sidebar.image(image, use_column_width=True)
    #st.sidebar. image(image, width=50)

# Sidebar
st.sidebar.header("Detection Model Tunning")

# Model Options

confidence = float(st.sidebar.slider(
    "Select Model Confidence", 0, 100, 20)) / 100

model_type = st.sidebar.radio(
    "Select Task", ['Detection', 'Segmentation'])

#confidence = float(st.sidebar.slider(
 #   "Select Model Confidence", 0, 100, 40)) / 100

# Selecting Detection Or Classification
if model_type == 'Detection':
     model_path = Path(settings.DETECTION_MODEL)
elif model_type == 'Segmentation':
     model_path = Path(settings.SEGMENTATION_MODEL)

# Selecting Category types
category_type = st.sidebar.radio( 'Choose Category Types',
    ['Root Category', 'Subcategory', 'Sub-Subcategory'])

if category_type == 'Root Category':
     model_path = Path(settings.Root_Category)
elif model_type == 'Subcategory':
     model_path = Path(settings.Subcategory)
elif model_type == 'Sub-Subcategory':
     model_path = Path(settings.Sub_Subcategory)





# Load Pre-trained ML Model
model_path =  'weights/bestV5.pt'

try:
    model = helper.load_model(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)

#st.sidebar.header("Image/Video Config")
source_radio = st.sidebar.radio(
    "Select Source", settings.SOURCES_LIST)

source_img = None
# If image is selected
if source_radio == settings.IMAGE:
    source_img = st.sidebar.file_uploader(
        "Choose a Product Image", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

    col1, col2 = st.columns(2)

    with col1:
        try:
            if source_img:
                uploaded_image = PIL.Image.open(source_img)
                st.image(source_img, caption="Uploaded Image",
                         use_column_width=True)
        except Exception as ex:
            st.error("Error occurred while opening the image.")
            st.error(ex)

    with col2:  
                    
        if st.sidebar.button('Detect Product Category'):
            res = model.predict(uploaded_image,
                                    conf=confidence
                                    )
            boxes = res[0].boxes
            res_plotted = res[0].plot()[:, :, ::-1]
            st.image(res_plotted, caption='Detected Image',
                         use_column_width=True)
            st.balloons()
            try:
                    with st.expander("Detection Results"):
                        for box in boxes:
                            st.write(box.data)
            except Exception as ex:
                    # st.write(ex)
                    st.write("No image is uploaded yet!")
elif source_radio == settings.VIDEO:
    helper.play_stored_video(confidence, model)
    st.balloons()
elif source_radio == settings.WEBCAM:
    helper.play_webcam(confidence, model)
    st.balloons()
elif source_radio == settings.YOUTUBE:
    helper.play_youtube_video(confidence, model)
    st.balloons()
else:
    st.error("Please select a valid source type!")
    st.snow()