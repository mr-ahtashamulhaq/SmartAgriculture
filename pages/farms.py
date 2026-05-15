import streamlit as st
import pandas as pd
from db import create_connection
from styles import inject_styles, render_sidebar, page_header, section_header

st.set_page_config(page_title="Farms", page_icon="🌱", layout="wide")
inject_styles()
render_sidebar()

conn   = create_connection()
cursor = conn.cursor()

page_header("home", "Farms", "Manage farm properties and their associated farmers")

cursor.execute("SELECT farmer_id, farmer_name FROM Farmer")
farmer_map = {f"{f[0]} – {f[1]}": f[0] for f in cursor.fetchall()}

tab_view, tab_add, tab_update, tab_delete = st.tabs(
    ["View Records", "Add Farm", "Update Farm", "Delete Farm"]
)

with tab_view:
    section_header("Farm Records")
    cursor.execute("""
        SELECT Farm.farm_id, Farmer.farmer_name, Farm.farm_name,
               Farm.farm_location, Farm.total_area
        FROM Farm JOIN Farmer ON Farm.farmer_id = Farmer.farmer_id
    """)
    df = pd.DataFrame(cursor.fetchall(), columns=["ID", "Farmer", "Farm Name", "Location", "Area (ha)"])
    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption(f"Total: **{len(df)}** farms")
    else:
        st.info("No farm records found.")

with tab_add:
    section_header("Add New Farm")
    with st.form("add_farm_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            selected_farmer = st.selectbox("Select Farmer *", options=list(farmer_map.keys()))
            farm_name       = st.text_input("Farm Name *", placeholder="e.g. Green Acres")
        with c2:
            farm_location   = st.text_input("Location", placeholder="City, District")
            total_area      = st.number_input("Total Area (ha)", min_value=0.0, step=0.5, format="%.2f")
        if st.form_submit_button("Add Farm", use_container_width=True):
            if not farm_name:
                st.error("Farm name is required.")
            else:
                cursor.execute(
                    "INSERT INTO Farm (farmer_id, farm_name, farm_location, total_area) VALUES (%s, %s, %s, %s)",
                    (farmer_map[selected_farmer], farm_name, farm_location, total_area)
                )
                conn.commit()
                st.success(f"Farm **{farm_name}** added successfully!")

with tab_update:
    section_header("Update Farm")
    cursor.execute("SELECT farm_id, farm_name FROM Farm")
    farms = cursor.fetchall()
    if farms:
        farm_map = {f"{f[0]} – {f[1]}": f[0] for f in farms}
        with st.form("update_farm_form"):
            selected_farm = st.selectbox("Select Farm to Update", options=list(farm_map.keys()))
            c1, c2 = st.columns(2)
            with c1:
                new_farmer   = st.selectbox("New Farmer", options=list(farmer_map.keys()))
                new_name     = st.text_input("New Farm Name")
            with c2:
                new_location = st.text_input("New Location")
                new_area     = st.number_input("New Total Area (ha)", min_value=0.0, step=0.5, format="%.2f")
            if st.form_submit_button("Update Farm", use_container_width=True):
                cursor.execute("""
                    UPDATE Farm SET farmer_id=%s, farm_name=%s, farm_location=%s, total_area=%s WHERE farm_id=%s
                """, (farmer_map[new_farmer], new_name, new_location, new_area, farm_map[selected_farm]))
                conn.commit()
                st.success("Farm updated successfully!")
    else:
        st.info("No farms available to update.")

with tab_delete:
    section_header("Delete Farm")
    cursor.execute("SELECT farm_id, farm_name FROM Farm")
    farms = cursor.fetchall()
    if farms:
        farm_map = {f"{f[0]} – {f[1]}": f[0] for f in farms}
        with st.form("delete_farm_form"):
            selected_farm = st.selectbox("Select Farm to Delete", options=list(farm_map.keys()))
            confirmed     = st.checkbox("I confirm I want to delete this farm")
            if st.form_submit_button("Delete Farm", use_container_width=True):
                if not confirmed:
                    st.warning("Please confirm deletion first.")
                else:
                    cursor.execute("DELETE FROM Farm WHERE farm_id=%s", (farm_map[selected_farm],))
                    conn.commit()
                    st.warning("Farm deleted successfully.")
    else:
        st.info("No farms available to delete.")

cursor.close()
conn.close()