import streamlit as st
import pandas as pd
from db import create_connection
from styles import inject_styles, render_sidebar, page_header, section_header

st.set_page_config(page_title="Farmers", page_icon="🌱", layout="wide")
inject_styles()
render_sidebar()

conn   = create_connection()
cursor = conn.cursor()

page_header("person", "Farmers", "Manage farmer profiles and contact information")

tab_view, tab_add, tab_update, tab_delete = st.tabs(
    ["View Records", "Add Farmer", "Update Farmer", "Delete Farmer"]
)

with tab_view:
    section_header("Farmer Records")
    cursor.execute("SELECT farmer_id, farmer_name, farmer_email, farmer_phone, farmer_address FROM Farmer")
    df = pd.DataFrame(cursor.fetchall(), columns=["ID", "Name", "Email", "Phone", "Address"])
    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption(f"Total: **{len(df)}** farmers")
    else:
        st.info("No farmer records found.")

with tab_add:
    section_header("Add New Farmer")
    with st.form("add_farmer_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            name  = st.text_input("Full Name *", placeholder="e.g. Ali Khan")
            email = st.text_input("Email Address *", placeholder="ali@example.com")
        with c2:
            phone   = st.text_input("Phone Number", placeholder="+92 300 0000000")
            address = st.text_area("Address", placeholder="Village, District, Province", height=100)
        if st.form_submit_button("Add Farmer", use_container_width=True):
            if not name or not email:
                st.error("Name and Email are required fields.")
            else:
                cursor.execute(
                    "INSERT INTO Farmer (farmer_name, farmer_email, farmer_phone, farmer_address) VALUES (%s, %s, %s, %s)",
                    (name, email, phone, address)
                )
                conn.commit()
                st.success(f"Farmer **{name}** added successfully!")

with tab_update:
    section_header("Update Farmer")
    cursor.execute("SELECT farmer_id, farmer_name FROM Farmer")
    farmers = cursor.fetchall()
    if farmers:
        farmer_map = {f"{f[0]} – {f[1]}": f[0] for f in farmers}
        with st.form("update_farmer_form"):
            selected = st.selectbox("Select Farmer to Update", options=list(farmer_map.keys()))
            c1, c2  = st.columns(2)
            with c1:
                new_name    = st.text_input("New Name")
                new_email   = st.text_input("New Email")
            with c2:
                new_phone   = st.text_input("New Phone")
                new_address = st.text_area("New Address", height=100)
            if st.form_submit_button("Update Farmer", use_container_width=True):
                farmer_id = farmer_map[selected]
                cursor.execute("""
                    UPDATE Farmer SET farmer_name=%s, farmer_email=%s,
                        farmer_phone=%s, farmer_address=%s WHERE farmer_id=%s
                """, (new_name, new_email, new_phone, new_address, farmer_id))
                conn.commit()
                st.success("Farmer updated successfully!")
    else:
        st.info("No farmers available to update.")

with tab_delete:
    section_header("Delete Farmer")
    cursor.execute("SELECT farmer_id, farmer_name FROM Farmer")
    farmers = cursor.fetchall()
    if farmers:
        farmer_map = {f"{f[0]} – {f[1]}": f[0] for f in farmers}
        with st.form("delete_farmer_form"):
            selected  = st.selectbox("Select Farmer to Delete", options=list(farmer_map.keys()))
            confirmed = st.checkbox("I confirm I want to delete this farmer")
            if st.form_submit_button("Delete Farmer", use_container_width=True):
                if not confirmed:
                    st.warning("Please confirm the deletion first.")
                else:
                    cursor.execute("DELETE FROM Farmer WHERE farmer_id=%s", (farmer_map[selected],))
                    conn.commit()
                    st.warning("Farmer deleted successfully.")
    else:
        st.info("No farmers available to delete.")

cursor.close()
conn.close()