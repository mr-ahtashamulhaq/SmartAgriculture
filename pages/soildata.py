import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from db import create_connection
from styles import inject_styles, render_sidebar, page_header, section_header, PLOTLY_LAYOUT, COLORS

st.set_page_config(page_title="Soil Data", page_icon="🌱", layout="wide")
inject_styles()
render_sidebar()

conn   = create_connection()
cursor = conn.cursor()

page_header("science", "Soil Data", "Analyze soil health — moisture, temperature, and pH readings")

cursor.execute("SELECT sensor_id, sensor_type FROM Sensor")
sensor_map = {f"{s[0]} – {s[1]}": s[0] for s in cursor.fetchall()}

tab_view, tab_add, tab_update, tab_delete = st.tabs(
    ["Analytics & Records", "Add Reading", "Update Reading", "Delete Reading"]
)

with tab_view:
    section_header("Soil Analytics")
    cursor.execute("""
        SELECT SoilData.soil_data_id, Sensor.sensor_type,
               SoilData.moisture_level, SoilData.temperature,
               SoilData.ph_level, SoilData.recorded_time
        FROM SoilData JOIN Sensor ON SoilData.sensor_id = Sensor.sensor_id
        ORDER BY SoilData.recorded_time
    """)
    df = pd.DataFrame(cursor.fetchall(),
        columns=["ID", "Sensor Type", "Moisture", "Temperature", "pH", "Recorded Time"])

    if not df.empty:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Readings", len(df))
        c2.metric("Avg Moisture",   f"{df['Moisture'].mean():.1f} %")
        c3.metric("Avg Temperature",f"{df['Temperature'].mean():.1f} °C")
        c4.metric("Avg pH",         f"{df['pH'].mean():.2f}")
        st.markdown("<br>", unsafe_allow_html=True)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["Recorded Time"], y=df["Moisture"],
            name="Moisture (%)", mode="lines+markers",
            line=dict(color=COLORS["blue"], width=2), marker=dict(size=4),
            fill="tozeroy", fillcolor="rgba(59,130,246,0.06)"
        ))
        fig.add_trace(go.Scatter(
            x=df["Recorded Time"], y=df["Temperature"],
            name="Temperature (°C)", mode="lines+markers",
            line=dict(color=COLORS["amber"], width=2), marker=dict(size=4), yaxis="y2"
        ))
        fig.add_trace(go.Scatter(
            x=df["Recorded Time"], y=df["pH"],
            name="pH Level", mode="lines+markers",
            line=dict(color=COLORS["violet"], width=2, dash="dot"), marker=dict(size=4), yaxis="y3"
        ))
        layout = PLOTLY_LAYOUT.copy()
        layout.update(height=340,
                      title=dict(text="Soil Readings Over Time", font=dict(color="#94a3b8", size=13)),
                      yaxis=dict(**PLOTLY_LAYOUT["yaxis"], title="Moisture %"),
                      yaxis2=dict(title="Temp °C", overlaying="y", side="right",
                                  showgrid=False, tickfont=dict(color="#64748b")),
                      yaxis3=dict(title="pH", overlaying="y", side="right", position=0.97,
                                  showgrid=False, tickfont=dict(color="#64748b")),
                      legend=dict(**PLOTLY_LAYOUT["legend"], orientation="h", y=1.08, x=0))
        fig.update_layout(**layout)
        st.plotly_chart(fig, use_container_width=True)

        col_a, col_b = st.columns(2)
        with col_a:
            fig_box = go.Figure()
            for col, color in [("Moisture", COLORS["blue"]), ("Temperature", COLORS["amber"]), ("pH", COLORS["violet"])]:
                fig_box.add_trace(go.Box(y=df[col], name=col, marker_color=color, line_color=color))
            fig_box.update_layout(**PLOTLY_LAYOUT, height=250,
                                  title=dict(text="Value Distribution", font=dict(color="#94a3b8", size=13)),
                                  showlegend=False)
            st.plotly_chart(fig_box, use_container_width=True)
        with col_b:
            st.markdown('<p style="font-size:0.8rem;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">All Readings</p>', unsafe_allow_html=True)
            st.dataframe(df.sort_values("Recorded Time", ascending=False),
                         use_container_width=True, hide_index=True, height=220)
    else:
        st.info("No soil data available.")

with tab_add:
    section_header("Add Soil Reading")
    with st.form("add_soil_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            selected_sensor = st.selectbox("Select Sensor *", options=list(sensor_map.keys()))
            moisture_level  = st.number_input("Moisture Level (%)", min_value=0.0, step=0.1, format="%.2f")
        with c2:
            temperature = st.number_input("Temperature (°C)", step=0.1, format="%.2f")
            ph_level    = st.number_input("pH Level", min_value=0.0, max_value=14.0, step=0.1, format="%.2f")
        if st.form_submit_button("Add Reading", use_container_width=True):
            cursor.execute(
                "INSERT INTO SoilData (sensor_id, moisture_level, temperature, ph_level) VALUES (%s,%s,%s,%s)",
                (sensor_map[selected_sensor], moisture_level, temperature, ph_level)
            )
            conn.commit()
            st.success("Soil reading added successfully!")

with tab_update:
    section_header("Update Soil Reading")
    cursor.execute("SELECT soil_data_id, recorded_time FROM SoilData ORDER BY recorded_time DESC")
    records = cursor.fetchall()
    if records:
        record_map = {f"ID {r[0]} @ {r[1]}": r[0] for r in records}
        with st.form("update_soil_form"):
            selected_record = st.selectbox("Select Record to Update", options=list(record_map.keys()))
            c1, c2 = st.columns(2)
            with c1:
                new_sensor   = st.selectbox("New Sensor", options=list(sensor_map.keys()))
                new_moisture = st.number_input("New Moisture (%)", min_value=0.0, step=0.1, format="%.2f")
            with c2:
                new_temp = st.number_input("New Temperature (°C)", step=0.1, format="%.2f")
                new_ph   = st.number_input("New pH Level", min_value=0.0, max_value=14.0, step=0.1, format="%.2f")
            if st.form_submit_button("Update Reading", use_container_width=True):
                cursor.execute("""
                    UPDATE SoilData SET sensor_id=%s, moisture_level=%s, temperature=%s, ph_level=%s WHERE soil_data_id=%s
                """, (sensor_map[new_sensor], new_moisture, new_temp, new_ph, record_map[selected_record]))
                conn.commit()
                st.success("Soil reading updated successfully!")
    else:
        st.info("No records available to update.")

with tab_delete:
    section_header("Delete Soil Reading")
    cursor.execute("SELECT soil_data_id, recorded_time FROM SoilData ORDER BY recorded_time DESC")
    records = cursor.fetchall()
    if records:
        record_map = {f"ID {r[0]} @ {r[1]}": r[0] for r in records}
        with st.form("delete_soil_form"):
            selected_record = st.selectbox("Select Record to Delete", options=list(record_map.keys()))
            confirmed       = st.checkbox("I confirm I want to delete this record")
            if st.form_submit_button("Delete Record", use_container_width=True):
                if not confirmed:
                    st.warning("Please confirm deletion first.")
                else:
                    cursor.execute("DELETE FROM SoilData WHERE soil_data_id=%s", (record_map[selected_record],))
                    conn.commit()
                    st.warning("Soil data record deleted successfully.")
    else:
        st.info("No records available to delete.")

cursor.close()
conn.close()
