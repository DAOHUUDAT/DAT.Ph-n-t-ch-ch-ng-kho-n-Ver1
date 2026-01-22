import streamlit as st
import google.generativeai as genai
from PIL import Image
import fitz  # PyMuPDF để đọc PDF

# 1. Cấu hình trang
st.set_page_config(page_title="AI Financial Analyst Pro", layout="wide")
st.title("🔍 Chuyên Gia Phân Tích Chứng Khoán (Ảnh & PDF)")

with st.sidebar:
    st.header("Cài đặt")
    api_key = st.text_input("Nhập API Key:", type="password")
    st.info("Anh có thể tải lên cùng lúc ảnh biểu đồ và file PDF báo cáo tài chính.")

# 2. Giao diện tải tệp đa phương thức
uploaded_files = st.file_uploader(
    "Tải lên các tệp (Ảnh biểu đồ hoặc PDF báo cáo tài chính)", 
    type=["jpg", "png", "jpeg", "pdf"], 
    accept_multiple_files=True
)

if uploaded_files and api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    # Danh sách chứa dữ liệu gửi cho AI
    content_to_send = ["Bạn là chuyên gia phân tích tài chính. Hãy tổng hợp dữ liệu từ ảnh biểu đồ kỹ thuật và file PDF báo cáo tài chính đính kèm để đưa ra nhận định chuyên sâu về mã cổ phiếu này."]
    
    # Xử lý từng tệp tải lên
    for uploaded_file in uploaded_files:
        if uploaded_file.type == "application/pdf":
            # Đọc PDF và chuyển thành văn bản hoặc xử lý trực tiếp (Gemini 1.5 hỗ trợ PDF)
            pdf_data = uploaded_file.read()
            content_to_send.append({
                "mime_type": "application/pdf",
                "data": pdf_data
            })
            st.write(f"✅ Đã nhận file PDF: {uploaded_file.name}")
        else:
            # Xử lý hình ảnh
            img = Image.open(uploaded_file)
            content_to_send.append(img)
            st.image(img, caption=f'Ảnh: {uploaded_file.name}', width=400)

    if st.button("🚀 Bắt đầu phân tích tổng hợp"):
        try:
            with st.spinner('AI đang đọc dữ liệu từ Ảnh và PDF (quá trình này có thể mất vài giây)...'):
                response = model.generate_content(content_to_send)
                st.success("Kết quả phân tích:")
                st.markdown(response.text)
        except Exception as e:
            st.error(f"Lỗi: {e}")
