

import streamlit as st
from textblob import TextBlob
import pandas as pd

# Load the data from the Excel file
df2 = pd.read_csv("english_texts.csv")

st.markdown(
    """
    <style>
        .title {
            font-size: 72px;
            font-weight: bold;
            color: yellow;
        }
        .subtitle {
            font-size: 72px;
            font-weight: bold;
            color: black;
        }
        .stButton > button {
                        color: black;
                        border: 3px solid yellow;
                        font-size: 18px;         /* Adjust this value to your liking */
                        padding: 10px 20px;      /* Adjust padding values for top/bottom and left/right respectively */
                        width: auto;             /* Optionally set a fixed width if needed */
                        height: auto;            /* Optionally set a fixed height if needed */
                    }

        .big-title {
            font-size: 28px;  # Adjust size as needed
        }
    </style>
    """, unsafe_allow_html=True
)

st.markdown(
    """
    <span class="title">One</span><span class="subtitle">AMZ</span>
    """, unsafe_allow_html=True
)

st.markdown('<p class="big-title">Duygu Analizi</p>', unsafe_allow_html=True)

# Dropdown to choose text
selected_text = st.selectbox("**OneAMZ yorumlarından bir tane seçin**", df2['english_texts'].tolist())
user_input = st.text_area("**Lütfen bir tane yorum yazın**", selected_text)


if st.button('ANALİZ'):
    blob = TextBlob(user_input)
    sentiment_polarity = blob.sentiment.polarity
    if -0.05 < sentiment_polarity < 0.05:
        result = 'Neutral'
    elif sentiment_polarity > 0:
        result = 'Positive'
    else:
        result = 'Negative'
    st.write(f"The sentiment is: **{result}**")
