import streamlit as st
import pandas as pd
from db import create_connection
from styles import inject_styles, render_sidebar, page_header, section_header

st.set_page_config(page_title="Fields", page_icon="🌱", layout="wide")
inject_styles()
render_sidebar()

conn   = create_connection()
cursor = conn.cursor()

page_header("grass", "Fields", "Manage field plots, soil types, and areas within each farm")

cursor.execute("SELECT farm_id, farm_name FROM Farm")
farm_map = {f"{f[0]} – {f[1]}": f[0] for f in cursor.fetchall()}

tab_view, tab_add, tab_update, tab_delete = st.tabs(
    ["View Records", "Add Field", "Update Field", "Delete Field"]
)

with tab_view:
    section_header("Field Records")
    cursor.execute("""
        SELECT Field.field_id, Farm.farm_name, Field.field_name, Field.soil_type, Field.field_area
        FROM Field JOIN Farm ON Field.farm_id = Farm.farm_id
    """)
    df = pd.DataFrame(cursor.fetchall(), columns=["ID", "Farm", "Field Name", "Soil Type", "Area (ha)"])
    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption(f"Total: **{len(df)}** fields")
    else:
        st.info("No field records found.")

with tab_add:
    section_header("Add New Field")
    with st.form("add_field_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            selected_farm = st.selectbox("Select Farm *", options=list(farm_map.keys()))
            field_name    = st.text_input("Field Name *", placeholder="e.g. North Plot A")
        with c2:
            soil_type  = st.text_input("Soil Type", placeholder="e.g. Loamy, Clay, Sandy")
            field_area = st.number_input("Field Area (ha)", min_value=0.0, step=0.5, format="%.2f")
        if st.form_submit_button("Add Field", use_container_width=True):
            if not field_name:
                st.error("Field name is required.")
            else:
                cursor.execute(
                    "INSERT INTO Field (farm_id, field_name, soil_type, field_area) VALUES (%s, %s, %s, %s)",
                    (farm_map[selected_farm], field_name, soil_type, field_area)
                )
                conn.commit()
                st.success(f"Field **{field_name}** added successfully!")

with tab_update:
    section_header("Update Field")
    cursor.execute("SELECT field_id, field_name FROM Field")
    fields = cursor.fetchall()
    if fields:
        field_map = {f"{f[0]} – {f[1]}": f[0] for f in fields}
        with st.form("update_field_form"):
            selected_field = st.selectbox("Select Field to Update", options=list(field_map.keys()))
            c1, c2 = st.columns(2)
            with c1:
                new_farm       = st.selectbox("New Farm", options=list(farm_map.keys()))
                new_field_name = st.text_input("New Field Name")
            with c2:
                new_soil_type  = st.text_input("New Soil Type")
                new_area       = st.number_input("New Area (ha)", min_value=0.0, step=0.5, format="%.2f")
            if st.form_submit_button("Update Field", use_container_width=True):
                cursor.execute("""
                    UPDATE Field SET farm_id=%s, field_name=%s, soil_type=%s, field_area=%s WHERE field_id=%s
                """, (farm_map[new_farm], new_field_name, new_soil_type, new_area, field_map[selected_field]))
                conn.commit()
                st.success("Field updated successfully!")
    else:
        st.info("No fields available to update.")

with tab_delete:
    section_header("Delete Field")
    cursor.execute("SELECT field_id, field_name FROM Field")
    fields = cursor.fetchall()
    if fields:
        field_map = {f"{f[0]} – {f[1]}": f[0] for f in fields}
        with st.form("delete_field_form"):
            selected_field = st.selectbox("Select Field to Delete", options=list(field_map.keys()))
            confirmed      = st.checkbox("I confirm I want to delete this field")
            if st.form_submit_button("Delete Field", use_container_width=True):
                if not confirmed:
                    st.warning("Please confirm deletion first.")
                else:
                    cursor.execute("DELETE FROM Field WHERE field_id=%s", (field_map[selected_field],))
                    conn.commit()
                    st.warning("Field deleted successfully.")
    else:
        st.info("No fields available to delete.")

cursor.close()
conn.close()
