import streamlit as st
import pandas as pd
import requests
import uuid
import time
from PIL import Image
import os
from dotenv import load_dotenv

# 讀取金鑰設定
load_dotenv()
AZURE_KEY = os.getenv("AZURE_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
MODEL_URL = f"{AZURE_ENDPOINT}formrecognizer/documentModels/prebuilt-businessCard:analyze?api-version=2023-07-31"

st.set_page_config(page_title="名片辨識預覽", layout="centered")
st.title("📇 名片辨識即時預覽")

# 上傳名片圖片
uploaded_file = st.file_uploader("請上傳名片圖片（JPG / PNG）", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="名片預覽", use_column_width=True)

    # 呼叫 Azure Form Recognizer API
    with st.spinner("辨識中..."):

        # 發送請求
        headers = {
            "Ocp-Apim-Subscription-Key": AZURE_KEY,
            "Content-Type": "application/octet-stream"
        }
        response = requests.post(MODEL_URL, headers=headers, data=uploaded_file.getvalue())

        if response.status_code != 202:
            st.error("⚠ 無法提交文件到 Azure API。請檢查金鑰與權限。")
            st.stop()

        operation_location = response.headers["Operation-Location"]

        # 查詢分析結果（輪詢）
        for _ in range(10):
            result = requests.get(operation_location, headers={"Ocp-Apim-Subscription-Key": AZURE_KEY})
            result_json = result.json()
            if result_json["status"] == "succeeded":
                break
            time.sleep(1)
        else:
            st.error("⚠ 分析超時，請稍後再試。")
            st.stop()

        # 解析欄位資料
        fields = result_json["analyzeResult"]["documents"][0]["fields"]
      def extract_value(field):
    if "valueString" in field:
        return field["valueString"]
    elif "valuePhoneNumber" in field:
        return field["valuePhoneNumber"]
    elif "valueArray" in field:
        return ", ".join([extract_value(item) for item in field["valueArray"]])
    elif "valueObject" in field:
        return str(field["valueObject"])
    else:
        return ""

def extract_nested_field(array_field, key):
    try:
        return array_field["valueArray"][0]["valueObject"].get(key, {}).get("valueString", "")
    except:
        return ""

fields = result_json["analyzeResult"]["documents"][0]["fields"]
data = {
    "FirstName": extract_nested_field(fields.get("ContactNames", {}), "firstName"),
    "LastName": extract_nested_field(fields.get("ContactNames", {}), "lastName"),
    "Company": extract_value(fields.get("CompanyNames", {})),
    "JobTitle": extract_value(fields.get("JobTitles", {})),
    "Email": extract_value(fields.get("Emails", {})),
    "Phone": extract_value(fields.get("MobilePhones", {})) or extract_value(fields.get("WorkPhones", {})),
}


        df = pd.DataFrame([data])
        st.success("🎉 分析完成！")
        st.dataframe(df, use_container_width=True)

        # 匯出 Excel
        if st.button("📤 匯出成 Excel"):
            df.to_excel("business_card_result.xlsx", index=False)
            with open("business_card_result.xlsx", "rb") as f:
                st.download_button("下載 Excel 檔", f, file_name="business_card_result.xlsx")
