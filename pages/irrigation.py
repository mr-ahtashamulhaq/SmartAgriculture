import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from db import create_connection
from styles import inject_styles, render_sidebar, page_header, section_header, PLOTLY_LAYOUT, COLORS

st.set_page_config(page_title="Irrigation", page_icon="🌱", layout="wide")
inject_styles()
render_sidebar()

conn   = create_connection()
cursor = conn.cursor()

page_header("water_drop", "Irrigation Schedules", "Plan and monitor water delivery across all field zones")

cursor.execute("SELECT field_id, field_name FROM Field")
field_map = {f"{f[0]} – {f[1]}": f[0] for f in cursor.fetchall()}

tab_view, tab_add, tab_update, tab_delete = st.tabs(
    ["Analytics & Schedules", "Add Schedule", "Update Schedule", "Delete Schedule"]
)

with tab_view:
    section_header("Irrigation Analytics")
    cursor.execute("""
        SELECT IrrigationSchedule.schedule_id, Field.field_name,
               IrrigationSchedule.start_time, IrrigationSchedule.duration_minutes,
               IrrigationSchedule.water_amount
        FROM IrrigationSchedule JOIN Field ON IrrigationSchedule.field_id = Field.field_id
        ORDER BY IrrigationSchedule.start_time
    """)
    df = pd.DataFrame(cursor.fetchall(),
        columns=["ID", "Field", "Start Time", "Duration (min)", "Water (L)"])

    if not df.empty:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Schedules", len(df))
        c2.metric("Total Water (L)",  f"{df['Water (L)'].sum():.0f}")
        c3.metric("Total Duration",   f"{df['Duration (min)'].sum()} min")
        c4.metric("Fields Covered",   df["Field"].nunique())
        st.markdown("<br>", unsafe_allow_html=True)

        field_water = df.groupby("Field")["Water (L)"].sum().reset_index().sort_values("Water (L)", ascending=False)
        fig = go.Figure(go.Bar(
            y=field_water["Field"], x=field_water["Water (L)"], orientation="h",
            marker=dict(color=field_water["Water (L)"],
                        colorscale=[[0,"#1e40af"],[0.5,"#3b82f6"],[1,"#06b6d4"]],
                        showscale=False, line=dict(width=0)),
            text=field_water["Water (L)"].map(lambda v: f"{v:.0f} L"),
            textposition="outside", textfont=dict(color="#94a3b8")
        ))
        layout = PLOTLY_LAYOUT.copy()
        layout.update(height=max(220, 80+len(field_water)*40),
                      title=dict(text="Total Water Used by Field", font=dict(color="#94a3b8", size=13)),
                      xaxis=dict(**PLOTLY_LAYOUT["xaxis"], title="Litres"),
                      yaxis=dict(**PLOTLY_LAYOUT["yaxis"], title=""))
        fig.update_layout(**layout)
        st.plotly_chart(fig, use_container_width=True)

        col_chart, col_tbl = st.columns(2)
        with col_chart:
            fig2 = go.Figure(go.Scatter(
                x=df["Duration (min)"], y=df["Water (L)"], mode="markers",
                marker=dict(size=10, color=df["Water (L)"],
                            colorscale=[[0,"#16a34a"],[1,"#06b6d4"]],
                            showscale=True, colorbar=dict(title="Water (L)", tickfont=dict(color="#64748b"))),
                text=df["Field"],
                hovertemplate="<b>%{text}</b><br>Duration: %{x} min<br>Water: %{y} L<extra></extra>"
            ))
            layout2 = PLOTLY_LAYOUT.copy()
            layout2.update(height=260,
                           title=dict(text="Duration vs Water Used", font=dict(color="#94a3b8", size=13)),
                           xaxis=dict(**PLOTLY_LAYOUT["xaxis"], title="Duration (min)"),
                           yaxis=dict(**PLOTLY_LAYOUT["yaxis"], title="Water (L)"))
            fig2.update_layout(**layout2)
            st.plotly_chart(fig2, use_container_width=True)
        with col_tbl:
            st.markdown('<p style="font-size:0.8rem;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">All Schedules</p>', unsafe_allow_html=True)
            st.dataframe(df.sort_values("Start Time", ascending=False),
                         use_container_width=True, hide_index=True, height=240)
    else:
        st.info("No irrigation schedules found.")

with tab_add:
    section_header("Add Irrigation Schedule")
    with st.form("add_irrigation_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            selected_field   = st.selectbox("Select Field *", options=list(field_map.keys()))
            schedule_date    = st.date_input("Schedule Date")
        with c2:
            schedule_time    = st.time_input("Schedule Time")
            duration_minutes = st.number_input("Duration (Minutes)", min_value=1, step=1)
        water_amount = st.number_input("Water Amount (Litres)", min_value=0.0, step=0.5, format="%.1f")
        if st.form_submit_button("Add Schedule", use_container_width=True):
            cursor.execute(
                "INSERT INTO IrrigationSchedule (field_id, start_time, duration_minutes, water_amount) VALUES (%s,%s,%s,%s)",
                (field_map[selected_field], datetime.combine(schedule_date, schedule_time), duration_minutes, water_amount)
            )
            conn.commit()
            st.success("Irrigation schedule added successfully!")

with tab_update:
    section_header("Update Schedule")
    cursor.execute("SELECT schedule_id, start_time FROM IrrigationSchedule ORDER BY start_time DESC")
    schedules = cursor.fetchall()
    if schedules:
        sched_map = {f"ID {s[0]} @ {s[1]}": s[0] for s in schedules}
        with st.form("update_irrigation_form"):
            selected_sched = st.selectbox("Select Schedule to Update", options=list(sched_map.keys()))
            c1, c2 = st.columns(2)
            with c1:
                new_field    = st.selectbox("New Field", options=list(field_map.keys()))
                new_date     = st.date_input("New Date")
            with c2:
                new_time     = st.time_input("New Time")
                new_duration = st.number_input("New Duration (min)", min_value=1, step=1)
            new_water = st.number_input("New Water Amount (L)", min_value=0.0, step=0.5, format="%.1f")
            if st.form_submit_button("Update Schedule", use_container_width=True):
                cursor.execute("""
                    UPDATE IrrigationSchedule SET field_id=%s, start_time=%s,
                        duration_minutes=%s, water_amount=%s WHERE schedule_id=%s
                """, (field_map[new_field], datetime.combine(new_date, new_time),
                      new_duration, new_water, sched_map[selected_sched]))
                conn.commit()
                st.success("Schedule updated successfully!")
    else:
        st.info("No schedules available to update.")

with tab_delete:
    section_header("Delete Schedule")
    cursor.execute("SELECT schedule_id, start_time FROM IrrigationSchedule ORDER BY start_time DESC")
    schedules = cursor.fetchall()
    if schedules:
        sched_map = {f"ID {s[0]} @ {s[1]}": s[0] for s in schedules}
        with st.form("delete_irrigation_form"):
            selected_sched = st.selectbox("Select Schedule to Delete", options=list(sched_map.keys()))
            confirmed      = st.checkbox("I confirm I want to delete this schedule")
            if st.form_submit_button("Delete Schedule", use_container_width=True):
                if not confirmed:
                    st.warning("Please confirm deletion first.")
                else:
                    cursor.execute("DELETE FROM IrrigationSchedule WHERE schedule_id=%s", (sched_map[selected_sched],))
                    conn.commit()
                    st.warning("Schedule deleted successfully.")
    else:
        st.info("No schedules available to delete.")

cursor.close()
conn.close()
