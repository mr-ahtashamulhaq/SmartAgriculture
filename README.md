# 🌱 Smart Agriculture Monitoring System

<div align="center">

### Smart Farming Solution Built with Streamlit + MySQL

Monitor farms, crops, soil conditions, irrigation schedules, weather records, and smart agriculture analytics from a single dashboard.

<img src="https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python">
<img src="https://img.shields.io/badge/Streamlit-Frontend-red?style=for-the-badge&logo=streamlit">
<img src="https://img.shields.io/badge/MySQL-Database-orange?style=for-the-badge&logo=mysql">
<img src="https://img.shields.io/badge/DBMS-Project-success?style=for-the-badge">

</div>

---

# 📌 Project Overview

The **Smart Agriculture Monitoring System** is a DBMS-based smart farming platform developed to manage and monitor agricultural activities digitally.

The system provides:
- Farmer management
- Farm and field monitoring
- Crop tracking
- Sensor management
- Soil condition monitoring
- Weather analytics
- Irrigation scheduling
- Dashboard analytics and visualization

This project combines:
- **Database Management System**
- **Frontend Development**
- **Data Analytics**
- **Smart Agriculture Concepts**

into one complete software solution.

---

# 🚀 Features

## 👨‍🌾 Farmer Management
- Add farmers
- Update farmer details
- Delete records
- View farmer database

---

## 🚜 Farm & Field Management
- Manage multiple farms
- Assign fields to farms
- Store soil information
- Track field area and location

---

## 🌾 Crop Monitoring
- Add crops
- Track planting dates
- Track expected harvest dates

---

## 📡 Sensor Management
- Moisture sensors
- Temperature sensors
- pH sensors
- Sensor status monitoring

---

## 🌱 Soil Data Analytics
- Moisture level monitoring
- Soil temperature tracking
- pH value monitoring
- Real-time data storage

---

## ☁️ Weather Monitoring
- Temperature tracking
- Humidity monitoring
- Rainfall records
- Environmental analytics

---

## 💧 Irrigation Scheduling
- Irrigation planning
- Water usage monitoring
- Smart scheduling system

---

## 📊 Dashboard & Analytics
- KPI Cards
- Charts & Graphs
- Soil Moisture Analytics
- Rainfall Analysis
- Recent Monitoring Records

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend Logic |
| Streamlit | Frontend UI |
| MySQL | Database |
| Pandas | Data Handling |
| SQL | Database Queries |

---

# 🗂️ Project Structure

```bash
SmartAgriculture/
│
├── .streamlit/
│   └── config.toml
│
├── pages/
│   ├── farmers.py
│   ├── farms.py
│   ├── fields.py
│   ├── corps.py
│   ├── sensors.py
│   ├── soildata.py
│   ├── weather.py
│   └── irrigation.py
│
├── sql/
│   └── schema.sql
│
├── app.py
├── db.py
├── requirements.txt
└── README.md
````

---

# 🧩 Database Modules

The project contains the following relational database tables:

* Farmer
* Farm
* Field
* Crop
* Sensor
* SoilData
* IrrigationSchedule
* WeatherRecord

---

# 🔗 Database Relationships

```text
Farmer
   ↓
Farm
   ↓
Field
   ↓
Crop

Field
   ↓
Sensor
   ↓
SoilData

Field
   ↓
WeatherRecord

Field
   ↓
IrrigationSchedule
```

---

# ⚙️ Installation Guide

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/SmartAgriculture.git
```

---

## 2️⃣ Open Project Folder

```bash
cd SmartAgriculture
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Setup MySQL Database

Run:

```sql
sql/schema.sql
```

inside MySQL Workbench.

---

## 5️⃣ Configure Database Connection

Open:

```python
db.py
```

Update:

```python
host="localhost"
user="root"
password="your_password"
database="smart_agriculture_db"
```

---

## 6️⃣ Run Streamlit App

```bash
streamlit run app.py
```

---

# 📈 Dashboard Preview

The dashboard provides:

* System overview
* Environmental analytics
* Soil moisture trends
* Rainfall analysis
* Real-time monitoring records

---

# 👨‍💻 Developers

#### Muhammad Ahtasham Ul Haq : [LinkedIn](https://www.linkedin.com/in/mr-ahtasham-ul-haq/)


#### Muhammad Faizan : [LinkedIn](https://www.linkedin.com/in/muhammad-faizan-992b86320/)