import streamlit as st
import pandas as pd
from db import create_connection

st.set_page_config( page_title="Smart Agriculture System", page_icon="🌱" )

conn = create_connection()
cursor = conn.cursor()

st.title("Sensor Management")


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



# SENSOR ENUM OPTIONS
sensor_types = [ "Moisture", "Temperature", "pH" ]

sensor_status =  ["Active", "Inactive", "Maintenance"]



# VIEW SENSORS

st.subheader("Sensor Records")

if st.button("View Sensors"):

    view_query = """
    SELECT Sensor.sensor_id, Field.field_name, Sensor.sensor_type, Sensor.installation_date, Sensor.current_status
    FROM Sensor
    JOIN Field
    ON Sensor.field_id = Field.field_id
    """

    cursor.execute(view_query)

    result = cursor.fetchall()

    df = pd.DataFrame(
        result,
        columns=[ "Sensor ID", "Field Name", "Sensor Type", "Installation Date", "Current Status" ]
    )

    st.dataframe(df)




# ADD SENSOR

st.subheader("Add New Sensor")

selected_field = st.selectbox(
    "Select Field",
    options=list(field_options.keys())
)

sensor_type = st.selectbox(
    "Sensor Type",
    options=sensor_types
)

installation_date = st.date_input(
    "Installation Date"
)

current_status = st.selectbox(
    "Sensor Status",
    options=sensor_status
)

if st.button("Add Sensor"):

    field_id = field_options[selected_field]

    insert_query = """
    INSERT INTO Sensor
    ( field_id, sensor_type, installation_date, current_status )
    VALUES (%s, %s, %s, %s)
    """

    values = ( field_id, sensor_type, installation_date, current_status )

    cursor.execute(insert_query, values)

    conn.commit()

    st.success("Sensor Added Successfully")



# DELETE SENSOR

st.subheader("Delete Sensor")

delete_id = st.number_input(
    "Enter Sensor ID",
    min_value=1,
    step=1,
    key="delete_sensor"
)

if st.button("Delete Sensor"):

    delete_query = """
    DELETE FROM Sensor
    WHERE sensor_id = %s
    """

    cursor.execute(delete_query, (delete_id,))

    conn.commit()

    st.warning("Sensor Deleted Successfully")



# UPDATE SENSOR

st.subheader("Update Sensor")

update_id = st.number_input(
    "Sensor ID to Update",
    min_value=1,
    step=1,
    key="update_sensor"
)

new_field = st.selectbox(
    "Select New Field",
    options=list(field_options.keys()),
    key="new_sensor_field"
)

new_sensor_type = st.selectbox(
    "New Sensor Type",
    options=sensor_types
)

new_installation_date = st.date_input(
    "New Installation Date"
)

new_status = st.selectbox(
    "New Sensor Status",
    options=sensor_status
)

if st.button("Update Sensor"):

    field_id = field_options[new_field]

    update_query = """
    UPDATE Sensor
    SET
        field_id = %s,
        sensor_type = %s,
        installation_date = %s,
        current_status = %s
    WHERE sensor_id = %s
    """

    values = ( field_id, new_sensor_type, new_installation_date, new_status, update_id )

    cursor.execute(update_query, values)

    conn.commit()

    st.success("Sensor Updated Successfully")

