import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from prophet import Prophet

st.markdown(
    """
    <style>
    .stApp {
        background-color: #fff300;  /* Koyu sarı renk */
    }
    .centered-title {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

df_Order = pd.read_csv("Ortak_Order.csv")
df_Ekoz = pd.read_csv("EKOZ_new.csv")

# Streamlit arayüzünü oluşturma

#selected_tab = st.sidebar.selectbox("Sayfa Seçiniz:", ["Mevcut Gelir Durumu", "Gelecek Gelir Tahmini"])
st.sidebar.image("logo-black.png", use_column_width=True, caption="Amazon Danışmanlık")
selected_tab = st.sidebar.radio("Sayfa Seçiniz:", ["Mevcut Gelir Durumu", "Gelecek Gelir Tahmini", "Gelecek Karlılık Tahmini"])

if selected_tab == "Mevcut Gelir Durumu":

    st.markdown('<p style="background-color: #1f191f; color: white; font-size: 20px; padding: 10px; border-radius: 5px; text-align: center; box-shadow: 0px 2px 3px rgba(0, 0, 0, 0.1);">Mağazaların Toplam Gelir Dağılımı</p>', unsafe_allow_html=True)

    country_orders = df_Order.groupby("ship-country")["item-price"].sum()
    # Seaborn ile bar grafiği oluşturma
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x=country_orders.index, y=country_orders.values)
    for container in ax.containers:
        ax.bar_label(container, label_type='edge', labels=[f"${height:.2f}" for height in container.datavalues])

    # Eksen etiketleri ve başlık ekleme
    plt.xlabel("Country")
    plt.ylabel("Total Order Amount")
    plt.title("Mağazaların Toplam Sipariş Gelirleri")

    # X eksenini özelleştirme
    custom_labels = ["OZM Canada","EKOZ Japan", "OZM Mexico"]
    plt.xticks(range(len(custom_labels)), custom_labels, rotation=45, fontsize=14)
    plt.grid(True)
    st.pyplot(plt)



    st.markdown('<p style="background-color: #1f191f; color: white; font-size: 20px; padding: 10px; border-radius: 5px; text-align: center; box-shadow: 0px 2px 3px rgba(0, 0, 0, 0.1);">Günlere Göre Gelir Dağılımı</p>', unsafe_allow_html=True)

    df_Order["days"] = pd.to_datetime(df_Order['purchase-date']).dt.day_name()
    daily_orders = df_Order.groupby("days")["item-price"].sum()
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    daily_orders = daily_orders.reindex(day_order)

    # Seaborn ile bar grafiği oluşturma
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x=daily_orders.index, y=daily_orders.values)
    for container in ax.containers:
        ax.bar_label(container, label_type='edge', labels=[f"${height:.2f}" for height in container.datavalues])
    # Eksen etiketleri ve başlık ekleme
    plt.xlabel("Day of Week")
    plt.ylabel("Total Order Amount")
    plt.title("Günlere Göre Toplam Sipariş Gelirleri(Tüm Mağazalar)")

    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(plt)


    df_Order["days"] = pd.to_datetime(df_Order['purchase-date']).dt.day_name()
    df_Order["days"] = pd.Categorical(df_Order["days"], categories=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], ordered=True)
    daily_orders = df_Order.groupby(["days", "ship-country"])["item-price"].sum().reset_index()

    # Etiketleri özelleştirin
    country_labels = {
        "Japan": "EKOZ Japan",
        "Canada": "OZM Canada",
        "Mexico": "OZM Mexico"
    }

    # Etiketleri güncelleyin
    daily_orders["ship-country"] = daily_orders["ship-country"].map(country_labels).fillna(daily_orders["ship-country"])

    # Seaborn ile bar grafiği oluşturma
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x="days", y="item-price", hue="ship-country", data=daily_orders)
    for container in ax.containers:
        ax.bar_label(container, label_type='edge', labels=[f"${height:.2f}" for height in container.datavalues])

    # Eksen etiketleri ve başlık ekleme
    plt.xlabel("Day of Week", fontsize=15)
    plt.ylabel("Total Order Amount", fontsize=15)
    plt.title("Mağazaların Günlere Göre Toplam Sipariş Gelirleri", fontsize=18)

    # Eksenlerin eğimini ayarlama
    plt.xticks(rotation=45, fontsize=14)

    plt.legend(title="Country", loc="upper left")

    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)

    ##############

    st.markdown('<p style="background-color: #1f191f; color: white; font-size: 20px; padding: 10px; border-radius: 5px; text-align: center; box-shadow: 0px 2px 3px rgba(0, 0, 0, 0.1);">Haftalara Göre Gelir Dağılımı</p>', unsafe_allow_html=True)

    df_Order["week_number"] = pd.to_datetime(df_Order['purchase-date']).dt.week
    weekly_orders = df_Order.groupby("week_number")["item-price"].sum()

    # Seaborn ile bar grafiği oluşturma
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x=weekly_orders.index, y=weekly_orders.values)
    for container in ax.containers:
        ax.bar_label(container, label_type='edge', labels=[f"${height:.2f}" for height in container.datavalues])
    # Eksen etiketleri ve başlık ekleme
    plt.xlabel("Week of Number")
    plt.ylabel("Total Order Amount")
    plt.title("Haftalık Toplam Sipariş Gelirleri (Tüm Mağazalar)")

    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(plt)

    weekly_orders = df_Order.groupby(["week_number", "ship-country"])["item-price"].sum().reset_index()

    # Etiketleri özelleştirin
    country_labels = {
        "Japan": "EKOZ Japan",
        "Canada": "OZM Canada",
        "Mexico": "OZM Mexico"
    }

    # Etiketleri güncelleyin
    weekly_orders["ship-country"] = weekly_orders["ship-country"].map(country_labels).fillna(weekly_orders["ship-country"])

    # Seaborn ile bar grafiği oluşturma
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x="week_number", y="item-price", hue="ship-country", data=weekly_orders)
    for container in ax.containers:
        ax.bar_label(container, label_type='edge', labels=[f"${height:.2f}" for height in container.datavalues])

    # Eksen etiketleri ve başlık ekleme
    plt.xlabel("Week of Number")
    plt.ylabel("Total Order Amount")
    plt.title("Mağazaların Haftalık Toplam Sipariş Gelirleri")
    plt.legend(loc='upper left')
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(plt)

    st.markdown('<p style="background-color: #1f191f; color: white; font-size: 20px; padding: 10px; border-radius: 5px; text-align: center; box-shadow: 0px 2px 3px rgba(0, 0, 0, 0.1);">Harita da Siparişlerin Dağılımı ve Büyüklüğü</p>', unsafe_allow_html=True)

    mean_item_price = df_Order["item-price"].mean()
    df_Order["item-price"].fillna(mean_item_price, inplace=True)

    # Map 
    fig = px.scatter_mapbox(df_Order, lat="Latitude", lon="Longitude", hover_name="ship-postal-code",
                            color="ship-country", size="item-price")

    # Harita stilini belirleyin (örneğin "open-street-map", "carto-positron", "stamen-terrain" vb.)
    fig.update_layout(mapbox_style="open-street-map")

    fig.update_layout(
        width=700, #Genişlik
        height=500,  # Yükseklik
        margin=dict(l=20, r=20, t=40, b=20),  
        title="Şehirlere Göre Sipariş Gelirinin Büyüklüğü"
    )
    st.plotly_chart(fig)
    
elif selected_tab == "Gelecek Gelir Tahmini":
    df_Order['purchase-date'] = pd.to_datetime(df_Order['purchase-date']).dt.date
    df_Order = df_Order.sort_values(by='purchase-date',ignore_index = True)
    # Canada da Forecasting için gerekli verilerin alınması
    df_can = df_Order[df_Order['ship-country'] == "Canada"]
    df_can = df_can[["purchase-date","item-price"]]
    df_can.reset_index(inplace=True)
    # Japonya da Forecasting için gerekli verilerin alınması
    df_jap = df_Order[df_Order['ship-country'] == "Japan"]
    df_jap = df_jap[["purchase-date","item-price"]]
    df_jap.reset_index(drop=True, inplace=True)
    
    st.markdown('<p style="background-color: #1f191f; color: white; font-size: 20px; padding: 10px; border-radius: 5px; text-align: center; box-shadow: 0px 2px 3px rgba(0, 0, 0, 0.1);">OZM Canada Mağazası</p>', unsafe_allow_html=True)

    # Canada mevcut zamana bağlı gelir dağılımı

    plt.figure(figsize=(12, 6))
    plt.plot(df_can['purchase-date'], df_can['item-price'], marker='o')
    # Eksen etiketleri ve başlık ekleme
    plt.xlabel("Purchase Date")
    plt.ylabel("Price")
    plt.title("Canada Mağazası Zamana Bağlı Gelir Grafiği",fontsize=18)

    # Eksenlerin eğimini ayarlama
    plt.gca().xaxis.set_tick_params(rotation=45)

    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)
    
    # Prophet kütüphanesi için uygun formata getirme
    df_can.rename(columns={'purchase-date': 'ds', 'item-price': 'y'}, inplace=True)

    # Prophet modelini oluşturma
    model = Prophet()

    # Verilerle modeli eğitme
    model.fit(df_can)

    # 1 haftalık (7 gün) öngörü yapma
    future = model.make_future_dataframe(periods=7, freq='D')
    forecast = model.predict(future)

    fig = model.plot(forecast)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Canada Gelecek Gelir Tahmini (1 Hafta)',fontsize=16)

    # Öngörünün sonunu ve gerçek verinin sonunu birleştirerek tahmin edilen çizgiyi çizme
    plt.axvline(df_can['ds'].iloc[-1], color='red', linestyle='--', label='Start Forecasting')
    plt.legend(loc='lower left')

    # Tahmin bölümünü kırmızı olarak gösterme
    plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='red', alpha=0.3)

    st.pyplot(plt)
    
    st.markdown('<p style="background-color: #1f191f; color: white; font-size: 20px; padding: 10px; border-radius: 5px; text-align: center; box-shadow: 0px 2px 3px rgba(0, 0, 0, 0.1);">EKOZ Japan Mağazası</p>', unsafe_allow_html=True)

    plt.figure(figsize=(12, 6))
    plt.plot(df_jap['purchase-date'], df_jap['item-price'], marker='o')
    # Eksen etiketleri ve başlık ekleme
    plt.xlabel("Purchase Date")
    plt.ylabel("Price")
    plt.title("Japonya Mağazası Zamana Bağlı Gelir Grafiği",fontsize=18)

    # Eksenlerin eğimini ayarlama
    plt.gca().xaxis.set_tick_params(rotation=45)

    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)
    
    # Prophet kütüphanesi için uygun formata getirme
    df_jap.rename(columns={'purchase-date': 'ds', 'item-price': 'y'}, inplace=True)

    # Prophet modelini oluşturma
    model2 = Prophet()

    # Verilerle modeli eğitme
    model2.fit(df_jap)

    # 1 haftalık (7 gün) öngörü yapma
    future = model2.make_future_dataframe(periods=7, freq='D')
    forecast = model2.predict(future)

    # Öngörüleri ve trendi görselleştirme
    fig = model2.plot(forecast)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Japonya Gelecek Gelir Tahmini (1 Hafta)',fontsize=16)
    # Öngörünün sonunu ve gerçek verinin sonunu birleştirerek tahmin edilen çizgiyi çizme
    plt.axvline(df_jap['ds'].iloc[-1], color='red', linestyle='--', label='Start Forecasting')
    plt.legend(loc='lower left')
    # Tahmin bölümünü kırmızı olarak gösterme
    plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='red', alpha=0.3)
    st.pyplot(plt)

    
    st.markdown('<p style="background-color: #1f191f; color: white; font-size: 20px; padding: 10px; border-radius: 5px; text-align: center; box-shadow: 0px 2px 3px rgba(0, 0, 0, 0.1);">Olması Gereken Örnek Veri ve Tahmin Çıktısı </p>', unsafe_allow_html=True)
    st.image("https://images.squarespace-cdn.com/content/v1/5268c662e4b0269256614e9a/1527140464965-JAF2HME6U6IB71S81CVZ/timeseries3.png", use_column_width=True)

    
elif selected_tab == "Gelecek Karlılık Tahmini":
    df_Ekoz['Date'] = pd.to_datetime(df_Ekoz['Date']).dt.date
    
    st.markdown('<p style="background-color: #1f191f; color: white; font-size: 20px; padding: 10px; border-radius: 5px; text-align: center; box-shadow: 0px 2px 3px rgba(0, 0, 0, 0.1);">EKOZ Japan Mağazası</p>', unsafe_allow_html=True)

    plt.figure(figsize=(12, 6))
    plt.plot(df_Ekoz['Date'], df_Ekoz['Kar'], marker='o', label='Kar')
    plt.plot(df_Ekoz['Date'], df_Ekoz['Ciro $'], marker='o', label='Ciro')

    # Eksen etiketleri ve başlık ekleme
    plt.xlabel("Purchase Date")
    plt.ylabel("Price")
    plt.title("EKOZ Japan Mağazası Toplam Ciro ve Kar Durumu",fontsize=18)

    # Eksenlerin eğimini ayarlama
    plt.gca().xaxis.set_tick_params(rotation=45)
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)
    
    
    df_forecast = df_Ekoz[["Date","Kar"]]
    # Prophet kütüphanesi için uygun formata getirme
    df_forecast.rename(columns={'Date': 'ds', 'Kar': 'y'}, inplace=True)

    # Prophet modelini oluşturma
    model3 = Prophet()

    # Verilerle modeli eğitme
    model3.fit(df_forecast)

    # 1 haftalık (7 gün) öngörü yapma
    future = model3.make_future_dataframe(periods=7, freq='D')
    forecast = model3.predict(future)

    # Öngörüleri ve trendi görselleştirme
    fig = model3.plot(forecast)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Japonya Gelecek Karlılık Tahmini (1 Hafta)',fontsize=16)
    # Öngörünün sonunu ve gerçek verinin sonunu birleştirerek tahmin edilen çizgiyi çizme
    plt.axvline(df_forecast['ds'].iloc[-1], color='red', linestyle='--', label='Start Forecasting')
    plt.gca().xaxis.set_tick_params(rotation=45)
    plt.legend(loc='lower left')
    # Tahmin bölümünü kırmızı olarak gösterme
    plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='red', alpha=0.3)
    st.pyplot(plt)
    
    st.markdown('<p style="background-color: #1f191f; color: white; font-size: 20px; padding: 10px; border-radius: 5px; text-align: center; box-shadow: 0px 2px 3px rgba(0, 0, 0, 0.1);">Olması Gereken Örnek Veri ve Tahmin Çıktısı </p>', unsafe_allow_html=True)
    st.image("https://i0.wp.com/www.phdata.io/wp-content/uploads/2021/03/time-series-forecast-1024x550.png", use_column_width=True)
