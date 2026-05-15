import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from db import create_connection
from styles import inject_styles, render_sidebar, page_header, section_header, PLOTLY_LAYOUT, COLORS

st.set_page_config(
    page_title="Smart Agriculture Monitoring System",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_styles()
render_sidebar()

conn   = create_connection()
cursor = conn.cursor()

# ── HEADER ────────────────────────────────────────────────────────────────────
page_header("dashboard", "Dashboard", "Real-time monitoring & analytics for your smart farm")

# ── KPI METRICS ───────────────────────────────────────────────────────────────
cursor.execute("SELECT COUNT(*) FROM Farmer");       total_farmers   = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM Farm");         total_farms     = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM Field");        total_fields    = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM Sensor");       total_sensors   = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM Crop");         total_crops     = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM IrrigationSchedule"); total_schedules = cursor.fetchone()[0]

section_header("System Overview")
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Farmers",    total_farmers)
c2.metric("Farms",      total_farms)
c3.metric("Fields",     total_fields)
c4.metric("Sensors",    total_sensors)
c5.metric("Crops",      total_crops)
c6.metric("Schedules",  total_schedules)

# ── ENVIRONMENTAL AVERAGES ────────────────────────────────────────────────────
cursor.execute("SELECT AVG(temperature), AVG(moisture_level), AVG(ph_level) FROM SoilData")
row = cursor.fetchone()
avg_soil_temp, avg_moisture, avg_ph = row

cursor.execute("SELECT AVG(rainfall), AVG(humidity), AVG(temperature) FROM WeatherRecord")
row2 = cursor.fetchone()
avg_rainfall, avg_humidity, avg_weather_temp = row2

section_header("Environmental Analytics")
e1, e2, e3, e4, e5 = st.columns(5)
e1.metric("Soil Temperature",  f"{avg_soil_temp:.1f} °C"  if avg_soil_temp  else "—")
e2.metric("Avg Moisture",      f"{avg_moisture:.1f} %"    if avg_moisture   else "—")
e3.metric("Soil pH",           f"{avg_ph:.2f}"            if avg_ph         else "—")
e4.metric("Avg Rainfall",      f"{avg_rainfall:.1f} mm"   if avg_rainfall   else "—")
e5.metric("Avg Humidity",      f"{avg_humidity:.1f} %"    if avg_humidity   else "—")

# ── CHARTS ────────────────────────────────────────────────────────────────────
section_header("Analytics & Trends")

cursor.execute("SELECT recorded_time, moisture_level, temperature, ph_level FROM SoilData ORDER BY recorded_time")
soil_chart = pd.DataFrame(cursor.fetchall(), columns=["Time", "Moisture", "Temperature", "pH"])

cursor.execute("SELECT record_date, rainfall, humidity, temperature FROM WeatherRecord ORDER BY record_date")
weather_chart = pd.DataFrame(cursor.fetchall(), columns=["Date", "Rainfall", "Humidity", "Temperature"])

cursor.execute("SELECT sensor_type, COUNT(*) FROM Sensor GROUP BY sensor_type")
sensor_df = pd.DataFrame(cursor.fetchall(), columns=["Type", "Count"])

cursor.execute("SELECT soil_type, COUNT(*) FROM Field GROUP BY soil_type")
soil_type_df = pd.DataFrame(cursor.fetchall(), columns=["Soil Type", "Count"])

row1_col1, row1_col2 = st.columns(2)

# Chart 1 – Soil Moisture & Temperature
with row1_col1:
    st.markdown('<p style="font-weight:700;font-size:0.92rem;color:#374151;margin-bottom:4px;">Soil Moisture &amp; Temperature Over Time</p>', unsafe_allow_html=True)
    if not soil_chart.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=soil_chart["Time"], y=soil_chart["Moisture"],
            name="Moisture (%)", mode="lines+markers",
            line=dict(color=COLORS["blue"], width=2.5), marker=dict(size=5),
            fill="tozeroy", fillcolor="rgba(59,130,246,0.08)"
        ))
        fig.add_trace(go.Scatter(
            x=soil_chart["Time"], y=soil_chart["Temperature"],
            name="Temperature (°C)", mode="lines+markers",
            line=dict(color=COLORS["amber"], width=2.5), marker=dict(size=5), yaxis="y2"
        ))
        layout = PLOTLY_LAYOUT.copy()
        layout.update(height=320,
                      yaxis=dict(**PLOTLY_LAYOUT["yaxis"], title="Moisture %"),
                      yaxis2=dict(title="Temperature °C", overlaying="y", side="right",
                                  showgrid=False, tickfont=dict(color="#64748b"),
                                  linecolor="rgba(255,255,255,0.08)"),
                      legend=dict(**PLOTLY_LAYOUT["legend"], orientation="h",
                                  yanchor="bottom", y=1.02, xanchor="right", x=1))
        fig.update_layout(**layout)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No soil data available yet.")

# Chart 2 – Rainfall Analysis
with row1_col2:
    st.markdown('<p style="font-weight:700;font-size:0.92rem;color:#374151;margin-bottom:4px;">Rainfall Analysis</p>', unsafe_allow_html=True)
    if not weather_chart.empty:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=weather_chart["Date"], y=weather_chart["Rainfall"], name="Rainfall (mm)",
            marker=dict(color=weather_chart["Rainfall"],
                        colorscale=[[0,"#1e40af"],[0.5,"#3b82f6"],[1,"#06b6d4"]],
                        showscale=False, line=dict(width=0))
        ))
        fig2.add_trace(go.Scatter(
            x=weather_chart["Date"], y=weather_chart["Humidity"],
            name="Humidity (%)", mode="lines",
            line=dict(color=COLORS["violet"], width=2, dash="dot"), yaxis="y2"
        ))
        layout2 = PLOTLY_LAYOUT.copy()
        layout2.update(height=320, bargap=0.25,
                       yaxis=dict(**PLOTLY_LAYOUT["yaxis"], title="Rainfall mm"),
                       yaxis2=dict(title="Humidity %", overlaying="y", side="right",
                                   showgrid=False, tickfont=dict(color="#64748b"),
                                   linecolor="rgba(255,255,255,0.08)"),
                       legend=dict(**PLOTLY_LAYOUT["legend"], orientation="h",
                                   yanchor="bottom", y=1.02, xanchor="right", x=1))
        fig2.update_layout(**layout2)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No weather data available yet.")

# Row 2
row2_col1, row2_col2, row2_col3 = st.columns([1.2, 1, 1])

with row2_col1:
    st.markdown('<p style="font-weight:700;font-size:0.92rem;color:#374151;margin-bottom:4px;">Sensor Type Distribution</p>', unsafe_allow_html=True)
    if not sensor_df.empty:
        fig3 = go.Figure(go.Pie(
            labels=sensor_df["Type"], values=sensor_df["Count"], hole=0.55,
            marker=dict(colors=[COLORS["green"], COLORS["blue"], COLORS["amber"],
                                 COLORS["rose"], COLORS["violet"]]),
            textinfo="label+percent", textfont=dict(color="#374151", size=12),
            hovertemplate="<b>%{label}</b><br>Count: %{value}<extra></extra>"
        ))
        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", color="#475569"),
            margin=dict(l=20, r=20, t=30, b=20), height=280, showlegend=True,
            legend=dict(font=dict(color="#374151"), bgcolor="rgba(255,255,255,0.8)"),
            annotations=[dict(text=f"<b>{sensor_df['Count'].sum()}</b><br>Total",
                               x=0.5, y=0.5, showarrow=False,
                               font=dict(size=16, color="#0f172a"))]
        )
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("No sensor data.")

with row2_col2:
    st.markdown('<p style="font-weight:700;font-size:0.92rem;color:#374151;margin-bottom:4px;">Fields by Soil Type</p>', unsafe_allow_html=True)
    if not soil_type_df.empty:
        fig4 = go.Figure(go.Bar(
            x=soil_type_df["Count"], y=soil_type_df["Soil Type"], orientation="h",
            marker=dict(color=[COLORS["green"], COLORS["blue"], COLORS["amber"],
                               COLORS["rose"], COLORS["violet"], COLORS["cyan"]][:len(soil_type_df)],
                        line=dict(width=0)),
            text=soil_type_df["Count"], textposition="outside",
            textfont=dict(color="#94a3b8")
        ))
        layout4 = PLOTLY_LAYOUT.copy()
        layout4.update(height=280, xaxis=dict(**PLOTLY_LAYOUT["xaxis"], title=""),
                       yaxis=dict(**PLOTLY_LAYOUT["yaxis"], title=""))
        fig4.update_layout(**layout4)
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("No field data.")

with row2_col3:
    st.markdown('<p style="font-weight:700;font-size:0.92rem;color:#374151;margin-bottom:4px;">Average Soil pH</p>', unsafe_allow_html=True)
    ph_val = float(avg_ph) if avg_ph else 7.0
    fig5 = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=ph_val,
        delta={"reference": 7.0, "valueformat": ".2f",
               "increasing": {"color": COLORS["amber"]},
               "decreasing": {"color": COLORS["blue"]}},
        number={"font": {"color": "#0f172a", "size": 34, "family": "Inter"}},
        gauge=dict(
            axis=dict(range=[0, 14], tickwidth=1, tickcolor="#475569",
                      tickfont=dict(color="#64748b")),
            bar=dict(color=COLORS["green"], thickness=0.25),
            bgcolor="rgba(0,0,0,0)", borderwidth=0,
            steps=[
                dict(range=[0,  6], color="rgba(239,68,68,0.12)"),
                dict(range=[6,  8], color="rgba(34,197,94,0.12)"),
                dict(range=[8, 14], color="rgba(59,130,246,0.12)"),
            ],
            threshold=dict(line=dict(color="white", width=2), thickness=0.75, value=7)
        ),
        title=dict(text="pH Scale  |  Ideal: 6–8", font=dict(color="#64748b", size=11))
    ))
    fig5.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#94a3b8"),
        margin=dict(l=20, r=20, t=30, b=10), height=280,
    )
    st.plotly_chart(fig5, use_container_width=True)

# ── RECENT RECORDS ────────────────────────────────────────────────────────────
section_header("Recent Monitoring Records")
t1, t2 = st.columns(2)

cursor.execute("""
    SELECT SoilData.soil_data_id, Sensor.sensor_type,
           SoilData.moisture_level, SoilData.temperature,
           SoilData.ph_level, SoilData.recorded_time
    FROM SoilData JOIN Sensor ON SoilData.sensor_id = Sensor.sensor_id
    ORDER BY SoilData.recorded_time DESC LIMIT 8
""")
soil_df = pd.DataFrame(cursor.fetchall(),
    columns=["ID", "Sensor", "Moisture", "Temperature", "pH", "Recorded"])

cursor.execute("""
    SELECT WeatherRecord.weather_id, Field.field_name,
           WeatherRecord.temperature, WeatherRecord.humidity,
           WeatherRecord.rainfall, WeatherRecord.record_date
    FROM WeatherRecord JOIN Field ON WeatherRecord.field_id = Field.field_id
    ORDER BY WeatherRecord.record_date DESC LIMIT 8
""")
weather_df = pd.DataFrame(cursor.fetchall(),
    columns=["ID", "Field", "Temp (°C)", "Humidity (%)", "Rainfall (mm)", "Date"])

with t1:
    st.markdown('<p style="font-size:0.8rem;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Latest Soil Records</p>', unsafe_allow_html=True)
    if not soil_df.empty:
        st.dataframe(soil_df, use_container_width=True, hide_index=True)
    else:
        st.info("No soil data available.")

with t2:
    st.markdown('<p style="font-size:0.8rem;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Latest Weather Records</p>', unsafe_allow_html=True)
    if not weather_df.empty:
        st.dataframe(weather_df, use_container_width=True, hide_index=True)
    else:
        st.info("No weather data available.")

st.markdown("""
<div style="text-align:center; color:#1e293b; font-size:0.75rem;
            padding: 2rem 0 0.5rem; border-top:1px solid rgba(255,255,255,0.05); margin-top:2rem;">
    Smart Agriculture Monitoring System
</div>
""", unsafe_allow_html=True)

cursor.close()
conn.close()