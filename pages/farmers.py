import streamlit as st
from db import create_connection
import pandas as pd

st.title("Farmers Management")

conn = create_connection() # Create mySQL connection
cursor = conn.cursor() #cursor execute queries


st.subheader("Add New Farmer")

name = st.text_input("Farmer Name")  # create text box and store in name
email = st.text_input("Farmer Email")
phone = st.text_input("Farmer Phone")
address = st.text_area("Farmer Address") # multi-line input box

if st.button("Add Farmer"): # runs code only when clicked.
    
    #SQL Query
    query = """ 
    INSERT INTO Farmer
    (farmer_name, farmer_email, farmer_phone, farmer_address)
    VALUES (%s, %s, %s, %s)
    """

    values = (name, email, phone, address) # Tuple of values

    cursor.execute(query, values)   #Runs SQL Query

    conn.commit()   #save changes permanently

    st.success("Farmer Added Successfully")


st.subheader("Farmer Records")

if st.button("Farmer Records"):
    query = "SELECT * FROM Farmer"

    cursor.execute(query)

    result = cursor.fetchall()  # get all rows from query result


    df = pd.DataFrame(
        result,
        columns=["ID", "Name", "Email", "Phone", "Address"] )

    st.dataframe(df)


#----
st.subheader("Delete Farmer")

delete_id = st.number_input(
    "Enter Farmer ID",
    min_value=1,
    step=1
)

if st.button("Delete Farmer"):

    delete_query = """
    DELETE FROM Farmer
    WHERE farmer_id = %s
    """

    cursor.execute(delete_query, (delete_id,))  #Comma is must, without it python will not treat it as a tuple

    conn.commit()

    st.warning("Farmer Deleted Successfully")


# -----
st.subheader("Update Farmer")

update_id = st.number_input(
    "Farmer ID to Update",
    min_value=1,
    step=1,
    key="update_id"
)

new_name = st.text_input(
    "New Name"
)

new_email = st.text_input(
    "New Email"
)

new_phone = st.text_input(
    "New Phone"
)

new_address = st.text_area(
    "New Address"
)

if st.button("Update Farmer"):

    update_query = """
    UPDATE Farmer
    SET
        farmer_name = %s,
        farmer_email = %s,
        farmer_phone = %s,
        farmer_address = %s
    WHERE farmer_id = %s
    """

    values = (
        new_name,
        new_email,
        new_phone,
        new_address,
        update_id
    )

    cursor.execute(update_query, values)

    conn.commit()

    st.success("Farmer Updated Successfully")