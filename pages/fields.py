import streamlit as st
from db import create_connection
import pandas as pd

st.set_page_config( page_title="Smart Agriculture System", page_icon="🌱" )

st.title("Fields Management")

conn = create_connection()
cursor = conn.cursor()

query = """
SELECT farm_id, farm_name
FROM Farm
"""

cursor.execute(query)

farms = cursor.fetchall()

# -Create FARM mapping dict -> farmname : farmID
farm_options = {}

for farm in farms:
    farm_options[farm[1]] = farm[0]



# --- VIEW Fields ---
st.subheader("Field Records")

if st.button("View Fields"):

    view_query = """
    SELECT Field.field_id, Farm.farm_name, Field.field_name, Field.soil_type, Field.field_area
    FROM Field
    JOIN Farm
    ON Field.farm_id = Farm.farm_id
    """

    cursor.execute(view_query)

    result = cursor.fetchall()

    df = pd.DataFrame( result, columns=[ "Field ID", "Farm Name", "Field Name", "Soil Type", "Field Area" ] )

    st.dataframe(df)



# --- ADD Field ---
st.subheader("Add New Field")

selected_farm = st.selectbox(
    "Select Farm",
    options=list(farm_options.keys())
)

field_name = st.text_input("Field Name")

soil_type = st.text_input("Soil Type")

field_area = st.number_input(
    "Field Area",
    min_value=0.0,
    step=1.0
)


# ---  Insert Field Query

if st.button("Add Field"):

    farm_id = farm_options[selected_farm]

    insert_query = """
    INSERT INTO Field
    (farm_id, field_name, soil_type, field_area)
    VALUES (%s, %s, %s, %s)
    """

    values = ( farm_id, field_name, soil_type, field_area )

    cursor.execute(insert_query, values)

    conn.commit()

    st.success("Field Added Successfully")



# ---DELETE Field ---
st.subheader("Delete Field")

delete_id = st.number_input(
    "Enter Field ID",
    min_value=1,
    step=1,
    key="delete_field"
)

if st.button("Delete Field"):

    delete_query = """
    DELETE FROM Field
    WHERE field_id = %s
    """

    cursor.execute(delete_query, (delete_id,))

    conn.commit()

    st.warning("Field Deleted Successfully")


# --- UPDATE Existing Field ---
st.subheader("Update Field")

update_id = st.number_input(
    "Field ID to Update",
    min_value=1,
    step=1,
    key="update_field"
)

new_field_name = st.text_input(
    "New Field Name"
)

new_soil_type = st.text_input(
    "New Soil Type"
)

new_field_area = st.number_input(
    "New Field Area",
    min_value=0.0,
    step=1.0,
    key="new_field_area"
)

new_farm = st.selectbox(
    "Select New Farm",
    options=list(farm_options.keys()),
    key="new_farm"
)

if st.button("Update Field"):

    farm_id = farm_options[new_farm]

    update_query = """
    UPDATE Field
    SET
        farm_id = %s,
        field_name = %s,
        soil_type = %s,
        field_area = %s
    WHERE field_id = %s
    """

    values = ( farm_id, new_field_name, new_soil_type, new_field_area, update_id )

    cursor.execute(update_query, values)

    conn.commit()

    st.success("Field Updated Successfully")

