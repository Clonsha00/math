import streamlit as st
import pandas as pd
import os

# 設定網頁標題與排版
st.set_page_config(page_title="Laplace 題庫", layout="wide")

FILE_NAME = 'laplace_questions.csv'

st.title("📝 拉普拉絲轉換 (Laplace Transform) 題庫系統")
st.markdown("---")

# --- 左側：輸入區 ---
with st.sidebar:
    st.header("新增題目")
    with st.form("question_form", clear_on_submit=True):
        # 題型分類
        tag = st.selectbox("題型分類", 
            ["基本轉換 (Basic)", "微分性質 (Derivative)", "平移定理 (Shifting)", 
             "單位步階 (Unit Step)", "摺積 (Convolution)", "反轉換 (Inverse)"])
        
        # 輸入提示
        st.info("💡 提示：輸入 LaTeX 語法可顯示數學符號。\n例如：`\\frac{1}{s^2}` 會顯示分數。")
        
        # 題目與答案輸入
        q_text = st.text_area("題目 (Question)", height=100, placeholder="例如: Find L{t^2}")
        a_text = st.text_area("答案 (Answer)", height=100, placeholder="例如: 2!/s^3")
        
        submitted = st.form_submit_button("💾 儲存題目", use_container_width=True)

# --- 處理儲存邏輯 ---
if submitted:
    if not q_text or not a_text:
        st.sidebar.error("❌ 題目與答案不能為空！")
    else:
        new_data = pd.DataFrame([{"Tag": tag, "Question": q_text, "Answer": a_text}])
        if os.path.exists(FILE_NAME):
            new_data.to_csv(FILE_NAME, mode='a', header=False, index=False)
        else:
            new_data.to_csv(FILE_NAME, index=False)
        st.sidebar.success("✅ 題目已儲存！")

# --- 右側：顯示區 ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("👁️ 即時預覽 (Preview)")
    st.caption("確認您的 LaTeX 語法是否正確")
    
    # 預覽卡片
    with st.container(border=True):
        st.markdown("**題目：**")
        if q_text:
            st.latex(q_text)
        else:
            st.text("(等待輸入...)")
        
        st.markdown("**答案：**")
        if a_text:
            st.latex(a_text)
        else:
            st.text("(等待輸入...)")

with col2:
    st.subheader("📚 已建立題庫")
    if os.path.exists(FILE_NAME):
        df = pd.read_csv(FILE_NAME)
        # 顯示資料表，並讓高度自動調整
        st.dataframe(df, use_container_width=True, height=400)
        
        # 下載按鈕
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 下載題庫 (CSV)", csv, "laplace_questions.csv", "text/csv")
    else:
        st.info("目前還沒有題目，請從左側新增！")