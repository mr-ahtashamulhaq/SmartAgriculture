import streamlit as st
import pandas as pd
import plotly.express as px
from db import create_connection
from styles import inject_styles, render_sidebar, page_header, section_header, PLOTLY_LAYOUT, COLORS

st.set_page_config(page_title="Crops", page_icon="🌱", layout="wide")
inject_styles()
render_sidebar()

conn   = create_connection()
cursor = conn.cursor()

page_header("agriculture", "Crops", "Track planting cycles, harvest dates and field assignments")

cursor.execute("SELECT field_id, field_name FROM Field")
field_map = {f"{f[0]} – {f[1]}": f[0] for f in cursor.fetchall()}

tab_view, tab_add, tab_update, tab_delete = st.tabs(
    ["View Records", "Add Crop", "Update Crop", "Delete Crop"]
)

with tab_view:
    section_header("Crop Records")
    cursor.execute("""
        SELECT Crop.crop_id, Field.field_name, Crop.crop_name,
               Crop.planting_date, Crop.expected_harvest_date
        FROM Crop JOIN Field ON Crop.field_id = Field.field_id
    """)
    df = pd.DataFrame(cursor.fetchall(), columns=["ID", "Field", "Crop Name", "Planted", "Harvest Expected"])
    if not df.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Crops",     len(df))
        c2.metric("Unique Fields",   df["Field"].nunique())
        c3.metric("Crop Varieties",  df["Crop Name"].nunique())
        st.markdown("<br>", unsafe_allow_html=True)

        crop_counts = df["Crop Name"].value_counts().reset_index()
        crop_counts.columns = ["Crop", "Count"]
        fig = px.bar(crop_counts, x="Crop", y="Count", color="Count",
                     color_continuous_scale=[[0,"#16a34a"],[0.5,"#22c55e"],[1,"#86efac"]],
                     title="Crop Variety Distribution")
        fig.update_layout(**PLOTLY_LAYOUT, height=260,
                          coloraxis_showscale=False,
                          title_font=dict(color="#94a3b8", size=13))
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No crop records found.")

with tab_add:
    section_header("Add New Crop")
    with st.form("add_crop_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            selected_field = st.selectbox("Select Field *", options=list(field_map.keys()))
            crop_name      = st.text_input("Crop Name *", placeholder="e.g. Wheat, Rice, Cotton")
        with c2:
            planting_date  = st.date_input("Planting Date")
            harvest_date   = st.date_input("Expected Harvest Date")
        if st.form_submit_button("Add Crop", use_container_width=True):
            if not crop_name:
                st.error("Crop name is required.")
            else:
                cursor.execute(
                    "INSERT INTO Crop (field_id, crop_name, planting_date, expected_harvest_date) VALUES (%s,%s,%s,%s)",
                    (field_map[selected_field], crop_name, planting_date, harvest_date)
                )
                conn.commit()
                st.success(f"Crop **{crop_name}** added successfully!")

with tab_update:
    section_header("Update Crop")
    cursor.execute("SELECT crop_id, crop_name FROM Crop")
    crops = cursor.fetchall()
    if crops:
        crop_map = {f"{c[0]} – {c[1]}": c[0] for c in crops}
        with st.form("update_crop_form"):
            selected_crop  = st.selectbox("Select Crop to Update", options=list(crop_map.keys()))
            c1, c2 = st.columns(2)
            with c1:
                new_field      = st.selectbox("New Field", options=list(field_map.keys()))
                new_crop_name  = st.text_input("New Crop Name")
            with c2:
                new_plant_date = st.date_input("New Planting Date")
                new_harv_date  = st.date_input("New Harvest Date")
            if st.form_submit_button("Update Crop", use_container_width=True):
                cursor.execute("""
                    UPDATE Crop SET field_id=%s, crop_name=%s, planting_date=%s, expected_harvest_date=%s WHERE crop_id=%s
                """, (field_map[new_field], new_crop_name, new_plant_date, new_harv_date, crop_map[selected_crop]))
                conn.commit()
                st.success("Crop updated successfully!")
    else:
        st.info("No crops available to update.")

with tab_delete:
    section_header("Delete Crop")
    cursor.execute("SELECT crop_id, crop_name FROM Crop")
    crops = cursor.fetchall()
    if crops:
        crop_map = {f"{c[0]} – {c[1]}": c[0] for c in crops}
        with st.form("delete_crop_form"):
            selected_crop = st.selectbox("Select Crop to Delete", options=list(crop_map.keys()))
            confirmed     = st.checkbox("I confirm I want to delete this crop")
            if st.form_submit_button("Delete Crop", use_container_width=True):
                if not confirmed:
                    st.warning("Please confirm deletion first.")
                else:
                    cursor.execute("DELETE FROM Crop WHERE crop_id=%s", (crop_map[selected_crop],))
                    conn.commit()
                    st.warning("Crop deleted successfully.")
    else:
        st.info("No crops available to delete.")

cursor.close()
conn.close()
