# 📇 Business Card Analyzer (Streamlit + Azure Form Recognizer)

這是一個使用 Azure Form Recognizer 的名片辨識工具，支援多張名片即時分析與 Excel 匯出。

## 🔧 快速啟動

```bash
pip install -r requirements.txt
streamlit run app.py
```

## ☁️ 部署到 Streamlit Cloud

1. 登入 [streamlit.io/cloud](https://streamlit.io/cloud)
2. 新增 App，選擇本專案 repo
3. 在 Secrets 設定中新增：
   ```
   AZURE_KEY=你的 Azure 金鑰
   AZURE_ENDPOINT=https://你的-resource.cognitiveservices.azure.com/
   ```

4. 部署完成即可使用

## 📁 專案結構

```
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── sample_cards/
└── outputs/
```
