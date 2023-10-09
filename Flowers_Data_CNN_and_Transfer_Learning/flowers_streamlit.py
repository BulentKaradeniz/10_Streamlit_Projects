import streamlit as st
import tensorflow as tf
from PIL import Image
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import requests
from io import BytesIO
st.markdown(
    """
    <style>
    .stApp {
        background-color: #83e627;  /* Koyu sarı renk */
    </style>
    """,
    unsafe_allow_html=True
)
# Streamlit uygulamasını başlat
st.markdown('<div style="display: flex; justify-content: flex-end; margin-top:-70px"><img src="https://i.pinimg.com/originals/4a/73/1f/4a731f6a5480f6ee8b9bfb34168c333b.gif" alt="GIF" width="100%" style="max-width: 400px; margin-right: 160px;"></div>', unsafe_allow_html=True)
st.markdown('<p style="background-color: #8a4baf; color: white; font-size: 30px; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0px 6px 8px rgba(0, 0, 0, 0.1);">🌻Çiçek Tahmin Uygulaması🌻</p>', unsafe_allow_html=True)
st.markdown('<p style="background-color: #8a4baf; color: white; font-size: 20px; padding: 10px; border-radius: 5px; text-align: center; box-shadow: 0px 2px 3px rgba(0, 0, 0, 0.1);">💐Çiçek Türleri💐</p>', unsafe_allow_html=True)
#st.image("turler.png", use_column_width=True)
#st.write("Çiçek Türleri: Daisy, Dandelion, Rose, Sunflower, Tulip")
flower_types = ["Daisy", "Dandelion", "Rose", "Sunflower", "Tulip"]
flower_colors = ["red", "green", "blue", "orange", "purple"]

# Her bir çiçek türünü yan yana bir kutucuk içinde göster
#st.markdown('<p style="text-align: center;">Çiçek Türleri</p>', unsafe_allow_html=True)
flower_divs = []

for i, flower in enumerate(flower_types):
    flower_divs.append(
        f'<div style="background-color: {flower_colors[i]}; color: white; font-size: 16px; padding: 10px; border-radius: 5px; text-align: center; margin-right: 10px; display: inline-block;">{flower}</div>'
    )

st.write(" ".join(flower_divs), unsafe_allow_html=True)

# Kullanıcıdan resim yükleme yöntemini seçmesini isteyin
st.sidebar.title("Resim Yükleme Yöntemi")
upload_method = st.sidebar.radio("Lütfen bir model seçin:", ["Bilgisayarınızdan Yükle", "İnternet Bağlantısı ile Yükle"])

uploaded_image = None  # Kullanıcının yüklediği resmi saklamak için

if upload_method == "Bilgisayarınızdan Yükle":
    # Kullanıcıdan resim yükleme
    #st.write("Lütfen bir çiçek resmi yükleyin:")
    uploaded_image = st.file_uploader("Lütfen bir çiçek resmi yükleyin:", type=["jpg", "png", "jpeg"])
elif upload_method == "İnternet Bağlantısı ile Yükle":
    # Kullanıcıdan internet linki alın
    st.write("Lütfen bir çiçek resmi internet linkini girin:")
    image_url = st.text_input("Resim Linki")

# Model seçimi
st.sidebar.title("Model Seçimi")
selected_model = st.sidebar.radio("Lütfen bir model seçin:", ["CNN_model", "VGG16_model", "ResNet_model", "Xception_model", "NASNetMobile_model"])


# Resmi yükle ve tahmin et butonları
if uploaded_image is not None or (upload_method == "İnternet Bağlantısı ile Yükle" and image_url):
    st.markdown('<p style="background-color: #8a4baf; color: white; font-size: 20px; padding: 10px; border-radius: 5px; text-align: center; box-shadow: 0px 2px 3px rgba(0, 0, 0, 0.1);">🌼Seçtiğiniz Resim🌼</p>', unsafe_allow_html=True)
    #st.write("Seçtiğiniz Resim")
    if uploaded_image is not None:
        st.image(uploaded_image, caption='', use_column_width=True)
    elif upload_method == "İnternet Bağlantısı ile Yükle" and image_url:
        try:
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            st.image(image, caption='', use_column_width=True)
        except Exception as e:
            st.error("Resim yüklenirken bir hata oluştu. Lütfen geçerli bir internet linki girin.")

# Model bilgisi düğmesi
if st.sidebar.button("Model Hakkında Bilgi"):
    st.markdown(f'<p style="background-color: #8a4baf; color: white; font-size: 20px; padding: 10px; border-radius: 5px; text-align: center; box-shadow: 0px 2px 3px rgba(0, 0, 0, 0.1);">🌷{selected_model}🌷</p>', unsafe_allow_html=True)

    if selected_model == "CNN_model":
        st.write("CNN_model, temel bir Evrişimli Sinir Ağı (CNN) modelidir. Evrişimli katmanlar, pooling katmanları ve tam bağlantılı katmanlar içerir. Genellikle temel görsel sınıflandırma görevleri için kullanılır.")
    elif selected_model == "VGG16_model":
        st.write("VGG16_model, 16 katmanlı bir derin Evrişimli Sinir Ağı modelidir. Ardışık olarak evrişimli ve pooling katmanları içerir. Görsel sınıflandırma ve nesne tanıma gibi görevler için kullanılır.")
    elif selected_model == "ResNet_model":
        st.write("ResNet_model, derin ağları eğitmeyi kolaylaştırmak için 'residual' blokları kullanan bir derin Evrişimli Sinir Ağı modelidir. Derin ağların eğitimini iyileştirmek için kullanılır.")
    elif selected_model == "Xception_model":
        st.write("Xception Modeli: Xception, evrişimli sinir ağı mimarisini temelden değiştiren bir modeldir. Etkili bir şekilde özellik çıkartır ve sınıflandırma görevleri için kullanılabilir.")
    elif selected_model == "NASNetMobile_model":
        st.write("NASNetMobile Modeli: NASNetMobile, otomatik mimari arama ile geliştirilen ve özellikle hafif ve mobil cihazlar için optimize edilmiş bir modeldir. Mobil uygulamalar ve taşınabilir cihazlar için transfer öğrenme amacıyla kullanılabilir.")
   
                
# Tahmin yap butonu
if st.button("Tahmin Et"):
    if upload_method == "Bilgisayarınızdan Yükle" and uploaded_image is not None:
        image = Image.open(uploaded_image)
    elif upload_method == "İnternet Bağlantısı ile Yükle" and image_url:
        try:
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
        except Exception as e:
            st.error("Resim yüklenirken bir hata oluştu. Lütfen geçerli bir internet linki girin.")

    # Kullanıcının seçtiği modele göre modeli yükle
    if selected_model == "CNN_model":
        model_path = 'CNN_model.h5'
    elif selected_model == "VGG16_model":
        model_path = 'VGG16.h5'
    elif selected_model == "ResNet_model":
        model_path = 'Resnet50.h5'
    elif selected_model == "Xception_model":
        model_path = 'Xception.h5'
    elif selected_model == "NASNetMobile_model":
        model_path = 'NASNetMobile.h5'

    # Seçilen modeli yükle
    model = tf.keras.models.load_model(model_path, compile=False)   # , compile=False

    # Resmi model için hazırla ve tahmin yap
    if 'image' in locals():
        image = image.resize((224, 224))
        image = tf.keras.preprocessing.image.img_to_array(image)
        image = image / 255.0
        image = np.expand_dims(image, axis=0)

        # Tahmin yap
        prediction = model.predict(image)

        # Tahmin sonuçlarını göster
        class_names = ["Daisy", "Dandelion", "Rose", "Sunflower", "Tulip"]  # Modelin tahmin sınıfları
        predicted_class = class_names[np.argmax(prediction)]
        confidence = np.max(prediction)
        
        st.markdown(f'<p style="background-color: #8a4baf; color: white; font-size: 20px; padding: 10px; border-radius: 5px; text-align: center; box-shadow: 0px 2px 3px rgba(0, 0, 0, 0.1);">🌷Model Tahmini🌷</p>', unsafe_allow_html=True)

        st.write(f"Tahmin Sonucu: {predicted_class}")
        st.write(f"Tahmin Güveni: {confidence:.2f}")
        
        st.markdown('<p style="background-color: #8a4baf; color: white; font-size: 20px; padding: 10px; border-radius: 5px; text-align: center; box-shadow: 0px 2px 3px rgba(0, 0, 0, 0.1);">📊 Tahmin Olasılıkları 📊</p>', unsafe_allow_html=True)
        prediction_df = pd.DataFrame({'Çiçek Türleri': class_names, 'Olasılıklar': prediction[0]})
        st.bar_chart(prediction_df.set_index('Çiçek Türleri'))
