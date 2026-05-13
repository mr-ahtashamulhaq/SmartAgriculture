import streamlit as st
import pandas as pd
from db import create_connection

st.set_page_config( page_title="Smart Agriculture System", page_icon="🌱" )

conn = create_connection()
cursor = conn.cursor()

st.title("Crop Management")


# FETCH FIELDS FROM DATABASE
query = """
SELECT field_id, field_name
FROM Field
"""

cursor.execute(query)

fields = cursor.fetchall()



# CREATE FIELD DROPDOWN OPTIONS
field_options = {}

for field in fields:
    field_options[field[1]] = field[0]



# VIEW CROPS

st.subheader("Crop Records")

if st.button("View Crops"):

    view_query = """
    SELECT Crop.crop_id, Field.field_name, Crop.crop_name, Crop.planting_date, Crop.expected_harvest_date
    FROM Crop
    JOIN Field
    ON Crop.field_id = Field.field_id
    """

    cursor.execute(view_query)

    result = cursor.fetchall()

    df = pd.DataFrame(
        result,
        columns=[ "Crop ID", "Field Name", "Crop Name", "Planting Date", "Expected Harvest" ]
    )

    st.dataframe(df)




# ADD CROP

st.subheader("Add New Crop")

selected_field = st.selectbox(
    "Select Field",
    options=list(field_options.keys())
)

crop_name = st.text_input("Crop Name")

# creates calendar/date picker.
planting_date = st.date_input(
    "Planting Date"
)

harvest_date = st.date_input(
    "Expected Harvest Date"
)

if st.button("Add Crop"):

    field_id = field_options[selected_field]

    insert_query = """
    INSERT INTO Crop
    ( field_id, crop_name, planting_date, expected_harvest_date )
    VALUES (%s, %s, %s, %s)
    """

    values = ( field_id, crop_name, planting_date, harvest_date )

    cursor.execute(insert_query, values)

    conn.commit()

    st.success("Crop Added Successfully")



# DELETE CROP

st.subheader("Delete Crop")

delete_id = st.number_input(
    "Enter Crop ID",
    min_value=1,
    step=1,
    key="delete_crop"
)

if st.button("Delete Crop"):

    delete_query = """
    DELETE FROM Crop
    WHERE crop_id = %s
    """

    cursor.execute(delete_query, (delete_id,))

    conn.commit()

    st.warning("Crop Deleted Successfully")



# UPDATE CROP

st.subheader("Update Crop")

update_id = st.number_input(
    "Crop ID to Update",
    min_value=1,
    step=1,
    key="update_crop"
)

new_field = st.selectbox(
    "Select New Field",
    options=list(field_options.keys()),
    key="new_field_crop"
)

new_crop_name = st.text_input(
    "New Crop Name"
)

new_planting_date = st.date_input(
    "New Planting Date"
)

new_harvest_date = st.date_input(
    "New Harvest Date"
)

if st.button("Update Crop"):

    field_id = field_options[new_field]

    update_query = """
    UPDATE Crop
    SET
        field_id = %s,
        crop_name = %s,
        planting_date = %s,
        expected_harvest_date = %s
    WHERE crop_id = %s
    """

    values = ( field_id, new_crop_name, new_planting_date, new_harvest_date, update_id )

    cursor.execute(update_query, values)

    conn.commit()

    st.success("Crop Updated Successfully")
