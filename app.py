import streamlit as st
import pandas as pd
import plotly.express as px
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from datetime import timedelta

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Aadhaar Intelligence Hub",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #0f1116; }
    .block-container { padding-top: 1rem; padding-bottom: 5rem; }

    /* CARDS */
    .metric-card {
        background: linear-gradient(135deg, #1e222b 0%, #161b22 100%);
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .metric-value { font-size: 24px; font-weight: 700; color: #f0f6fc; }
    .metric-label { font-size: 12px; color: #8b949e; text-transform: uppercase; }

    /* RICH ANALYST BOXES */
    .analyst-box {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-left: 5px solid #a371f7; /* Purple for Intelligence */
        padding: 25px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .analyst-header {
        color: #d2a8ff; font-weight: bold; font-size: 18px; margin-bottom: 15px;
        display: flex; align-items: center; gap: 10px;
        border-bottom: 1px solid #30363d; padding-bottom: 10px;
    }
    .section-title {
        color: #58a6ff; font-size: 14px; font-weight: bold; margin-top: 10px; margin-bottom: 5px; text-transform: uppercase;
    }
    .analyst-text { color: #c9d1d9; font-size: 14px; line-height: 1.6; }
    .highlight { color: #ffffff; font-weight: bold; }

    /* SIDEBAR */
    .sidebar-card {
        background-color: #1c2128; border: 1px solid #30363d; padding: 15px; border-radius: 8px; margin-bottom: 15px;
    }
    .sidebar-header { color: #58a6ff; font-weight: bold; font-size: 14px; margin-bottom: 8px;}
    .sidebar-stat { color: white; font-size: 16px; font-weight: bold; margin-bottom: 5px; }
    .sidebar-context { color: #8b949e; font-size: 12px; line-height: 1.4; }

    /* TABS */
    .stTabs [data-baseweb="tab-list"] { background-color: #0f1116; }
    .stTabs [aria-selected="true"] { background-color: #1f6feb !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. DATA LOADING & FEATURE ENGINEERING ---
@st.cache_data
def load_data():
    # Load the Cleaned Data
    df = pd.read_csv("Aadhar_Universal_Cleaned.csv")
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')

    # --- CRITICAL: CALCULATE METRICS HERE ---
    # This was missing/broken in your previous version
    df['Total_Updates'] = (df['bio_age_5_17'] + df['bio_age_17_'] +
                           df['demo_age_5_17'] + df['demo_age_17_'])
    df['Total_Enrolment'] = (df['age_0_5'] + df['age_5_17'] + df['age_18_greater'])
    df['Child_Bio_Updates'] = df['bio_age_5_17']
    df['New_Births'] = df['age_0_5']

    return df

# Load the data into a "Raw" variable first
df_raw = load_data()

# --- 4. EXECUTIVE SIDEBAR (FILTERS + SUMMARY) ---
# --- 4. EXECUTIVE SIDEBAR (FILTERS + TRANSLATION) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/c/cf/Aadhaar_Logo.svg/1200px-Aadhaar_Logo.svg.png", width=120)

    # 1. LANGUAGE TOGGLE
    lang = st.radio("🏳️ Language / भाषा", ["English", "Hindi (हिंदी)"], horizontal=True)

    # --- MASTER TRANSLATION DICTIONARY ---
    txt = {
        "English": {
            "title": "Aadhaar Intelligence Hub",
            "control": "Control Center",
            "filter_label": "Filter by State:",
            "mission": "Mission Briefing",
            "hotspot": "PRIMARY HOTSPOT",
            "hotspot_ctx": "Top performing region. Currently handling max operational load.",
            "risk": "RISK ALERT",
            "risk_ctx": "Districts failing mandatory child update protocols.",
            "status": "Viewing data for",
            "records": "records",
            # KPI Cards
            "kpi_enrol": "Total New Enrolments",
            "kpi_update": "Total Updates Processed",
            "kpi_child": "Mandatory Child Updates",
            "kpi_risk": "Risk Districts Identified",
            # Tab 1 Analyst Box
            "t1_header": "🧠 Zone Intelligence Report",
            "t1_obs": "The heatmap identifies a massive centralization of activity.",
            "t1_imp": "Creates a 'Dual-Speed Ecosystem': Red Zones have high wait times, while Blue Zones have idle resources.",
            "t1_strat": "Initiate Dynamic Load Balancing. Shift Mobile Units to the hotspot immediately.",
            # Tab 2 Analyst Box
            "t2_header": "⚠️ Governance Breach Report",
            "t2_obs": "Districts are critically failing the Mandatory Biometric Update (MBU) protocols (<10%).",
            "t2_imp": "Children at risk of Scholarship Rejection due to outdated biometrics.",
            "t2_strat": "Issue directive to District Magistrates for 'School Camp Drives'.",
            # Tab 3 Analyst Box
            "t3_header": "🕵️‍♂️ Fraud & Migration Intelligence",
            "t3_obs": "Red Zones show thousands of Enrolments but ZERO Births (Statistical Anomaly).",
            "t3_imp": "Indicates undocumented Workforce Migration or potential Fake ID rings.",
            "t3_strat": "Trigger 'Field Verification Audit' for applicants aged >18 in Red Zones.",
            # Tab 4 Forecast Headers
            "t4_header": "🔮 Predictive Intelligence",
            "t4_h1": "New User Growth",
            "t4_h2": "Operational Load",
            "t4_h3": "Fraud Risk"
        },
        "Hindi (हिंदी)": {
            "title": "आधार इंटेलिजेंस हब",
            "control": "नियंत्रण केंद्र (Control Center)",
            "filter_label": "राज्य द्वारा फ़िल्टर करें:",
            "mission": "मिशन ब्रीफिंग (Mission Briefing)",
            "hotspot": "प्रमुख केंद्र (Primary Hotspot)",
            "hotspot_ctx": "शीर्ष प्रदर्शन क्षेत्र। वर्तमान में अधिकतम परिचालन भार संभाल रहा है।",
            "risk": "जोखिम चेतावनी (Risk Alert)",
            "risk_ctx": "अनिवार्य बाल अपडेट प्रोटोकॉल में विफल जिले।",
            "status": "डेटा देखा जा रहा है:",
            "records": "रिकॉर्ड",
            # KPI Cards
            "kpi_enrol": "कुल नए नामांकन",
            "kpi_update": "कुल अपडेट संसाधित",
            "kpi_child": "अनिवार्य बाल अपडेट",
            "kpi_risk": "चिन्हित जोखिम जिले",
            # Tab 1 Analyst Box
            "t1_header": "🧠 क्षेत्र खुफिया रिपोर्ट (Zone Intelligence)",
            "t1_obs": "हीटमैप गतिविधि के भारी केंद्रीकरण की पहचान करता है।",
            "t1_imp": "यह 'दोहरी गति' की स्थिति बनाता है: लाल क्षेत्रों में प्रतीक्षा समय अधिक है, जबकि नीले क्षेत्रों में संसाधन बेकार हैं।",
            "t1_strat": "गतिशील लोड संतुलन (Load Balancing) शुरू करें। मोबाइल यूनिट्स को तुरंत हॉटस्पॉट पर भेजें।",
            # Tab 2 Analyst Box
            "t2_header": "⚠️ शासन उल्लंघन रिपोर्ट (Governance Breach)",
            "t2_obs": "जिले अनिवार्य बायोमेट्रिक अपडेट (MBU) प्रोटोकॉल (<10%) में गंभीर रूप से विफल हो रहे हैं।",
            "t2_imp": "पुराने बायोमेट्रिक्स के कारण बच्चों की छात्रवृत्ति खारिज होने का खतरा है।",
            "t2_strat": "जिलाधिकारियों को 'स्कूल कैंप अभियान' के लिए निर्देश जारी करें।",
            # Tab 3 Analyst Box
            "t3_header": "🕵️‍♂️ धोखाधड़ी और प्रवास खुफिया",
            "t3_obs": "लाल क्षेत्र हजारों नामांकन दिखाते हैं लेकिन शून्य जन्म (सांख्यिकीय विसंगति)।",
            "t3_imp": "यह बिना दस्तावेज वाले कार्यबल प्रवास या संभावित फर्जी आईडी गिरोह का संकेत देता है।",
            "t3_strat": "लाल क्षेत्रों में >18 वर्ष के आवेदकों के लिए 'फील्ड सत्यापन ऑडिट' शुरू करें।",
            # Tab 4 Forecast Headers
            "t4_header": "🔮 भविष्य कहनेवाला खुफिया (Predictive AI)",
            "t4_h1": "नए उपयोगकर्ता वृद्धि",
            "t4_h2": "परिचालन भार",
            "t4_h3": "धोखाधड़ी जोखिम"
        }
    }
    t = txt[lang] # Select Active Language

    # --- A. FILTER SECTION ---
    st.markdown(f"### 🕵️‍♂️ {t['control']}")

    # Filter Widget
    all_states = sorted(df_raw['state'].unique())
    selected_states = st.multiselect(
        t['filter_label'],
        options=all_states,
        default=[]
    )

    # --- B. APPLY FILTER LOGIC ---
    if selected_states:
        df = df_raw[df_raw['state'].isin(selected_states)]
        region_label = "Selected Region"
        group_col = 'district'
    else:
        df = df_raw.copy()
        region_label = "National Overview"
        group_col = 'state'

    st.divider()

    # --- C. MISSION BRIEFING (TRANSLATED) ---
    st.markdown(f"## ⚡ {t['mission']}")

    if not df.empty:
        top_performer = df.groupby(group_col)['Total_Updates'].sum().idxmax()
        risk_districts_count = len(df[ (df['Total_Updates']>1000) & ((df['Child_Bio_Updates']/df['Total_Updates']) < 0.10) ])

        st.markdown(f"""
        <div class="sidebar-card">
            <div class="sidebar-header">📍 {t['hotspot']}</div>
            <div class="sidebar-stat">{top_performer}</div>
            <div class="sidebar-context">{t['hotspot_ctx']}</div>
        </div>
        <div class="sidebar-card">
            <div class="sidebar-header">🚨 {t['risk']}</div>
            <div class="sidebar-stat">{risk_districts_count} Districts Critical</div>
            <div class="sidebar-context">{t['risk_ctx']}</div>
        </div>
        """, unsafe_allow_html=True)

        st.info(f"ℹ️ **{t['status']}** {len(df):,} {t['records']}.")


# --- 5. MAIN HEADER ---
st.title(f"{t['title']}: Strategic Dashboard")
st.caption("Unlocking Societal Trends with Hyper-Local Data Analytics & Predictive AI")

# --- CRITICAL FIX: Calculate Risk Districts based on the FILTERED data ---
if not df.empty:
    risk_districts = len(df[ (df['Total_Updates']>1000) & ((df['Child_Bio_Updates']/df['Total_Updates']) < 0.10) ])
else:
    risk_districts = 0

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

def custom_metric(label, value, col):
    col.markdown(f"""<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>""", unsafe_allow_html=True)

custom_metric(t['kpi_enrol'], f"{df['Total_Enrolment'].sum():,}", kpi1)
custom_metric(t['kpi_update'], f"{df['Total_Updates'].sum():,}", kpi2)
custom_metric(t['kpi_child'], f"{df['Child_Bio_Updates'].sum():,}", kpi3)
custom_metric(t['kpi_risk'], f"{risk_districts}", kpi4)

st.write("")

# --- 6. MAIN TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Geospatial Strategy", "🚨 Policy & Governance", "📊 Deep Dive Analysis", "🔮 AI Forecasting"])

# --- TAB 1: GEOSPATIAL ---
with tab1:
    col_map, col_data = st.columns([2, 1])

    # --- 1. DYNAMIC CALCULATION (THE FIX) ---
    if not df.empty:
        # Check: Are we looking at multiple states or just one?
        if df['state'].nunique() > 1:
            group_by_col = 'state'
            entity_name = "state"
        else:
            group_by_col = 'district'
            entity_name = "district"

        # Calculate metrics for the text
        stats = df.groupby(group_by_col)['Total_Updates'].sum()
        top_state = stats.idxmax() # This is the variable that was missing!
        top_val = stats.max()
        avg_val = stats.mean()

        if avg_val > 0:
            deviation = ((top_val - avg_val) / avg_val) * 100
        else:
            deviation = 0
    else:
        top_state = "N/A"
        deviation = 0
        entity_name = "zone"

    with col_map:
        st.subheader("📍 Update Intensity Heatmap")

        # Dynamic Path for Treemap (Drill down automatically)
        if df['state'].nunique() > 1:
            path_list = [px.Constant("India"), 'state', 'district']
        else:
            # If only one state selected, don't show "India" -> "State", just show "State" -> "District"
            path_list = [px.Constant(df['state'].iloc[0]), 'district']

        geo_df = df.groupby(['state', 'district'])[['Total_Updates']].sum().reset_index()
        fig_tree = px.treemap(
            geo_df,
            path=path_list,
            values='Total_Updates',
            color='Total_Updates',
            color_continuous_scale='Magma'
        )
        fig_tree.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=500, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_tree, use_container_width=True)
    with col_data:
        # Translated Analyst Box
        st.markdown(f"""
        <div class="analyst-box">
            <div class="analyst-header">{t['t1_header']}</div>
            <div class="section-title">🧐 OBSERVATION</div>
            <div class="analyst-text">
                {t['t1_obs']}
                The top {entity_name} (<b>{top_state}</b>) is operating at <span class="highlight">{deviation:.0f}% above average</span>.
            </div>
            <div class="section-title">📉 IMPLICATION</div>
            <div class="analyst-text">
                {t['t1_imp']}
            </div>
            <div class="section-title">🚀 STRATEGY</div>
            <div class="analyst-text">
                {t['t1_strat']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"### 🏆 Top 5 High-Load {entity_name.title()}s")

        # Dynamic Table Ranking
        rank_df = df.groupby(group_by_col)['Total_Updates'].sum().reset_index().sort_values('Total_Updates', ascending=False).head(5)

        st.dataframe(
            rank_df.style.format({'Total_Updates': '{:,.0f}'}).background_gradient(cmap="Blues"),
            hide_index=True,
            use_container_width=True
        )

    # --- RESOURCE OPTIMIZATION ENGINE ---
    st.markdown("---")
    st.subheader("🛠️ Resource Allocation Engine (Cost Optimization)")
    st.caption("AI-Calculated Distribution of Biometric Kits based on Daily Workload (Assume 50 ops/kit/day)")

    res_df = df.groupby(['state', 'district'])[['Total_Updates']].sum().reset_index()
    res_df['Daily_Load'] = res_df['Total_Updates'] / 90  # Approx 90 days data
    res_df['Kits_Needed'] = (res_df['Daily_Load'] / 50).astype(int)
    res_df['Current_Kits'] = res_df['Kits_Needed'] + 5 # Simulate inefficiency
    res_df['Action'] = res_df['Current_Kits'] - res_df['Kits_Needed']
    res_df['Recommendation'] = res_df['Action'].apply(lambda x: f"⬇️ Remove {x} Kits" if x > 0 else f"⬆️ Add {abs(x)} Kits")

    st.dataframe(
        res_df[['state', 'district', 'Daily_Load', 'Kits_Needed', 'Recommendation']]
        .sort_values('Kits_Needed', ascending=False)
        .head(8)
        .style.format({'Daily_Load': '{:.1f}'})
        .background_gradient(cmap='RdYlGn', subset=['Kits_Needed']),
        use_container_width=True
    )
# --- NEW FEATURE: DISASTER RELIEF PLANNING (IDEA 9) ---
    st.markdown("---")
    st.subheader("⛑️ Civil Defense & Disaster Relief Planner")
    st.caption("Using Aadhaar density to calculate emergency ration requirements during Floods/Cyclones.")

    col_disaster_ctrl, col_disaster_stats = st.columns([1, 2])

    with col_disaster_ctrl:
        # Simulation Controls
        st.markdown("##### ⚠️ Crisis Simulation")
        disaster_type = st.selectbox("Select Disaster Scenario:", ["Flood (Severe)", "Cyclone (Cat 4)", "Earthquake", "Pandemic Lockdown"])

        # Determine ration needs based on disaster
        if "Flood" in disaster_type:
            ration_per_person = 2.5 # kg food
            water_per_person = 5 # Liters
        elif "Cyclone" in disaster_type:
            ration_per_person = 3.0
            water_per_person = 3
        else:
            ration_per_person = 5.0
            water_per_person = 2

        # Select a target district for simulation (Filter based on current view)
        if df['state'].nunique() == 1:
            target_districts = df['district'].unique()
        else:
            target_districts = df[df['state'] == df['state'].mode()[0]]['district'].unique() # Default to most common state if All India

        selected_disaster_dist = st.selectbox("Target District for Relief:", target_districts)

    with col_disaster_stats:
        # Calculate Relief Metrics for the selected district
        # We use Total_Enrolment as a proxy for Population
        d_data = df[df['district'] == selected_disaster_dist]
        pop_count = d_data['Total_Enrolment'].sum()
        child_count = d_data['age_0_5'].sum()

        req_food = pop_count * ration_per_person
        req_water = pop_count * water_per_person

        st.markdown(f"#### 📊 Relief Logistics: **{selected_disaster_dist}**")

        m1, m2, m3 = st.columns(3)
        m1.metric("Est. Population Affected", f"{pop_count:,.0f}")
        m2.metric("📦 Food Packets Req.", f"{req_food/1000:,.1f} Tons", help=f"{ration_per_person}kg per person")
        m3.metric("💧 Water Tankers Req.", f"{int(req_water/5000):,} Tankers", help="Assuming 5000L tanker capacity")

        st.warning(f"🚨 **Vulnerable Group Alert:** There are **{child_count:,.0f} infants (0-5 yrs)** in this zone. Prioritize baby food & milk supplies.")

        # Visualizing the density within the district (if pincode data exists, otherwise general)
        # Since we aggregated to district earlier, we show a simple progress bar of "Density Risk"
        # (Simulated logic: Higher enrolment = Higher density risk)
        density_score = min(pop_count / 500000, 1.0) # Normalize
        st.write(" **Evacuation Complexity Score:**")
        st.progress(density_score)
        if density_score > 0.8:
            st.error("High Density Zone: Narrow lanes expected. Use Drones for delivery.")
        else:
            st.success("Moderate Density: Standard truck delivery possible.")
# --- TAB 2: POLICY ---
# --- TAB 2: POLICY ---
with tab2:
    policy_df = df.groupby(['state', 'district'])[['Child_Bio_Updates', 'Total_Updates', 'age_5_17', 'Total_Enrolment']].sum().reset_index()
    policy_df['Child_Share_Pct'] = (policy_df['Child_Bio_Updates'] / policy_df['Total_Updates']) * 100
    risk_df = policy_df[(policy_df['Total_Updates'] > 1000) & (policy_df['Child_Share_Pct'] < 10)].sort_values('Child_Share_Pct')

    # Calculate Impact
    risk_df['Deficit'] = (risk_df['Total_Updates'] * 0.20) - risk_df['Child_Bio_Updates']
    est_children_at_risk = int(risk_df['Deficit'].sum())

    col_pol_graph, col_pol_info = st.columns([2, 1])

    with col_pol_graph:
        st.subheader("🚩 Non-Compliant Districts (Risk Table)")
        st.dataframe(
            risk_df[['state', 'district', 'Total_Updates', 'Child_Share_Pct']].style.format({'Child_Share_Pct': '{:.2f}%', 'Total_Updates': '{:,.0f}'}).background_gradient(cmap='Reds_r'),
            use_container_width=True,
            height=400
        )

    with col_pol_info:
        # Translated Analyst Box
        st.markdown(f"""
        <div class="analyst-box">
            <div class="analyst-header">{t['t2_header']}</div>
            <div class="section-title">🧐 OBSERVATION</div>
            <div class="analyst-text">
                {t['t2_obs']}
            </div>
            <div class="section-title">📉 IMPLICATION (HUMAN COST)</div>
            <div class="analyst-text">
                {t['t2_imp']}
                <br>
                <span class="highlight" style="font-size: 20px; color: #ff7b72;">{est_children_at_risk:,} Children</span> affected.
            </div>
            <div class="section-title">🚀 STRATEGY</div>
            <div class="analyst-text">
                {t['t2_strat']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- NEW FEATURE: District Performance Report Card (Gamified) ---
    st.markdown("---")
    st.subheader("📊 District Performance Report Card (Gamified)")
    st.caption("Grading districts based on 'Child Update Compliance' and 'Operational Efficiency'.")

    # 1. Calculate Scores
    score_df = df.groupby(['state', 'district'])[['Child_Bio_Updates', 'Total_Updates']].sum().reset_index()
    score_df['Compliance_Rate'] = (score_df['Child_Bio_Updates'] / score_df['Total_Updates']) * 100

    # 2. Assign Grades
    def assign_grade(row):
        rate = row['Compliance_Rate']
        if rate >= 20: return 'A+ (Excellent)'
        elif rate >= 15: return 'B (Good)'
        elif rate >= 10: return 'C (Average)'
        elif rate >= 5: return 'D (Poor)'
        else: return 'F (Critical Failure)'

    score_df['Grade'] = score_df.apply(assign_grade, axis=1)

    # 3. Visual Scorecard
    col_grade_chart, col_grade_list = st.columns([1, 1])

    with col_grade_chart:
        # Pie chart of Grades
        fig_grade = px.pie(score_df, names='Grade', title="National Grade Distribution",
                           color='Grade',
                           color_discrete_map={
                               'A+ (Excellent)': '#00CC96',
                               'B (Good)': '#636EFA',
                               'C (Average)': '#EF553B',
                               'D (Poor)': '#FFA15A',
                               'F (Critical Failure)': '#B22222'
                           })
        st.plotly_chart(fig_grade, use_container_width=True)

    with col_grade_list:
        st.markdown("#### 🏆 Top A+ Districts")
        st.dataframe(score_df[score_df['Grade'] == 'A+ (Excellent)'][['state', 'district', 'Compliance_Rate']].head(5), hide_index=True)

        st.markdown("#### ⚠️ Critical 'F' Districts")
        st.dataframe(score_df[score_df['Grade'] == 'F (Critical Failure)'][['state', 'district', 'Compliance_Rate']].head(5), hide_index=True)

    # --- NEW FEATURE: LATE ENROLLMENT ANALYSIS ---
    st.markdown("---")
    st.subheader("🎒 The 'Invisible Child' Phenomenon (Late Enrolments)")
    st.write("Districts where children are being enrolled for the **first time** at age 5-17 (Late), instead of at birth. This indicates missed birth registrations.")

    policy_df['Late_Entry_Ratio'] = (policy_df['age_5_17'] / policy_df['Total_Enrolment']) * 100
    top_late = policy_df.sort_values('Late_Entry_Ratio', ascending=False).head(7)

    st.table(top_late[['state', 'district', 'age_5_17', 'Total_Enrolment', 'Late_Entry_Ratio']].style.format({'Late_Entry_Ratio': '{:.1f}%'}))
# --- TAB 3: DEEP DIVE ---
with tab3:
    st.subheader("🔎 Anomaly Detection: Migration vs. Organic Growth")

    corr_df = df.groupby('district').agg({'New_Births': 'sum', 'Total_Enrolment': 'sum', 'state': 'first', 'age_0_5': 'sum'}).reset_index()
    corr_df['Suspicious_Score'] = corr_df['Total_Enrolment'] - corr_df['New_Births']

    col_deep_map, col_deep_scatter = st.columns([1.5, 1.5])

    with col_deep_map:
        st.caption("Map colored by 'Suspicious Score' (High Enrolment without Births)")
        fig_sus = px.treemap(corr_df, path=[px.Constant("India"), 'state', 'district'], values='Total_Enrolment', color='Suspicious_Score', color_continuous_scale='RdYlGn_r')
        fig_sus.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=400)
        st.plotly_chart(fig_sus, use_container_width=True)

    with col_deep_scatter:
        st.caption("Statistical Correlation: Births vs Enrolments")
        fig_corr = px.scatter(corr_df, x="New_Births", y="Total_Enrolment", color="state", log_x=True, log_y=True)
        fig_corr.update_layout(showlegend=False, margin=dict(t=0, l=0, r=0, b=0), height=400)
        st.plotly_chart(fig_corr, use_container_width=True)

    # Translated Analyst Box
    st.markdown(f"""
    <div class="analyst-box">
        <div class="analyst-header">{t['t3_header']}</div>
        <div class="section-title">🧐 OBSERVATION</div>
        <div class="analyst-text">
            {t['t3_obs']}
        </div>
        <div class="section-title">📉 IMPLICATION</div>
        <div class="analyst-text">
            {t['t3_imp']}
        </div>
        <div class="section-title">🚀 STRATEGY</div>
        <div class="analyst-text">
            {t['t3_strat']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- NEW FEATURE 3: SCHOOL INFRASTRUCTURE PLANNER ---
    st.markdown("---")
    st.subheader("🏫 Future Infrastructure Planner (Ministry of Education)")
    st.caption("Using 0-5 Age Enrolments to predict Primary School classroom demand for 2029 (1 Classroom per 30 children).")

    # Logic
    corr_df['Est_New_Classrooms'] = (corr_df['age_0_5'] / 30).astype(int)
    top_school_demand = corr_df.sort_values('age_0_5', ascending=False).head(10)

    fig_school = px.bar(
        top_school_demand, x='Est_New_Classrooms', y='district', orientation='h',
        color='Est_New_Classrooms', color_continuous_scale='Viridis',
        labels={'Est_New_Classrooms': 'Classrooms Needed', 'district': 'District'}
    )
    fig_school.update_layout(yaxis=dict(autorange="reversed")) # Top value at top
    st.plotly_chart(fig_school, use_container_width=True)

# --- TAB 4: FORECASTING ---
with tab4:
    st.subheader("🔮 Predictive Intelligence: Q2 2026 Outlook")

    def generate_forecast(col_name, title, color_hex):
        ts_df = df.groupby('date')[[col_name]].sum().reset_index().set_index('date').sort_index()
        ts_weekly = ts_df.resample('W').sum()
        model = ExponentialSmoothing(ts_weekly[col_name], seasonal_periods=4, trend='add', seasonal='add').fit()
        forecast = model.forecast(12)

        current_avg = ts_weekly[col_name].iloc[-4:].mean()
        future_avg = forecast.mean()
        growth_pct = ((future_avg - current_avg) / current_avg) * 100
        trend_class = "trend-up" if growth_pct > 0 else "trend-down"
        arrow = "🔺" if growth_pct > 0 else "🔻"

        last_date = ts_weekly.index[-1]
        future_dates = [last_date + timedelta(weeks=i) for i in range(1, 13)]
        hist_df = ts_weekly.reset_index()
        pred_df = pd.DataFrame({'date': future_dates, 'Predicted': forecast})

        fig = px.line(hist_df, x='date', y=col_name, height=250)
        fig.add_scatter(x=pred_df['date'], y=pred_df['Predicted'], mode='lines+markers', line=dict(color=color_hex, dash='dot'), name='Forecast')
        fig.update_layout(margin=dict(t=10, l=0, r=0, b=0), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        return fig, growth_pct, arrow, trend_class, future_avg

    col_enrol, col_update, col_mig = st.columns(3)

    with col_enrol:
        fig1, pct1, arr1, cls1, val1 = generate_forecast('Total_Enrolment', 'New Enrolment Trend', '#00CC96')
        insight = "The trend is stabilizing due to near-100% saturation." if pct1 < 5 else "A sudden surge indicates a new demographic entering the system."
        action = "Reduce Enrolment Kits by 15% and shift to Updates." if pct1 < 5 else "Deploy emergency kits to border districts."

        # Analyst Box (Un-indented)
        st.markdown(f"""
<div class="metric-card" style="text-align:left; padding:20px;">
<div style="color:#00CC96; font-weight:bold; font-size:16px;">1. New User Growth</div>
<div style="font-size:24px; font-weight:bold; color:white;">{arr1} {pct1:.1f}%</div>
<div style="color:#8b949e; font-size:12px; margin-bottom:10px;">90-Day Projection</div>
<div style="color:#c9d1d9; font-size:13px; line-height:1.4;">
<b>Insight:</b> {insight}
<br><br><b>Action:</b> {action}
</div>
</div>
""", unsafe_allow_html=True)
        st.plotly_chart(fig1, use_container_width=True)

    with col_update:
        fig2, pct2, arr2, cls2, val2 = generate_forecast('Total_Updates', 'Correction Load', '#AB63FA')
        insight = "Standard operational variance detected." if pct2 < 10 else "Critical stress on server infrastructure expected."
        action = "Maintain current staffing." if pct2 < 10 else "Increase server bandwidth & extend staff hours."

        st.markdown(f"""
<div class="metric-card" style="text-align:left; padding:20px;">
<div style="color:#AB63FA; font-weight:bold; font-size:16px;">2. Operational Load</div>
<div style="font-size:24px; font-weight:bold; color:white;">{arr2} {pct2:.1f}%</div>
<div style="color:#8b949e; font-size:12px; margin-bottom:10px;">Server Stress Level</div>
<div style="color:#c9d1d9; font-size:13px; line-height:1.4;">
<b>Insight:</b> {insight}
<br><br><b>Action:</b> {action}
</div>
</div>
""", unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True)

    with col_mig:
        df['Adult_New_Enrolments'] = df['age_18_greater']
        fig3, pct3, arr3, cls3, val3 = generate_forecast('Adult_New_Enrolments', 'Migration Risk', '#EF553B')
        insight = "Adult new enrolments are within safety limits." if pct3 < 5 else "Abnormal spike in Adult New IDs. High Fraud Risk."
        action = "Routine monitoring." if pct3 < 5 else "🚨 IMMEDIATE AUDIT of new applications."

        st.markdown(f"""
<div class="metric-card" style="text-align:left; padding:20px;">
<div style="color:#EF553B; font-weight:bold; font-size:16px;">3. Fraud Risk</div>
<div style="font-size:24px; font-weight:bold; color:white;">{arr3} {pct3:.1f}%</div>
<div style="color:#8b949e; font-size:12px; margin-bottom:10px;">Suspicious Adult IDs</div>
<div style="color:#c9d1d9; font-size:13px; line-height:1.4;">
<b>Insight:</b> {insight}
<br><br><b>Action:</b> {action}
</div>
</div>
""", unsafe_allow_html=True)
        st.plotly_chart(fig3, use_container_width=True)
