-- TABLE: FARMER
CREATE TABLE Farmer (
    farmer_id INT AUTO_INCREMENT PRIMARY KEY,
    farmer_name VARCHAR(100) NOT NULL,
    farmer_email VARCHAR(100) UNIQUE,
    farmer_phone VARCHAR(20),
    farmer_address VARCHAR(255)
);


-- TABLE: FARM
CREATE TABLE Farm (
    farm_id INT AUTO_INCREMENT PRIMARY KEY,
    farmer_id INT NOT NULL,
    farm_name VARCHAR(100) NOT NULL,
    farm_location VARCHAR(255),
    total_area DECIMAL(10,2),

    CONSTRAINT fk_farm_farmer
        FOREIGN KEY (farmer_id)
        REFERENCES Farmer(farmer_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


-- TABLE: FIELD

CREATE TABLE Field (
    field_id INT AUTO_INCREMENT PRIMARY KEY,
    farm_id INT NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    soil_type VARCHAR(50),
    field_area DECIMAL(10,2),

    CONSTRAINT fk_field_farm
        FOREIGN KEY (farm_id)
        REFERENCES Farm(farm_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


-- TABLE: CROP

CREATE TABLE Crop (
    crop_id INT AUTO_INCREMENT PRIMARY KEY,
    field_id INT NOT NULL, 
    crop_name VARCHAR(100) NOT NULL,
    planting_date DATE,
    expected_harvest_date DATE,

    CONSTRAINT fk_crop_field
        FOREIGN KEY (field_id)
        REFERENCES Field(field_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


-- TABLE: SENSOR

CREATE TABLE Sensor (
    sensor_id INT AUTO_INCREMENT PRIMARY KEY,
    field_id INT NOT NULL,
    sensor_type ENUM('Moisture', 'Temperature', 'pH') NOT NULL,
    installation_date DATE,
    current_status ENUM('Active', 'Inactive', 'Maintenance') DEFAULT 'Active',

    CONSTRAINT fk_sensor_field
        FOREIGN KEY (field_id)
        REFERENCES Field(field_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


-- TABLE: SOIL DATA

CREATE TABLE SoilData (
    soil_data_id INT AUTO_INCREMENT PRIMARY KEY,
    sensor_id INT NOT NULL,
    moisture_level DECIMAL(5,2),
    temperature DECIMAL(5,2),
    ph_level DECIMAL(4,2),
    recorded_time DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_soildata_sensor
        FOREIGN KEY (sensor_id)
        REFERENCES Sensor(sensor_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


-- TABLE: IRRIGATION SCHEDULE

CREATE TABLE IrrigationSchedule (
    schedule_id INT AUTO_INCREMENT PRIMARY KEY,
    field_id INT NOT NULL,
    start_time DATETIME,
    duration_minutes INT,
    water_amount DECIMAL(10,2),

    CONSTRAINT fk_irrigation_field
        FOREIGN KEY (field_id)
        REFERENCES Field(field_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


-- TABLE: WEATHER RECORD

CREATE TABLE WeatherRecord (
    weather_id INT AUTO_INCREMENT PRIMARY KEY,
    field_id INT NOT NULL,
    temperature DECIMAL(5,2),
    humidity DECIMAL(5,2),
    rainfall DECIMAL(5,2),
    record_date DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_weather_field
        FOREIGN KEY (field_id)
        REFERENCES Field(field_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);