import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from db import create_connection
from styles import inject_styles, render_sidebar, page_header, section_header, PLOTLY_LAYOUT, COLORS

st.set_page_config(page_title="Sensors", page_icon="🌱", layout="wide")
inject_styles()
render_sidebar()

conn   = create_connection()
cursor = conn.cursor()

page_header("sensors", "Sensors", "Monitor IoT sensor installations, types and operational status")

cursor.execute("SELECT field_id, field_name FROM Field")
field_map = {f"{f[0]} – {f[1]}": f[0] for f in cursor.fetchall()}

SENSOR_TYPES  = ["Moisture", "Temperature", "pH"]
SENSOR_STATUS = ["Active", "Inactive", "Maintenance"]

tab_view, tab_add, tab_update, tab_delete = st.tabs(
    ["View Records", "Add Sensor", "Update Sensor", "Delete Sensor"]
)

with tab_view:
    section_header("Sensor Records")
    cursor.execute("""
        SELECT Sensor.sensor_id, Field.field_name, Sensor.sensor_type,
               Sensor.installation_date, Sensor.current_status
        FROM Sensor JOIN Field ON Sensor.field_id = Field.field_id
    """)
    df = pd.DataFrame(cursor.fetchall(), columns=["ID", "Field", "Type", "Installed", "Status"])
    if not df.empty:
        status_counts = df["Status"].value_counts()
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Sensors",  len(df))
        c2.metric("Active",         status_counts.get("Active", 0))
        c3.metric("Maintenance",    status_counts.get("Maintenance", 0))
        c4.metric("Inactive",       status_counts.get("Inactive", 0))
        st.markdown("<br>", unsafe_allow_html=True)

        col_chart, col_table = st.columns([1, 2])
        with col_chart:
            status_df = status_counts.reset_index()
            status_df.columns = ["Status", "Count"]
            color_map = {"Active": COLORS["green"], "Maintenance": COLORS["amber"], "Inactive": COLORS["rose"]}
            fig = go.Figure(go.Pie(
                labels=status_df["Status"], values=status_df["Count"], hole=0.55,
                marker=dict(colors=[color_map.get(s, COLORS["blue"]) for s in status_df["Status"]]),
                textinfo="label+percent", textfont=dict(color="#cbd5e1", size=12),
            ))
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter, sans-serif", color="#94a3b8"),
                margin=dict(l=10, r=10, t=20, b=10), height=220, showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)
        with col_table:
            st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No sensor records found.")

with tab_add:
    section_header("Add New Sensor")
    with st.form("add_sensor_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            selected_field    = st.selectbox("Select Field *", options=list(field_map.keys()))
            sensor_type       = st.selectbox("Sensor Type *", options=SENSOR_TYPES)
        with c2:
            installation_date = st.date_input("Installation Date")
            current_status    = st.selectbox("Status", options=SENSOR_STATUS)
        if st.form_submit_button("Add Sensor", use_container_width=True):
            cursor.execute(
                "INSERT INTO Sensor (field_id, sensor_type, installation_date, current_status) VALUES (%s,%s,%s,%s)",
                (field_map[selected_field], sensor_type, installation_date, current_status)
            )
            conn.commit()
            st.success(f"**{sensor_type}** sensor added successfully!")

with tab_update:
    section_header("Update Sensor")
    cursor.execute("SELECT sensor_id, sensor_type FROM Sensor")
    sensors = cursor.fetchall()
    if sensors:
        sensor_map = {f"{s[0]} – {s[1]}": s[0] for s in sensors}
        with st.form("update_sensor_form"):
            selected_sensor   = st.selectbox("Select Sensor to Update", options=list(sensor_map.keys()))
            c1, c2 = st.columns(2)
            with c1:
                new_field         = st.selectbox("New Field", options=list(field_map.keys()))
                new_sensor_type   = st.selectbox("New Type", options=SENSOR_TYPES)
            with c2:
                new_install_date  = st.date_input("New Installation Date")
                new_status        = st.selectbox("New Status", options=SENSOR_STATUS)
            if st.form_submit_button("Update Sensor", use_container_width=True):
                cursor.execute("""
                    UPDATE Sensor SET field_id=%s, sensor_type=%s, installation_date=%s, current_status=%s WHERE sensor_id=%s
                """, (field_map[new_field], new_sensor_type, new_install_date, new_status, sensor_map[selected_sensor]))
                conn.commit()
                st.success("Sensor updated successfully!")
    else:
        st.info("No sensors available to update.")

with tab_delete:
    section_header("Delete Sensor")
    cursor.execute("SELECT sensor_id, sensor_type FROM Sensor")
    sensors = cursor.fetchall()
    if sensors:
        sensor_map = {f"{s[0]} – {s[1]}": s[0] for s in sensors}
        with st.form("delete_sensor_form"):
            selected_sensor = st.selectbox("Select Sensor to Delete", options=list(sensor_map.keys()))
            confirmed       = st.checkbox("I confirm I want to delete this sensor")
            if st.form_submit_button("Delete Sensor", use_container_width=True):
                if not confirmed:
                    st.warning("Please confirm deletion first.")
                else:
                    cursor.execute("DELETE FROM Sensor WHERE sensor_id=%s", (sensor_map[selected_sensor],))
                    conn.commit()
                    st.warning("Sensor deleted successfully.")
    else:
        st.info("No sensors available to delete.")

cursor.close()
conn.close()
