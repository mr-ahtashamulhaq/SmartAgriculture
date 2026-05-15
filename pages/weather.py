import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from db import create_connection
from styles import inject_styles, render_sidebar, page_header, section_header, PLOTLY_LAYOUT, COLORS

st.set_page_config(page_title="Weather", page_icon="🌱", layout="wide")
inject_styles()
render_sidebar()

conn   = create_connection()
cursor = conn.cursor()

page_header("cloud", "Weather Records", "Track rainfall, temperature, and humidity across fields")

cursor.execute("SELECT field_id, field_name FROM Field")
field_map = {f"{f[0]} – {f[1]}": f[0] for f in cursor.fetchall()}

tab_view, tab_add, tab_update, tab_delete = st.tabs(
    ["Analytics & Records", "Add Record", "Update Record", "Delete Record"]
)

with tab_view:
    section_header("Weather Analytics")
    cursor.execute("""
        SELECT WeatherRecord.weather_id, Field.field_name,
               WeatherRecord.temperature, WeatherRecord.humidity,
               WeatherRecord.rainfall, WeatherRecord.record_date
        FROM WeatherRecord JOIN Field ON WeatherRecord.field_id = Field.field_id
        ORDER BY WeatherRecord.record_date
    """)
    df = pd.DataFrame(cursor.fetchall(),
        columns=["ID", "Field", "Temperature (°C)", "Humidity (%)", "Rainfall (mm)", "Date"])

    if not df.empty:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Records",    len(df))
        c2.metric("Avg Temperature",  f"{df['Temperature (°C)'].mean():.1f} °C")
        c3.metric("Avg Humidity",     f"{df['Humidity (%)'].mean():.1f} %")
        c4.metric("Avg Rainfall",     f"{df['Rainfall (mm)'].mean():.1f} mm")
        st.markdown("<br>", unsafe_allow_html=True)

        fig = go.Figure()
        fig.add_trace(go.Bar(x=df["Date"], y=df["Rainfall (mm)"], name="Rainfall (mm)",
                             marker=dict(color=COLORS["blue"], opacity=0.75, line=dict(width=0))))
        fig.add_trace(go.Scatter(x=df["Date"], y=df["Temperature (°C)"], name="Temperature (°C)",
                                 mode="lines+markers",
                                 line=dict(color=COLORS["amber"], width=2.5), marker=dict(size=5),
                                 yaxis="y2"))
        fig.add_trace(go.Scatter(x=df["Date"], y=df["Humidity (%)"], name="Humidity (%)",
                                 mode="lines", line=dict(color=COLORS["violet"], width=2, dash="dot"),
                                 yaxis="y2"))
        layout = PLOTLY_LAYOUT.copy()
        layout.update(height=340, bargap=0.3,
                      title=dict(text="Weather Trends", font=dict(color="#94a3b8", size=13)),
                      yaxis=dict(**PLOTLY_LAYOUT["yaxis"], title="Rainfall (mm)"),
                      yaxis2=dict(title="Temp / Humidity", overlaying="y", side="right",
                                  showgrid=False, tickfont=dict(color="#64748b")),
                      legend=dict(**PLOTLY_LAYOUT["legend"], orientation="h", y=1.08, x=0))
        fig.update_layout(**layout)
        st.plotly_chart(fig, use_container_width=True)

        field_rain = df.groupby("Field")["Rainfall (mm)"].mean().reset_index().sort_values("Rainfall (mm)", ascending=False)
        fig2 = go.Figure(go.Bar(
            y=field_rain["Field"], x=field_rain["Rainfall (mm)"], orientation="h",
            marker=dict(color=COLORS["cyan"], line=dict(width=0)),
            text=field_rain["Rainfall (mm)"].map(lambda v: f"{v:.1f}"),
            textposition="outside", textfont=dict(color="#94a3b8")
        ))
        layout2 = PLOTLY_LAYOUT.copy()
        layout2.update(height=max(200, 80 + len(field_rain)*40),
                       title=dict(text="Average Rainfall by Field", font=dict(color="#94a3b8", size=13)),
                       xaxis=dict(**PLOTLY_LAYOUT["xaxis"], title="mm"),
                       yaxis=dict(**PLOTLY_LAYOUT["yaxis"], title=""))
        fig2.update_layout(**layout2)
        st.plotly_chart(fig2, use_container_width=True)

        st.dataframe(df.sort_values("Date", ascending=False), use_container_width=True, hide_index=True)
    else:
        st.info("No weather records found.")

with tab_add:
    section_header("Add Weather Record")
    with st.form("add_weather_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            selected_field = st.selectbox("Select Field *", options=list(field_map.keys()))
            temperature    = st.number_input("Temperature (°C)", step=0.1, format="%.1f")
        with c2:
            humidity  = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, step=0.1, format="%.1f")
            rainfall  = st.number_input("Rainfall (mm)", min_value=0.0, step=0.1, format="%.1f")
        if st.form_submit_button("Add Weather Record", use_container_width=True):
            cursor.execute(
                "INSERT INTO WeatherRecord (field_id, temperature, humidity, rainfall) VALUES (%s,%s,%s,%s)",
                (field_map[selected_field], temperature, humidity, rainfall)
            )
            conn.commit()
            st.success("Weather record added successfully!")

with tab_update:
    section_header("Update Weather Record")
    cursor.execute("SELECT weather_id, record_date FROM WeatherRecord ORDER BY record_date DESC")
    records = cursor.fetchall()
    if records:
        record_map = {f"ID {r[0]} @ {r[1]}": r[0] for r in records}
        with st.form("update_weather_form"):
            selected_record = st.selectbox("Select Record to Update", options=list(record_map.keys()))
            c1, c2 = st.columns(2)
            with c1:
                new_field    = st.selectbox("New Field", options=list(field_map.keys()))
                new_temp     = st.number_input("New Temperature (°C)", step=0.1, format="%.1f")
            with c2:
                new_humidity = st.number_input("New Humidity (%)", min_value=0.0, max_value=100.0, step=0.1, format="%.1f")
                new_rainfall = st.number_input("New Rainfall (mm)", min_value=0.0, step=0.1, format="%.1f")
            if st.form_submit_button("Update Record", use_container_width=True):
                cursor.execute("""
                    UPDATE WeatherRecord SET field_id=%s, temperature=%s, humidity=%s, rainfall=%s WHERE weather_id=%s
                """, (field_map[new_field], new_temp, new_humidity, new_rainfall, record_map[selected_record]))
                conn.commit()
                st.success("Weather record updated successfully!")
    else:
        st.info("No records available to update.")

with tab_delete:
    section_header("Delete Weather Record")
    cursor.execute("SELECT weather_id, record_date FROM WeatherRecord ORDER BY record_date DESC")
    records = cursor.fetchall()
    if records:
        record_map = {f"ID {r[0]} @ {r[1]}": r[0] for r in records}
        with st.form("delete_weather_form"):
            selected_record = st.selectbox("Select Record to Delete", options=list(record_map.keys()))
            confirmed       = st.checkbox("I confirm I want to delete this record")
            if st.form_submit_button("Delete Record", use_container_width=True):
                if not confirmed:
                    st.warning("Please confirm deletion first.")
                else:
                    cursor.execute("DELETE FROM WeatherRecord WHERE weather_id=%s", (record_map[selected_record],))
                    conn.commit()
                    st.warning("Weather record deleted successfully.")
    else:
        st.info("No records available to delete.")

cursor.close()
conn.close()
