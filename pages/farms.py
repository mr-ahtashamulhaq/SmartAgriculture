import streamlit as st
from db import create_connection
import pandas as pd
st.title("Farm Management")

conn = create_connection()
cursor = conn.cursor()


# Fetch Farmers from database
query = "SELECT farmer_id, farmer_name FROM Farmer"

cursor.execute(query)

farmers = cursor.fetchall() # It will return list of tuples : [(1, 'Ali'), (2, 'Ahmed')]

# Create DropDow option
farmer_options = {}

for farmer in farmers:
    farmer_options[farmer[1]] = farmer[0]



# --- VIEW FARMs WITH FARMER NAMES ---
st.subheader("Farm Records")

if st.button("View Farms"):

    view_query = """
    SELECT
        Farm.farm_id,
        Farmer.farmer_name,
        Farm.farm_name,
        Farm.farm_location,
        Farm.total_area
    FROM Farm
    JOIN Farmer
    ON Farm.farmer_id = Farmer.farmer_id
    """

    cursor.execute(view_query)

    result = cursor.fetchall()

    df = pd.DataFrame(
        result,
        columns=["ID", "Farmer", "Farm", "Location", "Area"] )

    st.dataframe(df)



# ----- Add Farm Form -----
st.subheader("Add New Farm")

selected_farmer = st.selectbox( "Select Farmer", options=list(farmer_options.keys()) )  # creates dropdown menu

farm_name = st.text_input("Farm Name")

farm_location = st.text_input("Farm Location")

total_area = st.number_input(
    "Total Area",
    min_value=0.0,
    step=1.0
)


if st.button("Add Farm"):

    farmer_id = farmer_options[selected_farmer]     # If User select Ahsan -> This dictionary return his id

    insert_query = """
    INSERT INTO Farm
    (farmer_id, farm_name, farm_location, total_area)
    VALUES (%s, %s, %s, %s)
    """

    values = ( farmer_id, farm_name, farm_location, total_area )

    cursor.execute(insert_query, values)

    conn.commit()

    st.success("Farm Added Successfully")


# --- DELETE FARMS ---
st.subheader("Delete Farm")

delete_id = st.number_input(
    "Enter Farm ID",
    min_value=1,
    step=1,
    key="delete_farm"
)

if st.button("Delete Farm"):

    delete_query = """
    DELETE FROM Farm
    WHERE farm_id = %s
    """

    cursor.execute(delete_query, (delete_id,))

    conn.commit()

    st.warning("Farm Deleted Successfully")


# --- UPDATE FARM ---
st.subheader("Update Farm")

update_id = st.number_input(
    "Farm ID to Update",
    min_value=1,
    step=1,
    key="update_farm"
)

new_farm_name = st.text_input("New Farm Name")

new_location = st.text_input("New Farm Location")

new_area = st.number_input(
    "New Total Area",
    min_value=0.0,
    step=1.0,
    key="new_area"
)

new_farmer = st.selectbox(
    "Select New Farmer",
    options=list(farmer_options.keys()),
    key="new_farmer"
)

if st.button("Update Farm"):

    farmer_id = farmer_options[new_farmer]

    update_query = """
    UPDATE Farm
    SET
        farmer_id = %s,
        farm_name = %s,
        farm_location = %s,
        total_area = %s
    WHERE farm_id = %s
    """

    values = (
        farmer_id,
        new_farm_name,
        new_location,
        new_area,
        update_id
    )

    cursor.execute(update_query, values)

    conn.commit()

    st.success("Farm Updated Successfully")