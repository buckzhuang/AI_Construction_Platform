
import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="AI 工程估價系統",
    page_icon="🏗️",
    layout="wide"
)

model = joblib.load("工程報價模型.pkl")
model_columns = joblib.load("模型欄位.pkl")

st.title("🏗️ AI 工程估價系統")
st.write("輸入工程條件，立即取得 AI 預測報價。")

col1, col2 = st.columns(2)

with col1:
    project_type = st.selectbox(
        "工程類型",
        ["油漆工程", "水電工程", "室內裝修", "地板工程"]
    )

    area = st.number_input(
        "工程坪數",
        min_value=1,
        max_value=300,
        value=30
    )

    quality = st.selectbox(
        "品質等級",
        ["經濟型", "標準型", "高級型"]
    )

with col2:
    demolition = st.selectbox(
        "是否需要拆除",
        ["否", "是"]
    )

    difficulty = st.selectbox(
        "工程難度",
        ["低", "中", "高"]
    )

    st.info(
        "模型：Random Forest\n\n"
        "R²：0.986\n\n"
        "MAE：約 NT$37,320"
    )

if st.button("開始 AI 估價", use_container_width=True):
    data = pd.DataFrame({
        "工程類型": [project_type],
        "工程坪數": [area],
        "品質等級": [quality],
        "是否需要拆除": [demolition],
        "工程難度": [difficulty]
    })

    data = pd.get_dummies(data)
    data = data.reindex(columns=model_columns, fill_value=0)

    price = model.predict(data)[0]
    low_price = price * 0.9
    high_price = price * 1.1

    st.success("估價完成")

    result1, result2, result3 = st.columns(3)

    result1.metric(
        "AI 預測報價",
        f"NT$ {price:,.0f}"
    )

    result2.metric(
        "建議最低報價",
        f"NT$ {low_price:,.0f}"
    )

    result3.metric(
        "建議最高報價",
        f"NT$ {high_price:,.0f}"
    )

    st.subheader("工程摘要")

    summary = pd.DataFrame({
        "項目": [
            "工程類型",
            "工程坪數",
            "品質等級",
            "是否需要拆除",
            "工程難度"
        ],
        "內容": [
            project_type,
            f"{area} 坪",
            quality,
            demolition,
            difficulty
        ]
    })

    st.table(summary)

st.divider()
st.caption("AI 工程估價系統｜Python・Random Forest・Streamlit")