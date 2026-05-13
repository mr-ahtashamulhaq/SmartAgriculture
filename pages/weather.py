import streamlit as st
import pandas as pd
from db import create_connection

st.set_page_config( page_title="Smart Agriculture System", page_icon="🌱" )

conn = create_connection()
cursor = conn.cursor()

st.title("Weather Records Management")


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




# VIEW WEATHER RECORDS

st.subheader("Weather Records")

if st.button("View Weather Records"):

    view_query = """
    SELECT WeatherRecord.weather_id, Field.field_name, WeatherRecord.temperature, WeatherRecord.humidity, WeatherRecord.rainfall, WeatherRecord.record_date
    FROM WeatherRecord
    JOIN Field
    ON WeatherRecord.field_id = Field.field_id
    """

    cursor.execute(view_query)

    result = cursor.fetchall()

    df = pd.DataFrame(
        result,
        columns=[ "Weather ID", "Field Name", "Temperature", "Humidity", "Rainfall", "Record Date" ]
    )

    st.dataframe(df)




# ADD WEATHER RECORD

st.subheader("Add Weather Record")

selected_field = st.selectbox(
    "Select Field",
    options=list(field_options.keys())
)

temperature = st.number_input(
    "Temperature",
    step=0.1
)

humidity = st.number_input(
    "Humidity",
    min_value=0.0,
    max_value=100.0,
    step=0.1
)

rainfall = st.number_input(
    "Rainfall",
    min_value=0.0,
    step=0.1
)

if st.button("Add Weather Record"):

    field_id = field_options[selected_field]

    insert_query = """
    INSERT INTO WeatherRecord
    ( field_id, temperature, humidity, rainfall )
    VALUES (%s, %s, %s, %s)
    """

    values = ( field_id, temperature, humidity, rainfall )

    cursor.execute(insert_query, values)

    conn.commit()

    st.success("Weather Record Added Successfully")




# DELETE WEATHER RECORD

st.subheader("Delete Weather Record")

delete_id = st.number_input(
    "Enter Weather Record ID",
    min_value=1,
    step=1,
    key="delete_weather"
)

if st.button("Delete Weather Record"):

    delete_query = """
    DELETE FROM WeatherRecord
    WHERE weather_id = %s
    """

    cursor.execute(delete_query, (delete_id,))

    conn.commit()

    st.warning("Weather Record Deleted Successfully")



# UPDATE WEATHER RECORD

st.subheader("Update Weather Record")

update_id = st.number_input(
    "Weather Record ID to Update",
    min_value=1,
    step=1,
    key="update_weather"
)

new_field = st.selectbox(
    "Select New Field",
    options=list(field_options.keys()),
    key="new_weather_field"
)

new_temperature = st.number_input(
    "New Temperature",
    step=0.1,
    key="new_weather_temp"
)

new_humidity = st.number_input(
    "New Humidity",
    min_value=0.0,
    max_value=100.0,
    step=0.1,
    key="new_weather_humidity"
)

new_rainfall = st.number_input(
    "New Rainfall",
    min_value=0.0,
    step=0.1,
    key="new_weather_rainfall"
)

if st.button("Update Weather Record"):

    field_id = field_options[new_field]

    update_query = """
    UPDATE WeatherRecord
    SET
        field_id = %s,
        temperature = %s,
        humidity = %s,
        rainfall = %s
    WHERE weather_id = %s
    """

    values = ( field_id, new_temperature, new_humidity, new_rainfall, update_id )

    cursor.execute(update_query, values)

    conn.commit()

    st.success("Weather Record Updated Successfully")

