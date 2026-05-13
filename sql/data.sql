-- INSERT INTO FARMER

INSERT INTO Farmer
(farmer_name, farmer_email, farmer_phone, farmer_address)
VALUES
('Ahtasham Ul Haq', 'ahtasham@gmail.com', '03001234567', 'Bahria Town, Lahore'),
('Muhammad Faizan', 'faizan@gmail.com', '03011234567', 'Johar Town, Lahore'),
('Muhammad Taha', 'taha@gmail.com', '03021234567', 'Gulberg, Lahore'),
('Hasnain Ali', 'hasnain@gmail.com', '03031234567', 'Model Town, Lahore'),
('Abu Bakar', 'abubakar@gmail.com', '03041234567', 'DHA, Lahore'),
('Nouman Saeed', 'nouman@gmail.com', '03051234567', 'Satellite Town, Rawalpindi'),
('Shabir Butt', 'shabir@gmail.com', '03061234567', 'Saddar, Faisalabad'),
('Ali Hamza', 'alihamza@gmail.com', '03071234567', 'Cantt, Multan'),
('Osama Gull', 'osama@gmail.com', '03081234567', 'Hayatabad, Peshawar'),
('Akbar Ali', 'akbar@gmail.com', '03091234567', 'Defence Road, Sialkot');



-- INSERT INTO FARM

INSERT INTO Farm
(farmer_id, farm_name, farm_location, total_area)
VALUES
(1, 'Green Punjab Farm', 'Kasur, Punjab', 120.50),
(2, 'Al Rehman Agriculture Farm', 'Sheikhupura, Punjab', 95.00),
(3, 'River Side Farm', 'Sahiwal, Punjab', 140.75),
(4, 'Chaudhry Crops Farm', 'Okara, Punjab', 110.00),
(5, 'Dera Green Fields', 'Bahawalpur, Punjab', 180.25),
(6, 'Saeed Wheat Farm', 'Rawalpindi, Punjab', 90.50),
(7, 'Butt Agriculture Land', 'Faisalabad, Punjab', 130.00),
(8, 'Multan Mango Farm', 'Multan, Punjab', 160.00),
(9, 'KPK Smart Farm', 'Mardan, KPK', 100.75),
(10, 'Sialkot Rice Farm', 'Sialkot, Punjab', 115.25);



-- INSERT INTO FIELD

INSERT INTO Field
(farm_id, field_name, soil_type, field_area)
VALUES
(1, 'North Wheat Field', 'Clay', 40.50),
(2, 'Canal Side Field', 'Sandy', 35.00),
(3, 'Rice Production Field', 'Loamy', 55.75),
(4, 'South Crop Field', 'Clay', 42.25),
(5, 'Cotton Zone Field', 'Silty', 60.00),
(6, 'Vegetable Field', 'Loamy', 32.00),
(7, 'Sugarcane Field', 'Clay', 50.00),
(8, 'Mango Garden Field', 'Sandy', 75.50),
(9, 'Smart Irrigation Field', 'Loamy', 38.25),
(10, 'Premium Rice Field', 'Silty', 45.75);



-- INSERT INTO CROP

INSERT INTO Crop
(field_id, crop_name, planting_date, expected_harvest_date)
VALUES
(1, 'Wheat', '2025-11-10', '2026-04-15'),
(2, 'Maize', '2025-09-05', '2026-01-20'),
(3, 'Rice', '2025-06-12', '2025-11-18'),
(4, 'Potato', '2025-10-01', '2026-02-10'),
(5, 'Cotton', '2025-05-15', '2025-10-30'),
(6, 'Tomato', '2025-08-20', '2025-12-15'),
(7, 'Sugarcane', '2025-03-10', '2026-02-25'),
(8, 'Mango', '2025-02-18', '2025-07-25'),
(9, 'Chili', '2025-09-01', '2026-01-05'),
(10, 'Rice', '2025-06-20', '2025-11-28');



-- INSERT INTO SENSOR

INSERT INTO Sensor
(field_id, sensor_type, installation_date, current_status)
VALUES
(1, 'Moisture', '2025-01-10', 'Active'),
(2, 'Temperature', '2025-01-15', 'Active'),
(3, 'pH', '2025-02-01', 'Maintenance'),
(4, 'Moisture', '2025-02-10', 'Active'),
(5, 'Temperature', '2025-02-20', 'Inactive'),
(6, 'pH', '2025-03-01', 'Active'),
(7, 'Moisture', '2025-03-12', 'Active'),
(8, 'Temperature', '2025-03-20', 'Maintenance'),
(9, 'pH', '2025-04-05', 'Active'),
(10, 'Moisture', '2025-04-15', 'Active');



-- INSERT INTO SOILDATA

INSERT INTO SoilData
(sensor_id, moisture_level, temperature, ph_level, recorded_time)
VALUES
(1, 45.50, 28.20, 6.80, '2026-05-01 08:30:00'),
(2, 38.20, 31.50, 7.10, '2026-05-01 09:00:00'),
(3, 50.75, 27.80, 6.50, '2026-05-01 10:15:00'),
(4, 42.30, 29.40, 6.90, '2026-05-02 08:45:00'),
(5, 36.90, 33.20, 7.20, '2026-05-02 09:30:00'),
(6, 48.10, 26.70, 6.60, '2026-05-02 11:00:00'),
(7, 52.40, 30.00, 6.75, '2026-05-03 07:50:00'),
(8, 40.25, 32.60, 7.00, '2026-05-03 09:20:00'),
(9, 47.60, 28.90, 6.85, '2026-05-03 10:40:00'),
(10, 44.80, 29.70, 6.95, '2026-05-03 12:00:00');



-- INSERT INTO IRRIGATION SCHEDULE

INSERT INTO IrrigationSchedule
(field_id, start_time, duration_minutes, water_amount)
VALUES
(1, '2026-05-05 06:00:00', 45, 1200.50),
(2, '2026-05-05 07:00:00', 30, 950.00),
(3, '2026-05-05 08:15:00', 50, 1500.75),
(4, '2026-05-06 06:30:00', 40, 1100.00),
(5, '2026-05-06 07:45:00', 60, 1800.25),
(6, '2026-05-06 09:00:00', 35, 850.50),
(7, '2026-05-07 06:20:00', 55, 1600.00),
(8, '2026-05-07 07:40:00', 65, 2000.00),
(9, '2026-05-07 08:30:00', 38, 980.75),
(10, '2026-05-07 09:10:00', 42, 1250.25);



-- INSERT INTO WEATHER RECORD

INSERT INTO WeatherRecord
(field_id, temperature, humidity, rainfall, record_date)
VALUES
(1, 30.50, 65.00, 2.50, '2026-05-01 08:00:00'),
(2, 32.10, 58.20, 1.20, '2026-05-01 09:00:00'),
(3, 29.80, 70.50, 4.10, '2026-05-01 10:00:00'),
(4, 31.20, 60.00, 0.80, '2026-05-02 08:00:00'),
(5, 34.00, 55.40, 0.00, '2026-05-02 09:00:00'),
(6, 28.90, 72.10, 3.50, '2026-05-02 10:00:00'),
(7, 33.40, 59.00, 1.80, '2026-05-03 08:00:00'),
(8, 35.20, 52.30, 0.50, '2026-05-03 09:00:00'),
(9, 30.10, 66.70, 2.90, '2026-05-03 10:00:00'),
(10, 29.50, 69.80, 3.20, '2026-05-03 11:00:00');