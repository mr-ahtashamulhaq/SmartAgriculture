import streamlit as st
import pandas as pd
from db import create_connection

conn = create_connection()
cursor = conn.cursor()

st.title("Soil Data Management")


# FETCH SENSORS FROM DATABASE

query = """
SELECT sensor_id, sensor_type
FROM Sensor
"""

cursor.execute(query)

sensors = cursor.fetchall() # LIST OF TUPLES -> sensors = [ (1, 'Moisture'), (2, 'Temperature') ]



# CREATE SENSOR DROPDOWN OPTIONS

sensor_options = {}

for sensor in sensors:
    sensor_name = f"{sensor[0]} - {sensor[1]}" # sensor_name = "1 - Moisture"
    sensor_options[sensor_name] = sensor[0]     # sensor_options["1 - Moisture"] = 1




# VIEW SOIL DATA

st.subheader("Soil Data Records")

if st.button("View Soil Data"):

    view_query = """
    SELECT SoilData.soil_data_id, Sensor.sensor_type, SoilData.moisture_level, SoilData.temperature, SoilData.ph_level, SoilData.recorded_time
    FROM SoilData
    JOIN Sensor
    ON SoilData.sensor_id = Sensor.sensor_id
    """

    cursor.execute(view_query)

    result = cursor.fetchall()

    df = pd.DataFrame(
        result,
        columns=[ "Soil Data ID", "Sensor Type", "Moisture", "Temperature", "pH Level", "Recorded Time" ] )

    st.dataframe(df)




# ADD SOIL DATA

st.subheader("Add Soil Data")

selected_sensor = st.selectbox(
    "Select Sensor",
    options=list(sensor_options.keys())
)

moisture_level = st.number_input(
    "Moisture Level",
    min_value=0.0,
    step=0.1
)

temperature = st.number_input(
    "Temperature",
    step=0.1
)

ph_level = st.number_input(
    "pH Level",
    min_value=0.0,
    max_value=14.0,
    step=0.1
)

if st.button("Add Soil Data"):

    sensor_id = sensor_options[selected_sensor]

    insert_query = """
    INSERT INTO SoilData
    ( sensor_id, moisture_level, temperature, ph_level )
    VALUES (%s, %s, %s, %s)
    """

    values = ( sensor_id, moisture_level, temperature, ph_level )

    cursor.execute(insert_query, values)

    conn.commit()

    st.success("Soil Data Added Successfully")




# DELETE SOIL DATA

st.subheader("Delete Soil Data")

delete_id = st.number_input(
    "Enter Soil Data ID",
    min_value=1,
    step=1,
    key="delete_soildata"
)

if st.button("Delete Soil Data"):

    delete_query = """
    DELETE FROM SoilData
    WHERE soil_data_id = %s
    """

    cursor.execute(delete_query, (delete_id,))

    conn.commit()

    st.warning("Soil Data Deleted Successfully")



# UPDATE SOIL DATA

st.subheader("Update Soil Data")

update_id = st.number_input(
    "Soil Data ID to Update",
    min_value=1,
    step=1,
    key="update_soildata"
)

new_sensor = st.selectbox(
    "Select New Sensor",
    options=list(sensor_options.keys()),
    key="new_soildata_sensor"
)

new_moisture = st.number_input(
    "New Moisture Level",
    min_value=0.0,
    step=0.1,
    key="new_moisture"
)

new_temperature = st.number_input(
    "New Temperature",
    step=0.1,
    key="new_temperature"
)

new_ph = st.number_input(
    "New pH Level",
    min_value=0.0,
    max_value=14.0,
    step=0.1,
    key="new_ph"
)

if st.button("Update Soil Data"):

    sensor_id = sensor_options[new_sensor]

    update_query = """
    UPDATE SoilData
    SET
        sensor_id = %s,
        moisture_level = %s,
        temperature = %s,
        ph_level = %s
    WHERE soil_data_id = %s
    """

    values = ( sensor_id, new_moisture, new_temperature, new_ph, update_id )

    cursor.execute(update_query, values)

    conn.commit()

    st.success("Soil Data Updated Successfully")

