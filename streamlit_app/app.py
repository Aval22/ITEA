"""
ITEA Framework v1.45 — Interactive Dashboard
Triple Exposure to Automation Index
923 occupations · 8 indicators · O*NET 2024 v29.1

Author: Alberto García-Lluis Valencia
Affiliation: Universidad Rey Juan Carlos
DOI: 10.5281/zenodo.19578916
GitHub: https://github.com/Aval22/ITEA
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ==================== CONFIG ====================
st.set_page_config(
    page_title="ITEA Framework v1.45",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CONSTANTS ====================
INDICATORS = {
    'ITEA Global': {'label': 'ITEA', 'color': '#C0392B', 'desc': 'Triple Automation Exposure'},
    'IRO_v3': {'label': 'IRO', 'color': '#2471A3', 'desc': 'Occupational Resilience'},
    'ICT': {'label': 'ICT', 'color': '#148F77', 'desc': 'Technical Complexity'},
    'IFS_v3': {'label': 'IFS', 'color': '#B7950B', 'desc': 'Social Friction'},
    'IPI': {'label': 'IPI', 'color': '#CA6F1E', 'desc': 'Interpersonal Presence'},
    'IEF': {'label': 'IEF', 'color': '#1B4F72', 'desc': 'Functional Specificity'},
    'GEE_v3': {'label': 'GEE', 'color': '#6C3483', 'desc': 'Education-Experience Gradient'},
    'IMO_v3': {'label': 'IMO', 'color': '#1A5276', 'desc': 'Occupational Mutation'},
}
IND_KEYS = list(INDICATORS.keys())
IND_LABELS = [v['label'] for v in INDICATORS.values()]
IND_COLORS = [v['color'] for v in INDICATORS.values()]

JZ_LABELS = {
    1: "JZ1 — Little/No Preparation",
    2: "JZ2 — Some Preparation",
    3: "JZ3 — Medium Preparation",
    4: "JZ4 — Considerable Preparation",
    5: "JZ5 — Extensive Preparation"
}

SOC_SECTORS = {
    11: "Management", 13: "Business & Financial", 15: "Computer & Mathematical",
    17: "Architecture & Engineering", 19: "Life, Physical, Social Science",
    21: "Community & Social Service", 23: "Legal", 25: "Educational Instruction",
    27: "Arts, Design, Entertainment", 29: "Healthcare Practitioners",
    31: "Healthcare Support", 33: "Protective Service", 35: "Food Preparation",
    37: "Building & Grounds", 39: "Personal Care & Service", 41: "Sales",
    43: "Office & Administrative", 45: "Farming, Fishing, Forestry",
    47: "Construction & Extraction", 49: "Installation, Maintenance, Repair",
    51: "Production", 53: "Transportation & Material Moving"
}


# ==================== LOAD DATA ====================
@st.cache_data
def load_data():
    df = pd.read_csv("streamlit_app/itea_data.csv")
    df['Sector'] = df['SOC Major'].map(SOC_SECTORS).fillna('Other')
    df['JZ_Label'] = df['Job Zone'].map(JZ_LABELS).fillna('Unknown')
    df['Risk'] = pd.cut(df['ITEA Global'],
                        bins=[0, 0.25, 0.40, 0.50, 1.0],
                        labels=['Very Low', 'Low', 'Moderate', 'High'])
    # Filter rows with valid ITEA
    df = df[df['ITEA Global'].notna() & (df['ITEA Global'] > 0)]
    return df

df = load_data()


# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    .stApp { background-color: #EDEEF0; }
    .block-container { padding-top: 1.5rem; }
    div[data-testid="stMetric"] {
        background: white;
        border-radius: 10px;
        padding: 12px 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    div[data-testid="stMetric"] label { color: #7F8C8D !important; font-size: 12px !important; }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: #1B4F72 !important; }
    .stSelectbox > div > div { background: white; }
    section[data-testid="stSidebar"] { background: #F4F6F7; }
    h1 { color: #1B4F72 !important; }
    h2, h3 { color: #2C3E50 !important; }
</style>
""", unsafe_allow_html=True)


# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## 📊 ITEA Framework")
    st.markdown("**v1.45** · O*NET 2024 v29.1")
    st.markdown("---")

    # Filters
    st.markdown("### Filters")

    search = st.text_input("🔍 Search occupation", placeholder="e.g. Physician, 29-1214")

    jz_filter = st.multiselect(
        "Job Zone",
        options=[1, 2, 3, 4, 5],
        format_func=lambda x: f"JZ {x}",
        default=[]
    )

    sector_filter = st.multiselect(
        "Sector",
        options=sorted(df['Sector'].unique()),
        default=[]
    )

    risk_filter = st.multiselect(
        "Risk Level",
        options=['Very Low', 'Low', 'Moderate', 'High'],
        default=[]
    )

    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    **Author**: Alberto García-Lluis Valencia  
    **Affiliation**: Universidad Rey Juan Carlos  
    **DOI**: [10.5281/zenodo.19578916](https://doi.org/10.5281/zenodo.19578916)  
    **GitHub**: [Aval22/ITEA](https://github.com/Aval22/ITEA)
    """)


# ==================== FILTER DATA ====================
dff = df.copy()
if search:
    mask = (dff['Ocupación'].str.lower().str.contains(search.lower(), na=False) |
            dff['SOC Code'].str.contains(search, na=False))
    dff = dff[mask]
if jz_filter:
    dff = dff[dff['Job Zone'].isin(jz_filter)]
if sector_filter:
    dff = dff[dff['Sector'].isin(sector_filter)]
if risk_filter:
    dff = dff[dff['Risk'].isin(risk_filter)]


# ==================== HEADER ====================
st.title("ITEA Framework v1.45")
st.markdown("*Triple Exposure to Automation Index — 8 indicators across 1,016 occupations*")

# KPI row
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Occupations", f"{len(dff):,}")
with col2:
    st.metric("Avg ITEA", f"{dff['ITEA Global'].mean():.3f}")
with col3:
    st.metric("Avg IRO", f"{dff['IRO_v3'].mean():.3f}" if dff['IRO_v3'].notna().sum() > 0 else "N/A")
with col4:
    st.metric("High Risk", f"{(dff['Risk'] == 'High').sum()}")
with col5:
    st.metric("Job Zones", f"{dff['Job Zone'].nunique()}")


# ==================== TABS ====================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Occupation Table",
    "📊 Scatter Explorer",
    "🎯 Occupation Profile",
    "📈 Sector Analysis",
    "🔄 Compare Occupations"
])


# --- TAB 1: TABLE ---
with tab1:
    sort_by = st.selectbox("Sort by", IND_KEYS,
                           format_func=lambda x: INDICATORS[x]['label'],
                           index=0)

    display_cols = ['SOC Code', 'Ocupación', 'Job Zone', 'Sector', 'Risk'] + IND_KEYS
    display_df = dff[display_cols].sort_values(sort_by, ascending=False).head(100)

    # Rename columns for display
    rename_map = {k: v['label'] for k, v in INDICATORS.items()}
    display_df = display_df.rename(columns=rename_map)

    st.dataframe(
        display_df,
        use_container_width=True,
        height=500,
        column_config={
            "ITEA": st.column_config.ProgressColumn(min_value=0, max_value=0.6, format="%.3f"),
            "IRO": st.column_config.ProgressColumn(min_value=0, max_value=0.6, format="%.3f"),
            "ICT": st.column_config.ProgressColumn(min_value=0, max_value=1.0, format="%.3f"),
            "IFS": st.column_config.ProgressColumn(min_value=0, max_value=1.0, format="%.3f"),
            "IPI": st.column_config.ProgressColumn(min_value=0, max_value=1.0, format="%.3f"),
            "IEF": st.column_config.ProgressColumn(min_value=0, max_value=0.7, format="%.3f"),
            "GEE": st.column_config.ProgressColumn(min_value=0, max_value=1.0, format="%.3f"),
            "IMO": st.column_config.ProgressColumn(min_value=0, max_value=1.0, format="%.3f"),
        }
    )
    st.caption(f"Showing top {min(100, len(display_df))} of {len(dff)} filtered occupations")


# --- TAB 2: SCATTER ---
with tab2:
    col_x, col_y, col_size = st.columns(3)
    with col_x:
        x_axis = st.selectbox("X Axis", IND_KEYS, index=0,
                               format_func=lambda x: INDICATORS[x]['label'], key="scatter_x")
    with col_y:
        y_axis = st.selectbox("Y Axis", IND_KEYS, index=1,
                               format_func=lambda x: INDICATORS[x]['label'], key="scatter_y")
    with col_size:
        size_col = st.selectbox("Bubble size", ['AEI'] + IND_KEYS,
                                format_func=lambda x: x if x == 'AEI' else INDICATORS[x]['label'],
                                key="scatter_size")

    scatter_df = dff.dropna(subset=[x_axis, y_axis])
    if size_col == 'AEI':
        scatter_df = scatter_df[scatter_df['AEI'].notna() & (scatter_df['AEI'] > 0)]

    risk_colors = {'Very Low': '#2471A3', 'Low': '#148F77', 'Moderate': '#CA6F1E', 'High': '#C0392B'}

    fig_scatter = px.scatter(
        scatter_df,
        x=x_axis, y=y_axis,
        size=size_col if scatter_df[size_col].notna().sum() > 0 else None,
        color='Risk',
        color_discrete_map=risk_colors,
        hover_name='Ocupación',
        hover_data={'SOC Code': True, 'Job Zone': True, 'Sector': True,
                    x_axis: ':.3f', y_axis: ':.3f'},
        labels={x_axis: INDICATORS[x_axis]['label'], y_axis: INDICATORS[y_axis]['label']},
        height=550
    )
    fig_scatter.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='#EDEEF0',
        font=dict(family="DM Sans, sans-serif"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig_scatter.update_xaxes(gridcolor='#EAECEE', zerolinecolor='#D5D8DC')
    fig_scatter.update_yaxes(gridcolor='#EAECEE', zerolinecolor='#D5D8DC')
    st.plotly_chart(fig_scatter, use_container_width=True)


# --- TAB 3: PROFILE ---
with tab3:
    occ_options = dff['Ocupación'].tolist()
    if occ_options:
        selected_occ = st.selectbox("Select occupation", occ_options, key="profile_occ")
        occ_data = dff[dff['Ocupación'] == selected_occ].iloc[0]

        # Header
        risk = occ_data['Risk']
        risk_color = {'Very Low': '#2471A3', 'Low': '#148F77', 'Moderate': '#CA6F1E', 'High': '#C0392B'}.get(risk, '#7F8C8D')

        st.markdown(f"### {occ_data['Ocupación']}")
        st.markdown(f"**{occ_data['SOC Code']}** · {JZ_LABELS.get(occ_data['Job Zone'], '')} · "
                    f"Sector: {occ_data['Sector']} · "
                    f"Risk: **:{risk_color}[{risk}]**")

        # KPI cards
        cols = st.columns(8)
        for i, (key, info) in enumerate(INDICATORS.items()):
            val = occ_data[key]
            with cols[i]:
                st.metric(info['label'], f"{val:.3f}" if pd.notna(val) and val > 0 else "—")

        # Charts side by side
        col_radar, col_bar = st.columns(2)

        with col_radar:
            values = [occ_data[k] if pd.notna(occ_data[k]) else 0 for k in IND_KEYS]
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=values + [values[0]],
                theta=IND_LABELS + [IND_LABELS[0]],
                fill='toself',
                fillcolor='rgba(27,79,114,0.12)',
                line=dict(color='#1B4F72', width=2.5),
                name=occ_data['Ocupación'][:30]
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 1], gridcolor='#D5D8DC'),
                    bgcolor='white'
                ),
                showlegend=False,
                height=350,
                margin=dict(l=50, r=50, t=30, b=30),
                paper_bgcolor='#EDEEF0'
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        with col_bar:
            bar_df = pd.DataFrame({
                'Indicator': IND_LABELS,
                'Value': values,
                'Color': IND_COLORS
            })
            fig_bar = px.bar(bar_df, x='Value', y='Indicator', orientation='h',
                             color='Indicator', color_discrete_sequence=IND_COLORS,
                             height=350)
            fig_bar.update_layout(
                xaxis=dict(range=[0, 1], gridcolor='#EAECEE'),
                yaxis=dict(autorange='reversed'),
                showlegend=False,
                plot_bgcolor='white',
                paper_bgcolor='#EDEEF0',
                margin=dict(l=10, r=20, t=30, b=30)
            )
            st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No occupations match your filters. Try broadening your search.")


# --- TAB 4: SECTORS ---
with tab4:
    indicator_sector = st.selectbox("Indicator", IND_KEYS,
                                    format_func=lambda x: INDICATORS[x]['label'],
                                    key="sector_ind")

    sector_means = dff.groupby('Sector')[indicator_sector].agg(['mean', 'count']).reset_index()
    sector_means.columns = ['Sector', 'Mean', 'Count']
    sector_means = sector_means[sector_means['Count'] >= 3].sort_values('Mean', ascending=True)

    fig_sector = px.bar(sector_means, x='Mean', y='Sector', orientation='h',
                        color='Mean',
                        color_continuous_scale=['#148F77', '#B7950B', '#C0392B'],
                        height=max(400, len(sector_means) * 28),
                        hover_data={'Count': True, 'Mean': ':.3f'})
    fig_sector.update_layout(
        xaxis_title=INDICATORS[indicator_sector]['label'],
        yaxis_title='',
        coloraxis_showscale=False,
        plot_bgcolor='white',
        paper_bgcolor='#EDEEF0',
        margin=dict(l=10, r=20, t=30, b=30)
    )
    st.plotly_chart(fig_sector, use_container_width=True)

    # Distribution by Job Zone
    st.markdown(f"#### {INDICATORS[indicator_sector]['label']} Distribution by Job Zone")
    fig_box = px.box(dff.dropna(subset=[indicator_sector]),
                     x='Job Zone', y=indicator_sector,
                     color='Job Zone',
                     color_discrete_sequence=['#2471A3', '#148F77', '#B7950B', '#CA6F1E', '#C0392B'],
                     height=350,
                     labels={indicator_sector: INDICATORS[indicator_sector]['label']})
    fig_box.update_layout(
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='#EDEEF0'
    )
    st.plotly_chart(fig_box, use_container_width=True)


# --- TAB 5: COMPARE ---
with tab5:
    st.markdown("Select up to 4 occupations to compare their indicator profiles.")

    compare_occs = st.multiselect(
        "Occupations to compare",
        options=dff['Ocupación'].tolist(),
        max_selections=4,
        default=dff['Ocupación'].tolist()[:2] if len(dff) >= 2 else []
    )

    if len(compare_occs) >= 2:
        comp_colors = ['#C0392B', '#2471A3', '#148F77', '#6C3483']

        fig_comp = go.Figure()
        for i, occ_name in enumerate(compare_occs):
            occ = dff[dff['Ocupación'] == occ_name].iloc[0]
            vals = [occ[k] if pd.notna(occ[k]) else 0 for k in IND_KEYS]
            fig_comp.add_trace(go.Scatterpolar(
                r=vals + [vals[0]],
                theta=IND_LABELS + [IND_LABELS[0]],
                fill='toself',
                fillcolor=f'rgba({int(comp_colors[i][1:3],16)},{int(comp_colors[i][3:5],16)},{int(comp_colors[i][5:7],16)},0.08)',
                line=dict(color=comp_colors[i], width=2.5),
                name=occ_name[:35]
            ))

        fig_comp.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 1], gridcolor='#D5D8DC'),
                bgcolor='white'
            ),
            height=450,
            margin=dict(l=60, r=60, t=40, b=40),
            paper_bgcolor='#EDEEF0',
            legend=dict(orientation="h", yanchor="bottom", y=-0.15)
        )
        st.plotly_chart(fig_comp, use_container_width=True)

        # Comparison table
        comp_data = []
        for occ_name in compare_occs:
            occ = dff[dff['Ocupación'] == occ_name].iloc[0]
            row = {'Occupation': occ_name[:40], 'JZ': occ['Job Zone']}
            for k, v in INDICATORS.items():
                row[v['label']] = f"{occ[k]:.3f}" if pd.notna(occ[k]) and occ[k] > 0 else "—"
            comp_data.append(row)

        st.dataframe(pd.DataFrame(comp_data), use_container_width=True, hide_index=True)
    else:
        st.info("Select at least 2 occupations to compare.")


# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#95A5A6; font-size:11px; padding:10px;">
    <strong>ITEA Framework v1.45</strong> · García-Lluis Valencia, A. (2026) · Universidad Rey Juan Carlos<br>
    DOI: <a href="https://doi.org/10.5281/zenodo.19578916" style="color:#2471A3">10.5281/zenodo.19578916</a> · 
    GitHub: <a href="https://github.com/Aval22/ITEA" style="color:#2471A3">Aval22/ITEA</a> · 
    Data: O*NET 2024 v29.1, U.S. Department of Labor
</div>
""", unsafe_allow_html=True)
