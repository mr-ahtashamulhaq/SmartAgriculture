import streamlit as st
import pandas as pd
from db import create_connection


# PAGE CONFIGURATION

st.set_page_config(
    page_title="Smart Agriculture System",
    page_icon="🌱",
    layout="wide"
)


# CUSTOM CSS

st.markdown("""
<style>

/* Main App */
.main {
    padding-top: 1rem;
    padding-bottom: 2rem;
}

/* Metric Cards */
[data-testid="metric-container"] {
    background-color: #f7f9fc;
    border: 1px solid #e5e7eb;
    padding: 20px;
    border-radius: 16px;
}

/* Metric Labels */
[data-testid="metric-container"] label {
    color: #64748b !important;
    font-weight: 600;
}

/* Metric Values */
[data-testid="metric-container"] div {
    color: #1e293b;
}

/* Section Spacing */
.block-container {
    padding-top: 2rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    border-right: 1px solid #e5e7eb;
}

/* Dataframe Styling */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #e5e7eb;
}

</style>
""", unsafe_allow_html=True)


# DATABASE CONNECTION

conn = create_connection()
cursor = conn.cursor()


# SIDEBAR

st.sidebar.markdown("# 🌱 Smart Agriculture")

st.sidebar.markdown("""
Smart Agriculture Monitoring System

### Team Members
- Ahtasham
- Faizan
""")

st.sidebar.markdown("---")

st.sidebar.success("System Status: Online")


# HERO SECTION

st.markdown("""
# Smart Agriculture Monitoring System

Modern smart farming dashboard for monitoring:
- crops
- soil conditions
- weather records
- irrigation schedules
- agricultural analytics
""")

st.markdown("---")


# SYSTEM OVERVIEW

st.subheader("System Overview")


# TOTAL FARMERS

cursor.execute("SELECT COUNT(*) FROM Farmer")
total_farmers = cursor.fetchone()[0]


# TOTAL FARMS

cursor.execute("SELECT COUNT(*) FROM Farm")
total_farms = cursor.fetchone()[0]


# TOTAL FIELDS

cursor.execute("SELECT COUNT(*) FROM Field")
total_fields = cursor.fetchone()[0]


# TOTAL SENSORS

cursor.execute("SELECT COUNT(*) FROM Sensor")
total_sensors = cursor.fetchone()[0]


# KPI CARDS

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Farmers",
    total_farmers
)

col2.metric(
    "Total Farms",
    total_farms
)

col3.metric(
    "Total Fields",
    total_fields
)

col4.metric(
    "Total Sensors",
    total_sensors
)


# ENVIRONMENTAL ANALYTICS

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("Environmental Analytics")


# AVG TEMPERATURE

cursor.execute("""
SELECT AVG(temperature)
FROM SoilData
""")

avg_temp = cursor.fetchone()[0]


# AVG MOISTURE

cursor.execute("""
SELECT AVG(moisture_level)
FROM SoilData
""")

avg_moisture = cursor.fetchone()[0]


# AVG RAINFALL

cursor.execute("""
SELECT AVG(rainfall)
FROM WeatherRecord
""")

avg_rainfall = cursor.fetchone()[0]


# ANALYTICS CARDS

col1, col2, col3 = st.columns(3)

col1.metric(
    "Average Temperature",
    f"{avg_temp:.2f} °C"
    if avg_temp is not None else "No Data"
)

col2.metric(
    "Average Moisture",
    f"{avg_moisture:.2f}"
    if avg_moisture is not None else "No Data"
)

col3.metric(
    "Average Rainfall",
    f"{avg_rainfall:.2f} mm"
    if avg_rainfall is not None else "No Data"
)


# CHARTS SECTION

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("Analytics & Trends")


# SOIL MOISTURE CHART

chart_query = """
SELECT
    recorded_time,
    moisture_level
FROM SoilData
ORDER BY recorded_time
"""

cursor.execute(chart_query)

chart_result = cursor.fetchall()

chart_df = pd.DataFrame(
    chart_result,
    columns=[
        "Recorded Time",
        "Moisture Level"
    ]
)


# RAINFALL CHART

rain_query = """
SELECT
    record_date,
    rainfall
FROM WeatherRecord
ORDER BY record_date
"""

cursor.execute(rain_query)

rain_result = cursor.fetchall()

rain_df = pd.DataFrame(
    rain_result,
    columns=[
        "Record Date",
        "Rainfall"
    ]
)


# CHART LAYOUT

col1, col2 = st.columns(2)

with col1:

    st.markdown("#### Soil Moisture Trend")

    if not chart_df.empty:

        st.line_chart(
            chart_df.set_index("Recorded Time")
        )

    else:
        st.info("No soil moisture data available")


with col2:

    st.markdown("#### Rainfall Analysis")

    if not rain_df.empty:

        st.bar_chart(
            rain_df.set_index("Record Date")
        )

    else:
        st.info("No rainfall data available")


# RECENT RECORDS SECTION

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("Recent Monitoring Records")


# SOIL DATA QUERY

soil_query = """
SELECT
    SoilData.soil_data_id,
    Sensor.sensor_type,
    SoilData.moisture_level,
    SoilData.temperature,
    SoilData.ph_level,
    SoilData.recorded_time
FROM SoilData
JOIN Sensor
ON SoilData.sensor_id = Sensor.sensor_id
ORDER BY SoilData.recorded_time DESC
LIMIT 5
"""

cursor.execute(soil_query)

soil_result = cursor.fetchall()

soil_df = pd.DataFrame(
    soil_result,
    columns=[
        "ID",
        "Sensor",
        "Moisture",
        "Temperature",
        "pH",
        "Recorded Time"
    ]
)


# WEATHER DATA QUERY

weather_query = """
SELECT
    WeatherRecord.weather_id,
    Field.field_name,
    WeatherRecord.temperature,
    WeatherRecord.humidity,
    WeatherRecord.rainfall,
    WeatherRecord.record_date
FROM WeatherRecord
JOIN Field
ON WeatherRecord.field_id = Field.field_id
ORDER BY WeatherRecord.record_date DESC
LIMIT 5
"""

cursor.execute(weather_query)

weather_result = cursor.fetchall()

weather_df = pd.DataFrame(
    weather_result,
    columns=[
        "Weather ID",
        "Field Name",
        "Temperature",
        "Humidity",
        "Rainfall",
        "Record Date"
    ]
)


# TABLE LAYOUT

col1, col2 = st.columns(2)

with col1:

    st.markdown("#### Latest Soil Records")

    if not soil_df.empty:

        st.dataframe(
            soil_df,
            use_container_width=True
        )

    else:
        st.info("No soil data available")


with col2:

    st.markdown("#### Latest Weather Records")

    if not weather_df.empty:

        st.dataframe(
            weather_df,
            use_container_width=True
        )

    else:
        st.info("No weather data available")