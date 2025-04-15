import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="名片辨識預覽", layout="centered")

st.title("📇 名片辨識即時預覽")

# 上傳圖片
uploaded_file = st.file_uploader("請上傳名片圖片（JPG / PNG）", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="上傳的名片", use_column_width=True)

    # 模擬辨識結果（實際應接 Azure AI）
    st.subheader("🔍 分析結果（模擬資料）")

    data = {
        "FirstName": ["Tom"],
        "LastName": ["Chen"],
        "CompanyName": ["OpenAI Taiwan"],
        "JobTitle": ["AI Engineer"],
        "Email": ["tom@example.com"],
        "Phone": ["+886-912-345-678"]
    }

    df = pd.DataFrame(data)

    st.dataframe(df, use_container_width=True)

    # 匯出 Excel
    if st.button("📤 匯出成 Excel"):
        df.to_excel("business_card_output.xlsx", index=False)
        with open("business_card_output.xlsx", "rb") as f:
            st.download_button("下載 Excel 檔", f, file_name="business_card_output.xlsx")
