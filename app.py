# -*- coding: utf-8 -*-
"""
🌱 TA Terra Angel — Регенеративный дашборд (Streamlit)
Cash Flow + Гео-карта + KPI-карточки
Стиль: космический индиго • тёплое золото • минимализм
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime

# =============================================================================
# 🎨 КОНФИГУРАЦИЯ СТРАНИЦЫ И СТИЛЕЙ
# =============================================================================
st.set_page_config(
    page_title="TA Terra Angel Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Цветовая палитра
COLORS = {
    'indigo': '#2E86AB',
    'gold': '#F4A261',
    'azure': '#64B5F6',
    'bg_light': '#F8F9FC',
    'success': '#2A9D8F',
    'warning': '#E76F51',
    'text': '#1A1A2E'
}

# =============================================================================
# 💎 КАСТОМНЫЙ CSS (для красивых KPI-карточек)
# =============================================================================
st.markdown("""
<style>
    /* Основной фон */
    .stApp {
        background: linear-gradient(135deg, #F8F9FC 0%, #E8EEF7 100%);
    }
    
    /* Заголовок */
    .main-header {
        background: linear-gradient(135deg, #2E86AB 0%, #1A5276 100%);
        color: white;
        padding: 20px 30px;
        border-radius: 0 0 20px 20px;
        margin-bottom: 30px;
        box-shadow: 0 4px 20px rgba(46,134,171,0.25);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 24px;
        font-weight: 600;
    }
    
    .main-header p {
        margin: 5px 0 0 0;
        font-size: 12px;
        opacity: 0.9;
    }
    
    /* KPI карточки */
    .kpi-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(46,134,171,0.08);
        border: 1px solid rgba(46,134,171,0.1);
        text-align: center;
        transition: transform 0.2s;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(46,134,171,0.15);
    }
    
    .kpi-icon {
        font-size: 28px;
        margin-bottom: 8px;
    }
    
    .kpi-label {
        font-size: 12px;
        color: #666;
        margin-bottom: 8px;
        font-weight: 500;
    }
    
    .kpi-value {
        font-size: 28px;
        font-weight: 700;
        font-family: 'Courier New', monospace;
    }
    
    .kpi-unit {
        font-size: 11px;
        color: #888;
        margin-left: 4px;
    }
    
    .kpi-trend {
        font-size: 12px;
        margin-top: 8px;
    }
    
    /* Графики */
    .chart-container {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    /* Футер */
    .footer {
        text-align: center;
        padding: 20px;
        margin-top: 40px;
        border-top: 1px solid rgba(0,0,0,0.05);
        font-size: 11px;
        color: #888;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# 💰 ДАННЫЕ: Cash Flow
# =============================================================================
@st.cache_data
def generate_cashflow_data():
    years = list(range(1, 9))
    investments = [-800_000, -600_000, -400_000, -100_000, 0, 0, 0, 0]
    revenue = [0, 0, 50_000, 300_000, 900_000, 3_500_000, 3_800_000, 4_200_000]
    payouts = [0, 0, 0, 0, 0, -3_200_000, -3_200_000, -3_200_000]
    
    ocf = [inv + rev + pay for inv, rev, pay in zip(investments, revenue, payouts)]
    cumulative = [sum(ocf[:i+1]) for i in range(len(ocf))]
    
    return pd.DataFrame({
        'year': years,
        'investments': investments,
        'revenue': revenue,
        'payouts': payouts,
        'ocf': ocf,
        'cumulative': cumulative
    })

# =============================================================================
# 🌍 ДАННЫЕ: Гео-проекты
# =============================================================================
@st.cache_data
def generate_geo_data():
    return pd.DataFrame({
        'location': ['Casablanca', 'Marrakech', 'Agadir', 'Nairobi', 'Cape Town', 'Accra'],
        'lat': [33.5731, 31.6295, 30.4278, -1.2921, -33.9249, 5.6037],
        'lon': [-7.5898, -7.9811, -9.5981, 36.8219, 18.4241, -0.1870],
        'project': ['Worm Farm HQ', 'Solar Hub', 'Earthship Pilot', 'Bio-Refinery', 'Carbon Hub', 'WORM WORLD'],
        'co2_tons': [2500, 1200, 450, 3800, 2100, 1800],
        'status': ['Active', 'Planning', 'Pilot', 'Active', 'Active', 'Q2-2026'],
        'type': ['Био', 'Энергия', 'Жильё', 'Переработка', 'Финансы', 'Био']
    })

# =============================================================================
# 📊 ДАННЫЕ: KPI
# =============================================================================
@st.cache_data
def generate_kpi_data():
    return {
        'co2_absorbed_total': 11850,
        'tokens_issued': 11850,
        'operating_profit_share': '12.5%',
        'projects_active': 4,
        'projects_pipeline': 2,
        'avg_payback_months': 58,
        'community_members': 340,
        'local_jobs_created': 87
    }

# =============================================================================
# 🎨 ГРАФИКИ
# =============================================================================

def create_cashflow_chart(df):
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['year'], y=df['ocf'], name='OCF (операционный поток)',
        marker_color=[COLORS['success'] if v >= 0 else COLORS['warning'] for v in df['ocf']],
        hovertemplate='<b>Год %{x}</b><br>OCF: %{y:,.0f} USD<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=df['year'], y=df['cumulative'], name='Накопленный поток',
        line=dict(color=COLORS['indigo'], width=3, shape='spline'),
        mode='lines+markers',
        hovertemplate='Накоплено: %{y:,.0f} USD<extra></extra>'
    ))
    
    fig.add_vline(x=5.5, line_dash="dash", line_color=COLORS['gold'], line_width=2,
                  annotation_text="▶ Старт выплат: 6-й год", 
                  annotation_position="top right",
                  annotation_font=dict(size=10, color=COLORS['gold']))
    
    fig.add_hline(y=0, line_dash="dot", line_color="rgba(0,0,0,0.1)")
    
    fig.update_layout(
        title="💰 Cash Flow модели (8 лет)",
        xaxis_title="Год проекта", yaxis_title="USD",
        template='plotly_white',
        hovermode="x unified",
        yaxis_tickformat=',.0f',
        height=400,
        margin=dict(t=40, b=30, l=30, r=20),
        colorway=[COLORS['indigo'], COLORS['gold'], COLORS['success'], COLORS['warning']],
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig


def create_geo_map(df):
    status_colors = {
        'Active': COLORS['success'],
        'Planning': COLORS['azure'],
        'Pilot': COLORS['gold'],
        'Q2-2026': COLORS['warning']
    }
    
    fig = px.scatter_mapbox(
        df, lat="lat", lon="lon",
        size="co2_tons", 
        color="status",
        color_discrete_map=status_colors,
        hover_name="location",
        hover_data={
            "project": True,
            "co2_tons": ":,.0f тонн CO₂",
            "status": True,
            "type": True,
            "lat": False, "lon": False
        },
        zoom=2.5, height=400,
        mapbox_style="carto-positron"
    )
    
    # FIX: Remove invalid 'line' property for scattermapbox markers
    fig.update_traces(
        marker=dict(size=8, opacity=0.85),
        selector=dict(mode='markers')
    )
    
    fig.update_layout(
        title="🌍 География проектов",
        margin=dict(t=40, b=0, l=0, r=0),
        template='plotly_white',
        coloraxis_showscale=False,
        legend_title_text="Статус"
    )
    return fig

# =============================================================================
# 🏗️ UI: KPI КАРТОЧКИ (HTML)
# =============================================================================
def render_kpi_card(icon, label, value, unit, color, trend=None):
    trend_html = f'<div class="kpi-trend" style="color: {COLORS["success"]}">{trend}</div>' if trend else ''
    
    return f"""
    <div class="kpi-card">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value" style="color: {color}">
            {value}<span class="kpi-unit">{unit}</span>
        </div>
        {trend_html}
    </div>
    """

# =============================================================================
# 🚀 ОСНОВНОЙ ИНТЕРФЕЙС
# =============================================================================

# Заголовок
st.markdown(f"""
<div class="main-header">
    <h1>🌱 TA Terra Angel — Регенеративный дашборд</h1>
    <p>Обновлено: {datetime.now().strftime('%d.%m.%Y %H:%M')} • 1 токен = 1 тонна CO₂ + 12.5% операционной прибыли</p>
</div>
""", unsafe_allow_html=True)

# Получаем данные
kpi_data = generate_kpi_data()
cashflow_df = generate_cashflow_data()
geo_df = generate_geo_data()

# KPI Карточки (4 основные)
st.markdown("### 📊 Ключевые показатели")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(render_kpi_card(
        "🌱", "CO₂ абсорбировано", f"{kpi_data['co2_absorbed_total']:,}", "тонн",
        COLORS['success']
    ), unsafe_allow_html=True)

with col2:
    st.markdown(render_kpi_card(
        "🪙", "Токенов выпущено", f"{kpi_data['tokens_issued']:,}", "TA",
        COLORS['indigo']
    ), unsafe_allow_html=True)

with col3:
    st.markdown(render_kpi_card(
        "📈", "Доля прибыли", kpi_data['operating_profit_share'], "операционной",
        COLORS['gold']
    ), unsafe_allow_html=True)

with col4:
    st.markdown(render_kpi_card(
        "🗺️", "Активные проекты", str(kpi_data['projects_active']), 
        f"+{kpi_data['projects_pipeline']} в плане",
        COLORS['azure']
    ), unsafe_allow_html=True)

# Дополнительные KPI (второй ряд)
col5, col6, col7 = st.columns(3)

with col5:
    st.markdown(render_kpi_card(
        "⏱️", "Срок окупаемости", str(kpi_data['avg_payback_months']), "мес.",
        COLORS['text'], "▼ Оптимизация"
    ), unsafe_allow_html=True)

with col6:
    st.markdown(render_kpi_card(
        "👥", "Участников сообщества", f"{kpi_data['community_members']:,}", "чел.",
        COLORS['text'], "▲ Рост"
    ), unsafe_allow_html=True)

with col7:
    st.markdown(render_kpi_card(
        "💼", "Рабочих мест создано", f"{kpi_data['local_jobs_created']:,}", "локальных",
        COLORS['text'], "▲ Вакансии"
    ), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Графики: 2 колонки
col_chart, col_map = st.columns([6, 4])

with col_chart:
    st.markdown("### 💰 Динамика денежных потоков")
    fig_cashflow = create_cashflow_chart(cashflow_df)
    st.plotly_chart(fig_cashflow, use_container_width=True)

with col_map:
    st.markdown("### 🌍 Проекты в Африке")
    fig_map = create_geo_map(geo_df)
    st.plotly_chart(fig_map, use_container_width=True)

# Футер
st.markdown("""
<div class="footer">
    <strong>TA Terra Angel</strong> • Регенеративная экономика • Марокко & Африка<br>
    <em>Технологии на основе червей • Углеродные кредиты • Сообщество акционеров</em>
</div>
""", unsafe_allow_html=True)

# Сайдбар с информацией
with st.sidebar:
    st.header("ℹ️ О проекте")
    st.markdown("""
    **TA Terra Angel** — это регенеративная экономическая модель, 
    которая объединяет:
    
    - 🌱 Экологическую устойчивость (CO₂ абсорбция)
    - 💰 Финансовую отдачу (доля операционной прибыли)
    - 👥 Социальное воздействие (рабочие места)
    
    ---
    
    **Токенизация:**  
    1 TA токен = 1 тонна абсорбированного CO₂ + 12.5% доли операционной прибыли
    
    ---
    
    **Технологии:**
    - Vermicomposting (черви)
    - Biochar production
    - Solar energy
    - Earthship housing
    """)
    
    st.markdown("---")
    st.caption(f"Версия дашборда: 1.0\n\nПостроен на Streamlit + Plotly")
