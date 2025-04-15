import os
import streamlit as st
import pandas as pd
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import base64

load_dotenv()
endpoint = os.getenv("AZURE_ENDPOINT")
key = os.getenv("AZURE_KEY")

client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

st.set_page_config(page_title="Business Card Analyzer", page_icon="📇")
st.title("📇 名片辨識 App（Azure Form Recognizer）")
uploaded_files = st.file_uploader("請上傳名片圖片（支援多檔）", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

results = []
if uploaded_files:
    for file in uploaded_files:
        image_bytes = file.read()
        poller = client.begin_analyze_document("prebuilt-businessCard", document=image_bytes)
        result = poller.result()

        for doc in result.documents:
            fields = {k: v.value if v else "" for k, v in doc.fields.items()}
            fields["檔案名稱"] = file.name
            results.append(fields)

    df = pd.DataFrame(results)
    st.success("✅ 辨識完成")
    st.dataframe(df)

    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return output.getvalue()

    excel_data = to_excel(df)
    st.download_button("📥 下載 Excel 檔", data=excel_data, file_name="business_cards.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
