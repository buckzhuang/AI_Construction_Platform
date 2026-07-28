import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="AI 居家裝修規劃",
    page_icon="🏠",
    layout="wide"
)

model = joblib.load("工程報價模型.pkl")
model_columns = joblib.load("模型欄位.pkl")

st.markdown("""
<style>
.stApp {
    background-color: #f5f1e9;
}

.block-container {
    max-width: 1150px;
    padding-top: 1.5rem;
}

.hero {
    background: linear-gradient(120deg, #4d5145, #89836f);
    padding: 55px 45px;
    border-radius: 4px;
    color: white;
    margin-bottom: 28px;
}

.hero h1 {
    font-size: 45px;
    margin: 0 0 12px 0;
}

.hero p {
    font-size: 18px;
    color: #f3efe5;
}

.section-title {
    color: #49483f;
    font-size: 25px;
    font-weight: 700;
    margin: 15px 0;
}

.card {
    background: #ffffff;
    padding: 25px;
    border-radius: 5px;
    border: 1px solid #ded8ca;
    margin-bottom: 18px;
}

.price-card {
    background: #55584c;
    color: white;
    padding: 28px;
    border-radius: 5px;
    text-align: center;
}

.price-card h2 {
    font-size: 38px;
    margin: 8px 0;
}

.recommend-card {
    background: #ebe5d7;
    padding: 24px;
    border-left: 6px solid #7b806e;
    border-radius: 4px;
    margin-top: 18px;
}

.small-text {
    color: #747064;
    font-size: 14px;
}

div.stButton > button {
    background-color: #5c6153;
    color: white;
    border: none;
    border-radius: 3px;
    padding: 13px;
    font-size: 17px;
    font-weight: bold;
}

div.stButton > button:hover {
    background-color: #454a3f;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>AI 居家裝修規劃</h1>
    <p>先設定預算上限，再由 AI 為您規劃合適的裝修方案。</p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown('<div class="section-title">01　基本需求</div>',
                unsafe_allow_html=True)

    budget = st.number_input(
        "最高裝修預算（NT$）",
        min_value=100000,
        max_value=10000000,
        value=1500000,
        step=100000
    )

    area = st.number_input(
        "室內坪數",
        min_value=5,
        max_value=200,
        value=30
    )

    house_type = st.selectbox(
        "房屋狀況",
        ["新成屋", "中古屋", "老屋翻新"]
    )

    style = st.selectbox(
        "喜好風格",
        ["現代簡約", "北歐風", "無印風", "工業風", "日式風"]
    )

with right:
    st.markdown('<div class="section-title">02　裝修需求</div>',
                unsafe_allow_html=True)

    priority = st.selectbox(
        "最重視的裝修項目",
        ["收納機能", "客廳空間", "廚房設備", "臥室舒適", "整體質感"]
    )

    family = st.selectbox(
        "居住人數",
        ["1 人", "2 人", "3～4 人", "5 人以上"]
    )

    quality = st.selectbox(
        "材料等級",
        ["經濟型", "標準型", "高級型"]
    )

    st.info(
        "模型：Random Forest\n\n"
        "模型 R²：0.986\n\n"
        "平均誤差：約 NT$37,320"
    )

if st.button("產生 AI 裝修方案", use_container_width=True):

    demolition = "否" if house_type == "新成屋" else "是"

    if house_type == "新成屋":
        difficulty = "低"
    elif house_type == "中古屋":
        difficulty = "中"
    else:
        difficulty = "高"

    data = pd.DataFrame({
        "工程類型": ["室內裝修"],
        "工程坪數": [area],
        "品質等級": [quality],
        "是否需要拆除": [demolition],
        "工程難度": [difficulty]
    })

    data = pd.get_dummies(data)
    data = data.reindex(columns=model_columns, fill_value=0)

    estimate = model.predict(data)[0]
    difference = budget - estimate
    budget_per_ping = budget / area

    if budget >= estimate * 1.1:
        plan = "完整質感裝修"
        description = (
            "預算較充足，可進行全室規劃，包含收納、天花板、"
            "燈光、系統櫃與風格設計。"
        )
    elif budget >= estimate * 0.85:
        plan = "標準實用裝修"
        description = (
            f"建議以「{priority}」為主要投入項目，其他空間採用"
            "標準材料，兼顧機能與預算。"
        )
    else:
        plan = "重點區域裝修"
        description = (
            f"目前預算低於 AI 完整裝修估價，建議優先處理「{priority}」，"
            "並保留原有格局與可使用設備。"
        )

    st.markdown("---")
    st.markdown('<div class="section-title">03　AI 規劃結果</div>',
                unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="price-card">
            <div>您的預算上限</div>
            <h2>NT$ {budget:,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="price-card">
            <div>AI 預估費用</div>
            <h2>NT$ {estimate:,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="price-card">
            <div>每坪可用預算</div>
            <h2>NT$ {budget_per_ping:,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)

    if difference >= 0:
        st.success(f"預算高於 AI 預估約 NT$ {difference:,.0f}")
    else:
        st.warning(f"預算低於 AI 預估約 NT$ {abs(difference):,.0f}")

    st.markdown(f"""
    <div class="recommend-card">
        <div class="small-text">AI 推薦方案</div>
        <h2>{plan}</h2>
        <p>{description}</p>
        <p><b>建議風格：</b>{style}</p>
        <p><b>優先項目：</b>{priority}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">04　建議預算分配</div>',
                unsafe_allow_html=True)

    construction = budget * 0.62
    furniture = budget * 0.15
    appliances = budget * 0.15
    reserve = budget * 0.08

    allocation = pd.DataFrame({
        "項目": ["裝修工程", "家具軟裝", "家電設備", "備用預算"],
        "比例": ["62%", "15%", "15%", "8%"],
        "建議金額": [
            f"NT$ {construction:,.0f}",
            f"NT$ {furniture:,.0f}",
            f"NT$ {appliances:,.0f}",
            f"NT$ {reserve:,.0f}"
        ]
    })

    st.table(allocation)

    st.markdown('<div class="section-title">05　裝修摘要</div>',
                unsafe_allow_html=True)

    summary = pd.DataFrame({
        "項目": [
            "房屋狀況",
            "室內坪數",
            "居住人數",
            "喜好風格",
            "材料等級",
            "裝修重點",
            "AI 推薦方案"
        ],
        "內容": [
            house_type,
            f"{area} 坪",
            family,
            style,
            quality,
            priority,
            plan
        ]
    })

    st.table(summary)

st.markdown("---")
st.caption("AI 居家裝修規劃｜本系統結果為專題模擬估算，實際費用仍須現場丈量。")
st.caption("AI 工程估價系統｜Python・Random Forest・Streamlit")
