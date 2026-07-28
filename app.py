import streamlit as st
import pandas as pd
import joblib

# =========================
# 網站基本設定
# =========================
st.set_page_config(
    page_title="築居 AI 室內設計",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# 載入模型
# =========================
@st.cache_resource
def load_model():
    model = joblib.load("工程報價模型.pkl")
    model_columns = joblib.load("模型欄位.pkl")
    return model, model_columns


model, model_columns = load_model()

# =========================
# CSS 網站樣式
# =========================
st.markdown(
    """
    <style>
    html {
        scroll-behavior: smooth;
    }

    .stApp {
        background-color: #f6f3ed;
        color: #33352f;
    }

    .block-container {
        max-width: 1280px;
        padding-top: 0;
        padding-bottom: 2rem;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* 導覽列 */
    .navbar {
        position: sticky;
        top: 0;
        z-index: 999;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 17px 28px;
        margin: 0 -1rem;
        background: rgba(246, 243, 237, 0.96);
        border-bottom: 1px solid #ddd7ca;
        backdrop-filter: blur(10px);
    }

    .navbar-logo {
        font-size: 23px;
        font-weight: 800;
        letter-spacing: 3px;
        color: #3e453b;
        white-space: nowrap;
    }

    .navbar-links {
        display: flex;
        flex-wrap: wrap;
        justify-content: flex-end;
        gap: 18px;
    }

    .navbar-links a {
        color: #4c5048;
        text-decoration: none;
        font-size: 14px;
        font-weight: 600;
    }

    .navbar-links a:hover {
        color: #8b7053;
    }

    /* 首頁背景圖 */
    .hero {
        min-height: 640px;
        margin: 0 -1rem 55px -1rem;
        padding: 85px 55px;
        display: flex;
        align-items: center;
        border-radius: 0 0 8px 8px;
        background:
            linear-gradient(
                90deg,
                rgba(31, 34, 29, 0.78),
                rgba(31, 34, 29, 0.30)
            ),
            url("https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?auto=format&fit=crop&w=1800&q=85");
        background-size: cover;
        background-position: center;
    }

    .hero-content {
        max-width: 680px;
        color: white;
    }

    .hero-small {
        font-size: 15px;
        letter-spacing: 4px;
        margin-bottom: 17px;
        color: #eee7da;
    }

    .hero h1 {
        margin: 0 0 22px 0;
        font-size: 58px;
        line-height: 1.2;
        letter-spacing: 2px;
    }

    .hero p {
        max-width: 600px;
        font-size: 19px;
        line-height: 1.9;
        color: #f1ede5;
    }

    .hero-button {
        display: inline-block;
        margin-top: 25px;
        padding: 14px 27px;
        color: white !important;
        background-color: #8b7053;
        text-decoration: none;
        border-radius: 3px;
        font-weight: 700;
    }

    .hero-button:hover {
        background-color: #70583f;
    }

    /* 通用標題 */
    .section-anchor {
        scroll-margin-top: 90px;
    }

    .section-heading {
        margin-top: 48px;
        margin-bottom: 28px;
        text-align: center;
    }

    .section-label {
        color: #9b8061;
        font-size: 13px;
        letter-spacing: 4px;
        font-weight: 700;
    }

    .section-heading h2 {
        margin: 9px 0;
        color: #3c4139;
        font-size: 36px;
    }

    .section-heading p {
        max-width: 760px;
        margin: auto;
        color: #3f3f3f;
        font-size: 16px;
        font-weight: 500;
        line-height: 1.9;
    }

    /* 卡片 */
    .content-card {
        height: 100%;
        padding: 28px;
        background: white;
        border: 1px solid #e1dbcf;
        border-radius: 6px;
        box-shadow: 0 8px 25px rgba(60, 55, 45, 0.05);
    }

    .content-card h3 {
        margin-top: 4px;
        color: #43483f;
    }

    .content-card p {
        color: #71736d;
        line-height: 1.8;
    }

    /* 圖片案例卡 */
    .project-card {
        overflow: hidden;
        margin-bottom: 20px;
        background: white;
        border: 1px solid #dfd9cd;
        border-radius: 6px;
        box-shadow: 0 8px 24px rgba(50, 46, 39, 0.06);
    }

    .project-card img {
        width: 100%;
        height: 250px;
        object-fit: cover;
        display: block;
    }

    .project-content {
        padding: 20px;
    }

    .project-tag {
        color: #9b8061;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
    }

    .project-content h3 {
        margin: 8px 0;
        color: #3d4239;
    }

    .project-content p {
        margin: 5px 0;
        color: #74766f;
        line-height: 1.6;
    }

    /* AI 表單區 */
    .ai-section {
        margin-top: 45px;
        padding: 35px;
        background: #ebe6dc;
        border: 1px solid #d9d1c2;
        border-radius: 7px;
    }

    /* 結果卡 */
    .result-title {
        margin-top: 35px;
        margin-bottom: 20px;
        color: #3f443c;
        font-size: 30px;
        font-weight: 800;
    }

    .price-card {
        min-height: 150px;
        padding: 24px 18px;
        text-align: center;
        color: white;
        background: #50574d;
        border-radius: 6px;
    }

    .price-card .label {
        color: #e7e2d8;
        font-size: 14px;
    }

    .price-card .number {
        margin-top: 13px;
        font-size: 29px;
        font-weight: 800;
    }

    .recommend-box {
        margin-top: 22px;
        padding: 25px;
        background: white;
        border-left: 6px solid #8b7053;
        border-radius: 5px;
    }

    .recommend-box h3 {
        margin-top: 0;
        color: #41463e;
    }

    .recommend-box p,
    .recommend-box li {
        color: #666a62;
        line-height: 1.8;
    }

    .notice-box {
        margin-top: 22px;
        padding: 22px;
        background: #fff8e9;
        border: 1px solid #e6d4ac;
        border-radius: 5px;
        color: #66583e;
        line-height: 1.8;
    }

    /* 設計流程 */
    .flow-step {
        min-height: 160px;
        padding: 23px;
        text-align: center;
        background: white;
        border: 1px solid #ded8cc;
        border-radius: 6px;
    }

    .flow-number {
        width: 42px;
        height: 42px;
        margin: auto;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        background: #858b7c;
        border-radius: 50%;
        font-weight: 800;
    }

    .flow-step h4 {
        color: #41463e;
        margin-bottom: 8px;
    }

    .flow-step p {
        color: #75776f;
        font-size: 14px;
        line-height: 1.6;
    }

    /* 聯絡區 */
    .contact-box {
        padding: 32px;
        color: white;
        background: #454b42;
        border-radius: 6px;
    }

    .contact-box h3 {
        margin-top: 0;
        color: white;
    }

    .contact-box p {
        color: #e7e4dc;
        line-height: 1.8;
    }

    /* Streamlit 元件 */
    div.stButton > button,
    div.stFormSubmitButton > button {
        min-height: 48px;
        color: white;
        background-color: #596052;
        border: none;
        border-radius: 3px;
        font-size: 16px;
        font-weight: 700;
    }

    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover {
        color: white;
        background-color: #41473d;
        border: none;
    }

    div[data-testid="stMetric"] {
        padding: 18px;
        background: white;
        border: 1px solid #ded8cc;
        border-radius: 5px;
    }

    @media (max-width: 850px) {
        .navbar {
            display: block;
            padding: 14px;
        }

        .navbar-logo {
            margin-bottom: 12px;
        }

        .navbar-links {
            justify-content: flex-start;
            gap: 10px 15px;
        }

        .navbar-links a {
            font-size: 12px;
        }

        .hero {
            min-height: 540px;
            padding: 55px 25px;
        }

        .hero h1 {
            font-size: 39px;
        }

        .hero p {
            font-size: 16px;
        }

        .section-heading h2 {
            font-size: 29px;
        }

        .project-card img {
            height: 220px;
        }
    }

    /* ========================= */
    /* Streamlit 表單修正 */
    /* ========================= */

    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #222222 !important;
    }

    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #222222 !important;
    }

    .stTextInput label,
    .stNumberInput label,
    .stSelectbox label,
    .stTextArea label {
        color: #333333 !important;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# 上方導覽列
# =========================
st.markdown(
    """
    <div class="navbar">
        <div class="navbar-logo">築居 AI DESIGN</div>
        <div class="navbar-links">
            <a href="#home">首頁</a>
            <a href="#about">關於我們</a>
            <a href="#ai-plan">AI 智慧規劃</a>
            <a href="#new-home">新屋案例</a>
            <a href="#old-home">舊屋翻新</a>
            <a href="#portfolio">作品集</a>
            <a href="#process">設計流程</a>
            <a href="#booking">預約設計</a>
            <a href="#contact">聯絡我們</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# 首頁
# =========================
st.markdown('<div id="home" class="section-anchor"></div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="hero">
        <div class="hero-content">
            <div class="hero-small">AI × INTERIOR DESIGN</div>
            <h1>讓理想生活<br>從合理預算開始</h1>
            <p>
                結合 AI 初步預算評估與專業現場服務，
                根據房屋條件、預算上限及生活需求，
                為您推薦合適的裝修方向。
            </p>
            <a class="hero-button" href="#ai-plan">立即開始 AI 規劃</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# 關於我們
# =========================
st.markdown('<div id="about" class="section-anchor"></div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="section-heading">
        <div class="section-label">ABOUT US</div>
        <h2>關於我們</h2>
        <p>
            我們結合 AI 預算分析與室內設計服務，
            讓客戶在裝修初期便能了解預算可行性、適合風格與施工重點。
            AI 負責提供快速的初步規劃，正式報價則由專業人員現場丈量後確認。
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

about_col1, about_col2, about_col3 = st.columns(3)

with about_col1:
    st.markdown(
        """
        <div class="content-card">
            <h3>AI 初步評估</h3>
            <p>
                根據坪數、房屋狀況、預算與客戶需求，
                快速提供裝修費用參考區間。
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with about_col2:
    st.markdown(
        """
        <div class="content-card">
            <h3>預算導向規劃</h3>
            <p>
                先設定預算上限，再推薦基礎整理、標準裝修或完整翻新的執行方向。
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with about_col3:
    st.markdown(
        """
        <div class="content-card">
            <h3>專業現場估價</h3>
            <p>
                可預約專業人員進行丈量與屋況確認，
                再提供正式施工內容與最終報價。
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# AI 智慧規劃
# =========================
st.markdown('<div id="ai-plan" class="section-anchor"></div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="section-heading">
        <div class="section-label">AI PLANNING</div>
        <h2>AI 智慧裝修規劃</h2>
        <p>
            填寫房屋條件、預算上限與生活需求，
            系統將提供初步預算區間、風格推薦與施工建議。
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

with st.container():
    st.markdown('<div class="ai-section">', unsafe_allow_html=True)

    form_col1, form_col2 = st.columns(2, gap="large")

    with form_col1:
        budget = st.number_input(
            "最高裝修預算（NT$）",
            min_value=100000,
            max_value=20000000,
            value=1500000,
            step=100000
        )

        area = st.number_input(
            "室內坪數",
            min_value=5,
            max_value=200,
            value=30,
            step=1
        )

        house_type = st.selectbox(
            "房屋狀況",
            ["新成屋", "中古屋", "老屋翻新"]
        )

    with form_col2:
        position = st.selectbox(
            "裝修定位",
            ["自住住宅", "出租住宅", "商業空間"]
        )

        family = st.selectbox(
            "主要使用人數",
            ["1 人", "2 人", "3～4 人", "5 人以上"]
        )

        priorities = st.multiselect(
            "最重視的項目（可複選）",
            [
                "收納空間",
                "客廳空間",
                "廚房機能",
                "浴室更新",
                "臥室舒適",
                "自然採光",
                "隔音效果",
                "智慧家居",
                "耐用性",
                "整體美觀"
            ],
            default=["收納空間", "整體美觀"]
        )

    analyze = st.button(
        "產生 AI 初步裝修規劃",
        use_container_width=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# AI 分析結果
# =========================
if analyze:
    # 模型仍需要原始訓練欄位，因此在後台設定固定值，
    # 但不讓客戶選擇或看見「材料等級」。
    hidden_quality = "標準型"

    demolition = "否" if house_type == "新成屋" else "是"

    if house_type == "新成屋":
        difficulty = "低"
        uncertainty_rate = 0.08
    elif house_type == "中古屋":
        difficulty = "中"
        uncertainty_rate = 0.12
    else:
        difficulty = "高"
        uncertainty_rate = 0.18

    input_data = pd.DataFrame(
        {
            "工程類型": ["室內裝修"],
            "工程坪數": [area],
            "品質等級": [hidden_quality],
            "是否需要拆除": [demolition],
            "工程難度": [difficulty]
        }
    )

    input_data = pd.get_dummies(input_data)
    input_data = input_data.reindex(
        columns=model_columns,
        fill_value=0
    )

    center_estimate = float(model.predict(input_data)[0])

    lower_estimate = center_estimate * (1 - uncertainty_rate)
    upper_estimate = center_estimate * (1 + uncertainty_rate)

    budget_difference = budget - center_estimate
    budget_per_ping = budget / area

    # 預算方案
    if budget < lower_estimate:
        budget_plan = "基礎整理方案"
        plan_description = (
            "建議以必要工程及最重視的空間為優先，"
            "保留可正常使用的設備與原有格局，降低拆除及重作費用。"
        )
    elif budget <= upper_estimate * 1.08:
        budget_plan = "標準實用裝修"
        plan_description = (
            "預算與目前初步估算接近，適合進行主要空間裝修，"
            "並依需求排序分配系統櫃、地板、燈光及局部水電預算。"
        )
    else:
        budget_plan = "完整整體規劃"
        plan_description = (
            "目前預算較充足，可進行較完整的空間整合，"
            "包含收納、燈光、地板、天花板及重點設備升級。"
        )

    # 風格推薦
    if position == "出租住宅":
        recommended_style = "現代簡約風"
        style_reason = "線條簡潔、容易維護，能兼顧耐用性與出租市場接受度。"
    elif position == "商業空間":
        recommended_style = "現代質感風"
        style_reason = "可強化空間識別度與視覺焦點，適合塑造商業形象。"
    elif "自然採光" in priorities or "整體美觀" in priorities:
        recommended_style = "北歐自然風"
        style_reason = "以淺色、木質與自然採光為核心，空間明亮且適合自住。"
    elif "收納空間" in priorities:
        recommended_style = "無印機能風"
        style_reason = "適合搭配整合式系統櫃，兼顧收納與整體視覺。"
    else:
        recommended_style = "現代簡約風"
        style_reason = "設計彈性高，可依預算調整材料與施工範圍。"

    # 建議施工
    construction_items = []

    if "收納空間" in priorities:
        construction_items.append("規劃玄關櫃、電視櫃及臥室系統收納")
    if "客廳空間" in priorities:
        construction_items.append("改善客廳照明、動線與主要視覺牆面")
    if "廚房機能" in priorities:
        construction_items.append("優先改善廚房收納、工作檯面與使用動線")
    if "浴室更新" in priorities:
        construction_items.append("檢查防水、衛浴設備及乾濕分離需求")
    if "臥室舒適" in priorities:
        construction_items.append("改善臥室照明、收納與插座配置")
    if "自然採光" in priorities:
        construction_items.append("採用淺色牆面並減少遮擋採光的固定隔間")
    if "隔音效果" in priorities:
        construction_items.append("評估隔音門窗、牆面或天花板改善方式")
    if "智慧家居" in priorities:
        construction_items.append("預留智慧燈光、網路與電源控制線路")
    if "耐用性" in priorities:
        construction_items.append("優先採用耐磨、易清潔及容易維護的表面材質")
    if "整體美觀" in priorities:
        construction_items.append("統一色彩、燈光與櫃體線條，提升整體一致性")

    if not construction_items:
        construction_items = [
            "以基礎水電安全、牆面整理與主要生活空間為優先"
        ]

    # 保留項目建議
    saving_text = ""

    if house_type == "新成屋":
        saving_text = (
            "建議保留建商原有廚房及可正常使用的衛浴設備，"
            "可減少拆除與重作費用。若保留原有廚房，"
            "初步可節省約 NT$180,000。"
        )
    elif house_type == "中古屋":
        saving_text = (
            "建議先檢查原有廚房、室內門及地板狀況。"
            "可正常使用的項目優先保留，將預算集中在水電安全與主要需求。"
        )
    else:
        saving_text = (
            "老屋翻新應先確認水電、漏水與結構狀況。"
            "不建議只為節省預算而保留有安全疑慮的管線或設備。"
        )

    st.markdown(
        '<div class="result-title">AI 初步預算評估</div>',
        unsafe_allow_html=True
    )

    result_col1, result_col2, result_col3 = st.columns(3)

    with result_col1:
        st.markdown(
            f"""
            <div class="price-card">
                <div class="label">客戶預算上限</div>
                <div class="number">NT$ {budget:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with result_col2:
        st.markdown(
            f"""
            <div class="price-card">
                <div class="label">裝修費用參考區間</div>
                <div class="number">
                    NT$ {lower_estimate:,.0f}<br>
                    ～ {upper_estimate:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with result_col3:
        st.markdown(
            f"""
            <div class="price-card">
                <div class="label">每坪可用預算</div>
                <div class="number">NT$ {budget_per_ping:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        f"""
        <div class="recommend-box">
            <h3>預算可行性分析｜{budget_plan}</h3>
            <p>{plan_description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if budget_difference >= 0:
        st.success(
            f"目前預算高於初步中心估算約 NT$ {budget_difference:,.0f}，"
            "可保留部分金額作為現場追加工程及備用預算。"
        )
    else:
        st.warning(
            f"目前預算低於初步中心估算約 NT$ {abs(budget_difference):,.0f}，"
            "建議縮小施工範圍或保留部分現有設備。"
        )

    result_left, result_right = st.columns(2, gap="large")

    with result_left:
        priority_html = "".join(
            f"<li>{item}</li>" for item in priorities
        )

        st.markdown(
            f"""
            <div class="recommend-box">
                <h3>AI 風格推薦</h3>
                <p><b>{recommended_style}</b></p>
                <p>{style_reason}</p>
                <p><b>客戶重視項目：</b></p>
                <ul>{priority_html}</ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    with result_right:
        construction_html = "".join(
            f"<li>{item}</li>" for item in construction_items
        )

        st.markdown(
            f"""
            <div class="recommend-box">
                <h3>建議施工方向</h3>
                <ul>{construction_html}</ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        f"""
        <div class="recommend-box">
            <h3>建議保留項目</h3>
            <p>{saving_text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="notice-box">
            <b>此結果為 AI 初步預算評估。</b><br>
            實際報價仍須依現場丈量、屋況、材料與施工方式確認。<br>
            AI 提供裝修費用參考區間與預算可行性分析，
            現場評估後再由專業人員提供正式報價。
        </div>
        """,
        unsafe_allow_html=True
    )

    action_col1, action_col2 = st.columns(2)

    with action_col1:
        if st.button(
            "預約免費初步諮詢",
            use_container_width=True,
            key="consult_button"
        ):
            st.info("請前往下方「預約設計」填寫聯絡資料。")

    with action_col2:
        if st.button(
            "安排專業人員現場估價",
            use_container_width=True,
            key="estimate_button"
        ):
            st.info("請前往下方「預約設計」，選擇現場估價服務。")

# =========================
# 新屋案例
# =========================
st.markdown('<div id="new-home" class="section-anchor"></div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="section-heading">
        <div class="section-label">NEW HOME PROJECTS</div>
        <h2>新屋案例</h2>
        <p>
            針對新成屋進行格局優化、收納整合與風格設計，
            在保留現有設備的情況下提升空間完整度。
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

new1, new2, new3 = st.columns(3)

new_home_projects = [
    {
        "image": "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1000&q=80",
        "tag": "新成屋｜北歐風",
        "title": "光影木質宅",
        "info": "高雄｜28 坪｜三房兩廳",
        "description": "以淺木色、白色與自然採光，打造溫暖且具有收納機能的居住空間。"
    },
    {
        "image": "https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?auto=format&fit=crop&w=1000&q=80",
        "tag": "新成屋｜現代風",
        "title": "城市質感宅",
        "info": "高雄｜35 坪｜三房兩廳",
        "description": "使用俐落線條與中性色調，整合客廳、餐廳及展示收納空間。"
    },
    {
        "image": "https://images.unsplash.com/photo-1600210491892-03d54c0aaf87?auto=format&fit=crop&w=1000&q=80",
        "tag": "新成屋｜無印風",
        "title": "日常留白",
        "info": "台南｜24 坪｜兩房兩廳",
        "description": "透過簡潔櫃體與柔和配色，保留彈性空間並提升日常生活機能。"
    }
]

for column, project in zip([new1, new2, new3], new_home_projects):
    with column:
        st.markdown(
            f"""
            <div class="project-card">
                <img src="{project['image']}">
                <div class="project-content">
                    <div class="project-tag">{project['tag']}</div>
                    <h3>{project['title']}</h3>
                    <p><b>{project['info']}</b></p>
                    <p>{project['description']}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================
# 舊屋翻新
# =========================
st.markdown('<div id="old-home" class="section-anchor"></div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="section-heading">
        <div class="section-label">RENOVATION PROJECTS</div>
        <h2>舊屋翻新</h2>
        <p>
            從屋況、水電與動線重新檢視老屋問題，
            透過專業丈量與工程評估，改善安全性及生活品質。
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

old1, old2 = st.columns(2)

with old1:
    st.markdown(
        """
        <div class="project-card">
            <img src="https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1200&q=80">
            <div class="project-content">
                <div class="project-tag">30 年老屋｜全面翻新</div>
                <h3>老宅新生計畫</h3>
                <p><b>高雄｜32 坪｜水電與格局重新規劃</b></p>
                <p>
                    更新老舊管線、改善採光與動線，
                    並透過開放式公共空間提升住宅使用效率。
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with old2:
    st.markdown(
        """
        <div class="project-card">
            <img src="https://images.unsplash.com/photo-1600566753051-f0b89df2dd90?auto=format&fit=crop&w=1200&q=80">
            <div class="project-content">
                <div class="project-tag">中古屋｜局部翻新</div>
                <h3>機能更新住宅</h3>
                <p><b>高雄｜26 坪｜廚房、浴室及收納更新</b></p>
                <p>
                    保留狀況良好的原有項目，
                    將預算集中於廚房、衛浴、水電安全與收納機能。
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# 作品集
# =========================
st.markdown('<div id="portfolio" class="section-anchor"></div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="section-heading">
        <div class="section-label">PORTFOLIO</div>
        <h2>作品集</h2>
        <p>
            從空間機能、居住習慣到視覺風格，
            依照不同需求規劃具有個人特色的生活場景。
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

portfolio_images = [
    (
        "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=1000&q=80",
        "現代簡約｜客廳設計"
    ),
    (
        "https://images.unsplash.com/photo-1600566753199-17f0baa2a6c3?auto=format&fit=crop&w=1000&q=80",
        "自然木質｜餐廳設計"
    ),
    (
        "https://images.unsplash.com/photo-1600566752355-35792bedcfea?auto=format&fit=crop&w=1000&q=80",
        "沉穩質感｜臥室設計"
    )
]

portfolio_columns = st.columns(3)

for column, (image, title) in zip(portfolio_columns, portfolio_images):
    with column:
        st.markdown(
            f"""
            <div class="project-card">
                <img src="{image}">
                <div class="project-content">
                    <div class="project-tag">PORTFOLIO</div>
                    <h3>{title}</h3>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================
# 設計流程
# =========================
st.markdown('<div id="process" class="section-anchor"></div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="section-heading">
        <div class="section-label">DESIGN PROCESS</div>
        <h2>設計流程</h2>
        <p>
            AI 初步估價作為裝修規劃輔助，
            最終仍由專業人員現場丈量、確認屋況及施工內容後提供正式報價。
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

flow_data = [
    ("01", "填寫需求", "輸入預算、坪數、屋況及重視項目。"),
    ("02", "AI 初步評估", "提供預算區間、風格與施工建議。"),
    ("03", "免費初步諮詢", "由專人聯繫並確認裝修需求。"),
    ("04", "現場丈量", "專業人員確認尺寸、屋況與施工限制。"),
    ("05", "正式報價", "依丈量、材料及施工方式提供完整報價。"),
    ("06", "設計與施工", "確認提案、簽約並進行施工與驗收。")
]

flow_columns_1 = st.columns(3)
flow_columns_2 = st.columns(3)

for column, step in zip(flow_columns_1, flow_data[:3]):
    with column:
        st.markdown(
            f"""
            <div class="flow-step">
                <div class="flow-number">{step[0]}</div>
                <h4>{step[1]}</h4>
                <p>{step[2]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

for column, step in zip(flow_columns_2, flow_data[3:]):
    with column:
        st.markdown(
            f"""
            <div class="flow-step">
                <div class="flow-number">{step[0]}</div>
                <h4>{step[1]}</h4>
                <p>{step[2]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================
# 預約設計
# =========================
st.markdown('<div id="booking" class="section-anchor"></div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="section-heading">
        <div class="section-label">BOOKING</div>
        <h2>預約設計</h2>
        <p>
            填寫基本聯絡資料與裝修需求，
            我們將安排專人進行初步諮詢或現場估價。
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

with st.form("booking_form", clear_on_submit=True):
    booking_col1, booking_col2 = st.columns(2)

    with booking_col1:
        customer_name = st.text_input("姓名")
        customer_phone = st.text_input("聯絡電話")
        customer_email = st.text_input("Email")
        customer_area = st.text_input("裝修地區")

    with booking_col2:
        booking_service = st.selectbox(
            "預約服務",
            ["免費初步諮詢", "安排專業人員現場估價"]
        )

        booking_house = st.selectbox(
            "房屋類型",
            ["新成屋", "中古屋", "老屋翻新", "商業空間"]
        )

        booking_budget = st.selectbox(
            "預算範圍",
            [
                "NT$500,000 以下",
                "NT$500,000～1,000,000",
                "NT$1,000,000～1,500,000",
                "NT$1,500,000～2,500,000",
                "NT$2,500,000 以上"
            ]
        )

        contact_time = st.selectbox(
            "方便聯絡時間",
            ["上午", "下午", "晚上"]
        )

    customer_need = st.text_area(
        "裝修需求說明",
        placeholder="例如：希望增加收納、更新廚房、改善採光等。"
    )

    booking_submit = st.form_submit_button(
        "送出預約資料",
        use_container_width=True
    )

    if booking_submit:
        if not customer_name or not customer_phone:
            st.warning("請至少填寫姓名與聯絡電話。")
        else:
            st.success(
                f"{customer_name}，您的預約資料已送出。"
                f"預約項目：{booking_service}。"
            )
            st.caption(
                "此網站為專題展示版本，目前不會真的將資料寄送給設計公司。"
            )

# =========================
# 聯絡我們
# =========================
st.markdown('<div id="contact" class="section-anchor"></div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="section-heading">
        <div class="section-label">CONTACT</div>
        <h2>聯絡我們</h2>
        <p>
            歡迎與我們聯繫，進一步了解裝修規劃及現場評估服務。
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

contact_col1, contact_col2 = st.columns([1, 1])

with contact_col1:
    st.markdown(
        """
        <div class="contact-box">
            <h3>築居 AI 室內設計</h3>
            <p>
                電話：07-123-4567<br>
                Email：service@example.com<br>
                服務地區：高雄、台南及鄰近地區<br>
                服務時間：週一至週六 09:00～18:00
            </p>
            <p>
                本網站為 Python 與 AI 應用專題展示，
                聯絡資訊及案例內容皆為示意資料。
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with contact_col2:
    st.markdown(
        """
        <div class="content-card">
            <h3>服務說明</h3>
            <p>
                AI 初步評估可以協助客戶快速了解可能的裝修預算與方向，
                但無法取代現場丈量與專業工程判斷。
            </p>
            <p>
                正式報價將依實際尺寸、屋況、施工項目、材料規格與工法確認。
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# 頁尾
# =========================
st.markdown(
    """
    <div style="
        margin-top:55px;
        padding:28px;
        text-align:center;
        color:#dcd8cf;
        background:#373c35;
        border-radius:5px;
    ">
        築居 AI 室內設計平台<br>

        <span style="font-size:13px;">
            AI 初步預算評估不等同於正式工程報價
        </span>
    </div>
    """,
    unsafe_allow_html=True
)
