import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Verilerin okunması
order_bus_kep = pd.read_csv("order_bus_kep.csv")
keepa_business = pd.read_csv("kep_bus.csv")
df_Business = pd.read_csv("Ortak_Business.csv")
df_All_Users = pd.read_csv("New_All_Users.csv")

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

# Streamlit arayüzünü oluşturma
st.image("logo-black.png", use_column_width=True)
#st.markdown("<h1 class='centered-title'>OneAMZ</h1>", unsafe_allow_html=True)

page = st.sidebar.radio("Sayfa Seçiniz", ["Tüm Satıcılar","Mağazalar Genel Tablo", "Mağazalar Detay"])
st.sidebar.title("Parametre Ayarı")


if page == "Tüm Satıcılar":
    st.markdown("<h2 class='centered-title'>Tüm Satıcılar Genel Tablo</h2>", unsafe_allow_html=True)
    nlargest_value = st.sidebar.slider("Görüntülemek istediğiniz satıcı sayısı (1-30)", 1, 30, 20)
    
    counts = [df_All_Users["Seller ID"].count(), df_All_Users["Total Account Count"].sum()]
    labels = ["Satıcı Sayısı", "Satıcı Hesap Sayısı"]

    # Bar grafiği çizimi
    plt.figure(facecolor = "#fff300",figsize=(8, 5))
    ax=sns.barplot(x=labels, y=counts)
    ax.bar_label(ax.containers[0])
    plt.title("Satıcı Sayısı & Hesap Sayısı Grafiği")
    plt.ylabel("Sayı")
    st.pyplot(plt)
    
    
    top_15_accounts = df_All_Users.nlargest(nlargest_value, "Total Account Count")
    plt.figure(facecolor = "#fff300",figsize=(10, 6))
    ax = sns.barplot(y="Seller ID", x="Total Account Count", data=top_15_accounts)
    ax.bar_label(ax.containers[0])

    # Sadece "suspend" olan satırların sırasını tutma
    suspend_indices = []
    active_indices = []
    i = 0
    for idx, row in top_15_accounts.iterrows():
        if row["Status"] == "Suspended":
            suspend_indices.append(i)
        else:
            active_indices.append(i)
        i += 1

    # "suspend" olanların bar grafiğinde "suspended", "active" olmayanların bar grafiğinde "active" yazılması
    for idx, bar in enumerate(ax.patches):
        if idx in suspend_indices:
            text = 'Suspended'
        elif idx in active_indices:
            text = 'Active'
        else:
            text = ''  # Herhangi bir durum belirtilmediyse boş bırak
        width = bar.get_width()
        height = bar.get_height()
        x, y = bar.get_xy()
        ax.text(x + width/2, y + height/2, text, ha='center', va='center', fontsize=12, color='black')

    plt.title(f"En Çok Hesaba Sahip İlk {nlargest_value} Satıcının Total Account & Status Durumu")
    plt.xlabel("Total Account Count")
    plt.ylabel("Seller ID")
    st.pyplot(plt)
    
    
    # İki subplot oluşturma
    fig, axes = plt.subplots(nrows=1, ncols=2,facecolor = "#fff300", figsize=(15, 8))

    # İlk subplot: Total Income
    ax1 = sns.barplot(y="Seller ID", x="Total Account Count", data=top_15_accounts, ax=axes[0])
    ax1.bar_label(ax1.containers[0])
    # Sadece "suspend" olan satırların sırasını tutma
    suspend_indices = []
    i = 0
    for idx, row in top_15_accounts.iterrows():
        if row["Status"] == "Suspended":       
            suspend_indices.append(i)
        i+=1

    # Sadece "suspend" olanların bar grafiğinde barın içinde belirtilmesi
    for idx, bar in enumerate(ax.patches):
        if idx in suspend_indices:
            width = bar.get_width()
            height = bar.get_height()
            x, y = bar.get_xy()
            ax1.text(x + width/2, y + height/2, 'suspend', ha='center', va='center', fontsize=14, color='black')
    ax1.set_title(f"En Çok Hesaba Sahip İlk {nlargest_value} Satıcı Hesap Sayısı",fontsize= 18)
    ax1.set_xlabel("Total Account",fontsize= 15)
    ax1.set_ylabel("Seller ID",fontsize= 15)
    ax1.tick_params(axis='x', labelsize=12)
    ax1.tick_params(axis='y', labelsize=12)

    # İkinci subplot: Total Profit
    ax2 = sns.barplot(y="Seller ID", x="Total Product Count", data=top_15_accounts, ax=axes[1])
    ax2.bar_label(ax2.containers[0], fontsize=14)
    ax2.set_title(f"En Çok Hesaba Sahip İlk {nlargest_value} Satıcı Ürün Sayısı",fontsize= 18)
    ax2.set_xlabel("Total Product",fontsize= 15)
    ax2.set_ylabel("")
    ax2.tick_params(axis='x', labelsize=12)
    ax2.tick_params(axis='y', labelsize=12)

    plt.tight_layout()
    st.pyplot(plt)
    
    
    # İki subplot oluşturma
    fig, axes = plt.subplots(nrows=1, ncols=2,facecolor = "#fff300", figsize=(15, 8))

    # İlk subplot: Total Income
    ax1 = sns.barplot(y="Seller ID", x="Total Income", data=top_15_accounts, ax=axes[0])
    ax1.bar_label(ax1.containers[0], fontsize=14)
    ax1.set_title(f"En Çok Hesaba Sahip İlk {nlargest_value} Satıcı Gelir Bilgisi",fontsize= 18)
    ax1.set_xlabel("Total Income",fontsize= 15)
    ax1.set_ylabel("Seller ID",fontsize= 15)
    ax1.tick_params(axis='x', labelsize=12)
    ax1.tick_params(axis='y', labelsize=12)

    # İkinci subplot: Total Profit
    ax2 = sns.barplot(y="Seller ID", x="Total Profit", data=top_15_accounts, ax=axes[1])
    ax2.bar_label(ax2.containers[0], fontsize=14)
    ax2.set_title(f"En Çok Hesaba Sahip İlk {nlargest_value} Satıcı Kar Bilgisi",fontsize= 18)
    ax2.set_xlabel("Total Profit",fontsize= 15)
    ax2.set_ylabel("")
    ax2.tick_params(axis='x', labelsize=12)
    ax2.tick_params(axis='y', labelsize=12)

    plt.tight_layout()
    st.pyplot(plt)

elif page == "Mağazalar Genel Tablo":
    st.markdown("<h2 class='centered-title'>Satıcı Sayfa Etkileşim Analizi</h2>", unsafe_allow_html=True)
    st.markdown("<h3 class='centered-title'>Satılan Ürünlerin Analizi</h2>", unsafe_allow_html=True)
    nlargest_value = st.sidebar.slider("Görüntülemek istediğiniz ürün sayısı (1-30)", 1, 30, 20)
    
    country_counts = order_bus_kep["Country"].value_counts()

    plt.figure(facecolor = "#fff300",figsize = (6,3))
    plt.pie(country_counts, labels=country_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title("Mağazaların Sipariş Dağılımı",fontsize= 10)
    plt.axis('equal')  # Dairesel şeklin korunması için
    st.pyplot(plt)
    
    # 1. grafik
    plt.figure(facecolor = "#fff300",figsize = (12,6))
    #plt.figure(figsize=(12, 6))
    ax=sns.barplot(x=order_bus_kep['asin'], y=order_bus_kep['Page Views - Total'], label='Page Views')
    ax2=sns.barplot(x=order_bus_kep['asin'], y=order_bus_kep['Page Views - Total - B2B'],color = "black", label='Page Views - B2B')
    ax.bar_label(ax.containers[0])
    #ax2.bar_label(ax2.containers[1])
    # Eksen etiketleri ve başlık ekleme
    plt.xlabel("ASIN")
    plt.ylabel("Page Views")
    plt.title("Tüm Mağazalar İçin Siparişi Verilen Ürünlerin Sayfa Görüntülenmesi (Bireysel & Kurumsal)",fontsize= 18)

    # Eksenlerin eğimini ayarlama
    plt.gca().xaxis.set_tick_params(rotation=90)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)
    
    # 2. grafik
    category_counts = order_bus_kep["Categories: Root"].value_counts()
    page_views_total = order_bus_kep.groupby("Categories: Root")["Page Views - Total"].sum().sort_values(ascending=False)

    fig, axes = plt.subplots(1, 2, facecolor = "#fff300",figsize=(14, 6))

    # İlk grafik: Kategori Sayıları
    sns.barplot(ax=axes[0], y=category_counts.index, x=category_counts.values)
    axes[0].bar_label(axes[0].containers[0])
    axes[0].set_xlabel("Counts")
    axes[0].set_ylabel("Categories")
    axes[0].set_title("Kategorilerin Satış Durumu",fontsize= 15)
    axes[0].tick_params(axis='y', labelrotation=0)

    # İkinci grafik: Toplam Sayfa Görüntüleme Sayıları
    sns.barplot(ax=axes[1], y=page_views_total.index, x=page_views_total.values)
    axes[1].bar_label(axes[1].containers[0])
    axes[1].set_xlabel("Counts")
    axes[1].set_ylabel("")
    axes[1].set_title("Kategorilerin Sayfa Tıklanma Durumu",fontsize= 15)
    axes[1].tick_params(axis='y', labelrotation=0)

    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("<h3 class='centered-title'>Satışa Sunulan Ürünlerin Analizi</h2>", unsafe_allow_html=True)
    # 2. grafik
    
    country_counts2 = keepa_business["Country"].value_counts()

    plt.figure(facecolor = "#fff300",figsize = (6,3))
    plt.pie(country_counts2, labels=country_counts2.index, autopct='%1.1f%%', startangle=140)
    plt.title("Mağazaların Satışa Sunulan Ürün Dağılımı",fontsize= 10)
    plt.axis('equal')  # Dairesel şeklin korunması için
    st.pyplot(plt)
    
    # En yüksek ilk 20 ürünün çekilmesi
    df_20 = keepa_business.nlargest(nlargest_value, 'Page Views - Total')[["(Child) ASIN","Page Views - Total","Country","Categories: Root"]]

    # Grafik oluşturma
    plt.figure(facecolor = "#fff300",figsize=(25, 15))  # Grafik boyutunu ayarlayın
    ax = sns.barplot(y=df_20['(Child) ASIN'], x=df_20['Page Views - Total'])
    ax.bar_label(ax.containers[0], fmt="%d", fontsize=22)  # Sayıları daha net hale getirmek için format ayarı

    canada = []
    mexico = []
    japan = []
    i = 0
    for idx, row in df_20.iterrows():
        if row["Country"] == "Canada":
            canada.append(i)
        elif row["Country"] == "Mexico":
            mexico.append(i)
        else:
            japan.append(i)
        i += 1

    # "suspend" olanların bar grafiğinde "suspended", "active" olmayanların bar grafiğinde "active" yazılması
    for idx, bar in enumerate(ax.patches):
        if idx in canada:
            text = 'Canada'
        elif idx in mexico:
            text = 'Mexico'
        else:
            text = 'Japan'  # Herhangi bir durum belirtilmediyse boş bırak
        width = bar.get_width()
        height = bar.get_height()
        x, y = bar.get_xy()
        ax.text(x + width/2, y + height/2, text, ha='center', va='center', fontsize=22, color='black')

    # Eksen etiketlerini daha büyük ve okunabilir hale getirme
    plt.xlabel("Page Views", fontsize=20)
    plt.ylabel("ASIN", fontsize=20)
    plt.title(f"Satışa Sunulan Ürünlerde En Çok Tıklanması Olan İlk {nlargest_value} Ürün ve Mağaza Bilgisi", fontsize=30)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    st.pyplot(plt)
    
    # 3. grafik
    
    category_counts = keepa_business["Categories: Root"].value_counts()
    page_views_total = keepa_business.groupby("Categories: Root")["Page Views - Total"].sum().sort_values(ascending=False)

    # İki grafiği yan yana çizdirme
    fig, axes = plt.subplots(1, 2,facecolor = "#fff300", figsize=(12, 6))

    # İlk grafik: Kategori Sayıları
    sns.barplot(ax=axes[0], y=category_counts.index, x=category_counts.values)
    axes[0].bar_label(axes[0].containers[0])
    axes[0].set_xlabel("Counts")
    axes[0].set_ylabel("Categories")
    axes[0].set_title("Satışa Sunulan Ürünlerin Kategori Durumu",fontsize= 15)
    axes[0].tick_params(axis='y', labelrotation=0)

    # İkinci grafik: Toplam Sayfa Görüntüleme Sayıları
    sns.barplot(ax=axes[1], y=page_views_total.index, x=page_views_total.values)
    axes[1].bar_label(axes[1].containers[0])
    axes[1].set_xlabel("Counts")
    axes[1].set_ylabel("")
    axes[1].set_title("Satışa Sunulan Ürünlerin Kategorik Tıklanma Durumu",fontsize= 15)
    axes[1].tick_params(axis='y', labelrotation=0)

    plt.tight_layout()
    st.pyplot(plt)
    
    

elif page == "Mağazalar Detay":
    st.markdown("<h2 class='centered-title'>Satıcı Sayfa Etkileşim Analizi</h2>", unsafe_allow_html=True)
    countries = ["OZM Canada", "OZM Mexico", "EKOZ Japan"]
    selected_country = st.sidebar.selectbox("Ülke Seçiniz", countries)
    nlargest_value = st.sidebar.slider("Görüntülemek istediğiniz ürün sayısı (1-30)", 1, 30, 20)

    # Seçilen ülkeye ait kodları çalıştırma
    if selected_country == "OZM Canada":
        country = "Canada"
    elif selected_country == "OZM Mexico":
        country = "Mexico"
    elif selected_country == "EKOZ Japan":
        country = "Japan"
    else:
        country = ""

    if country:
        st.markdown(f"<h3 class='centered-title'>{selected_country} Mağazasının Sipariş ve Tıklanma Analizi</h3>", unsafe_allow_html=True)

        # Seçilen ülkeye ait siparişleri çekme
        dff = order_bus_kep[order_bus_kep["Country"] == country]
        dff2 = df_Business[df_Business["Country"]==country]
        st.write(f"{selected_country} Mağazasının toplam sipariş sayısı: **{dff.shape[0]}**")
        st.write(f"{selected_country} Mağazasının toplam satışa sunulan ürün sayısı: **{dff2.shape[0]}**")

        # Siparişlere ait grafiği çizdirme
        plt.figure(facecolor = "#fff300",figsize=(12, 6))
        ax = sns.barplot(y=dff['asin'], x=dff['Page Views - Total'], order=dff.sort_values('Page Views - Total', ascending=False)['asin'])
        ax.bar_label(ax.containers[0])
        plt.xlabel("ASIN")
        plt.ylabel("Page Views")
        plt.title(f"{selected_country} Mağazasında Siparişi Verilen Ürünlerin Sayfa Görüntülenmesi",fontsize= 15)
        plt.gca().xaxis.set_tick_params(rotation=90)
        plt.grid(True)
        st.pyplot(plt)


        # En çok tıklanmış ürünlerin grafiği
        dff_30 = keepa_business[keepa_business["Country"]==country].nlargest(nlargest_value, 'Page Views - Total')
        plt.figure(facecolor = "#fff300",figsize=(14, 8))
        ax = sns.barplot(y=dff_30['(Child) ASIN'], x=dff_30['Page Views - Total'])
        ax.bar_label(ax.containers[0])
        plt.xlabel("ASIN")
        plt.ylabel("Page Views")
        plt.title(f"{selected_country} Mağazasında Satışa Sunulan Ürünlerde En Çok Tıklanması olan İlk {nlargest_value} Ürün",fontsize= 15)
        plt.gca().xaxis.set_tick_params(rotation=90)
        plt.grid(True)
        st.pyplot(plt)

        # Ortak ürünleri bulma ve sayma
        common_asins = set(dff['asin']).intersection(set(dff_30['(Child) ASIN']))
        common_count = len(common_asins)
        st.write(f"{selected_country} Mağazasında Satışa Sunulan ve En Çok Tıklanma Alan İlk {nlargest_value} Üründe **{common_count}** Tane Satış Gerçekleşmiş")
        
        category_counts2 = order_bus_kep[order_bus_kep["Country"]==country]["Categories: Root"].value_counts()
        page_views_total2 = order_bus_kep[order_bus_kep["Country"]==country].groupby("Categories: Root")["Page Views - Total"].sum().sort_values(ascending=False)

        # İki grafiği yan yana çizdirme
        fig, axes = plt.subplots(1, 2,facecolor = "#fff300", figsize=(14, 6))

        # İlk grafik: Kategori Sayıları
        sns.barplot(ax=axes[0], y=category_counts2.index, x=category_counts2.values)
        axes[0].bar_label(axes[0].containers[0])
        axes[0].set_xlabel("Counts",fontsize= 15)
        axes[0].set_ylabel("Categories",fontsize= 15)
        axes[0].set_title(f"{selected_country} Mağazası İçin Kategorilerin Satış Durumu",fontsize= 15)
        axes[0].tick_params(axis='y', labelrotation=0)
        axes[0].tick_params(axis='x', labelsize=12)
        axes[0].tick_params(axis='y', labelsize=12)

        # İkinci grafik: Toplam Sayfa Görüntüleme Sayıları
        sns.barplot(ax=axes[1], y=page_views_total2.index, x=page_views_total2.values)
        axes[1].bar_label(axes[1].containers[0])
        axes[1].set_xlabel("Counts",fontsize= 15)
        axes[1].set_ylabel("")
        axes[1].set_title(f"{selected_country} Mağazası İçin Kategorilerin Sayfa Tıklanma Durumu",fontsize= 15)
        axes[1].tick_params(axis='y', labelrotation=0)
        axes[1].tick_params(axis='x', labelsize=12)
        axes[1].tick_params(axis='y', labelsize=12)

        plt.tight_layout()
        st.pyplot(plt)
