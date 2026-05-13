import streamlit as st
import pandas as pd
from db import create_connection
from datetime import datetime

st.set_page_config( page_title="Smart Agriculture System", page_icon="🌱" )

conn = create_connection()
cursor = conn.cursor()

st.title("Irrigation Schedule Management")


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




# VIEW IRRIGATION SCHEDULES

st.subheader("Irrigation Records")

if st.button("View Irrigation Schedules"):

    view_query = """
    SELECT IrrigationSchedule.schedule_id, Field.field_name, IrrigationSchedule.start_time, IrrigationSchedule.duration_minutes, IrrigationSchedule.water_amount
    FROM IrrigationSchedule
    JOIN Field
    ON IrrigationSchedule.field_id = Field.field_id
    """

    cursor.execute(view_query)

    result = cursor.fetchall()

    df = pd.DataFrame(
        result,
        columns=[ "Schedule ID", "Field Name", "Start Time", "Duration (Minutes)", "Water Amount" ] )

    st.dataframe(df)




# ADD IRRIGATION SCHEDULE

st.subheader("Add Irrigation Schedule")

selected_field = st.selectbox(
    "Select Field",
    options=list(field_options.keys())
)

schedule_date = st.date_input(
    "Schedule Date"
)

schedule_time = st.time_input(
    "Schedule Time"
)

duration_minutes = st.number_input(
    "Duration (Minutes)",
    min_value=1,
    step=1
)

water_amount = st.number_input(
    "Water Amount",
    min_value=0.0,
    step=0.1
)

if st.button("Add Irrigation Schedule"):

    field_id = field_options[selected_field]

    start_datetime = datetime.combine( schedule_date, schedule_time )

    insert_query = """
    INSERT INTO IrrigationSchedule
    ( field_id, start_time, duration_minutes, water_amount )
    VALUES (%s, %s, %s, %s)
    """

    values = ( field_id, start_datetime, duration_minutes, water_amount )

    cursor.execute(insert_query, values)

    conn.commit()

    st.success("Irrigation Schedule Added Successfully")




# DELETE IRRIGATION SCHEDULE

st.subheader("Delete Irrigation Schedule")

delete_id = st.number_input(
    "Enter Schedule ID",
    min_value=1,
    step=1,
    key="delete_irrigation"
)

if st.button("Delete Irrigation Schedule"):

    delete_query = """
    DELETE FROM IrrigationSchedule
    WHERE schedule_id = %s
    """

    cursor.execute(delete_query, (delete_id,))

    conn.commit()

    st.warning("Irrigation Schedule Deleted Successfully")



# UPDATE IRRIGATION SCHEDULE

st.subheader("Update Irrigation Schedule")

update_id = st.number_input(
    "Schedule ID to Update",
    min_value=1,
    step=1,
    key="update_irrigation"
)

new_field = st.selectbox(
    "Select New Field",
    options=list(field_options.keys()),
    key="new_irrigation_field"
)

new_date = st.date_input(
    "New Schedule Date"
)

new_time = st.time_input(
    "New Schedule Time"
)

new_duration = st.number_input(
    "New Duration",
    min_value=1,
    step=1,
    key="new_duration"
)

new_water_amount = st.number_input(
    "New Water Amount",
    min_value=0.0,
    step=0.1,
    key="new_water_amount"
)

if st.button("Update Irrigation Schedule"):

    field_id = field_options[new_field]

    updated_datetime = datetime.combine(
        new_date,
        new_time
    )

    update_query = """
    UPDATE IrrigationSchedule
    SET
        field_id = %s,
        start_time = %s,
        duration_minutes = %s,
        water_amount = %s
    WHERE schedule_id = %s
    """

    values = ( field_id, updated_datetime, new_duration, new_water_amount, update_id )

    cursor.execute(update_query, values)

    conn.commit()

    st.success("Irrigation Schedule Updated Successfully")

