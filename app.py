import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Cấu hình giao diện
st.title("Phân Tích Chứng Khoán AI - Anh Đạt")
api_key = st.sidebar.text_input("Nhập API Key của bạn:", type="password")

# 2. Tải ảnh lên
uploaded_file = st.file_uploader("Tải lên biểu đồ hoặc báo cáo tài chính", type=["jpg", "png", "jpeg"])

if uploaded_file and api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    img = Image.open(uploaded_file)
    st.image(img, caption='Ảnh đã tải lên', use_column_width=True)
    
    if st.button("Bắt đầu phân tích & Chấm điểm CANSLIM"):
        # Prompt này anh đã soạn sẵn trong AI Studio
        prompt = "Hãy phân tích hình ảnh này và chấm điểm CANSLIM 1-10..."
        response = model.generate_content([prompt, img])

        st.markdown(response.text)
