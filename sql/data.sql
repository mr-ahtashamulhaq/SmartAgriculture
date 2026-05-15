-- =========================================
-- INSERT DATA INTO FARMER
-- =========================================

INSERT INTO Farmer
(farmer_name, farmer_email, farmer_phone, farmer_address)
VALUES

('Ahtasham Ul Haq', 'ahtasham@gmail.com', '03001234501', 'Lahore, Punjab'),
('Muhammad Faizan', 'faizan@gmail.com', '03001234502', 'Faisalabad, Punjab'),
('Hasnain Ali Asghar', 'hasnain@gmail.com', '03001234503', 'Multan, Punjab'),
('Abu Bakar Subhan', 'abubakar@gmail.com', '03001234504', 'Sahiwal, Punjab'),
('Ehtisham Zahid', 'ehtisham@gmail.com', '03001234505', 'Bahawalpur, Punjab'),

('Ali Raza', 'aliraza@gmail.com', '03001234506', 'Okara, Punjab'),
('Usman Tariq', 'usman@gmail.com', '03001234507', 'Kasur, Punjab'),
('Hamza Shahid', 'hamza@gmail.com', '03001234508', 'Gujranwala, Punjab'),
('Bilal Ahmed', 'bilal@gmail.com', '03001234509', 'Sheikhupura, Punjab'),
('Nouman Javed', 'nouman@gmail.com', '03001234510', 'Rahim Yar Khan, Punjab'),

('Saad Khalid', 'saad@gmail.com', '03001234511', 'Vehari, Punjab'),
('Zain Ali', 'zain@gmail.com', '03001234512', 'Mianwali, Punjab'),
('Hassan Raza', 'hassan@gmail.com', '03001234513', 'Narowal, Punjab'),
('Taha Imran', 'taha@gmail.com', '03001234514', 'Sialkot, Punjab'),
('Shahzaib Malik', 'shahzaib@gmail.com', '03001234515', 'Jhang, Punjab'),

('Umer Farooq', 'umer@gmail.com', '03001234516', 'Pakpattan, Punjab'),
('Adeel Ahmed', 'adeel@gmail.com', '03001234517', 'Attock, Punjab'),
('Rizwan Ali', 'rizwan@gmail.com', '03001234518', 'Dera Ghazi Khan, Punjab'),
('Kamran Haider', 'kamran@gmail.com', '03001234519', 'Muzaffargarh, Punjab'),
('Waqas Ahmad', 'waqas@gmail.com', '03001234520', 'Chiniot, Punjab'),

('Imran Yousaf', 'imran@gmail.com', '03001234521', 'Hyderabad, Sindh'),
('Shahmeer Khan', 'shahmeer@gmail.com', '03001234522', 'Sukkur, Sindh'),
('Arslan Butt', 'arslan@gmail.com', '03001234523', 'Larkana, Sindh'),
('Danish Iqbal', 'danish@gmail.com', '03001234524', 'Nawabshah, Sindh'),
('Jawad Hussain', 'jawad@gmail.com', '03001234525', 'Mirpur Khas, Sindh'),

('Muneeb Ashraf', 'muneeb@gmail.com', '03001234526', 'Peshawar, KPK'),
('Asad Ullah', 'asad@gmail.com', '03001234527', 'Mardan, KPK'),
('Yasir Mehmood', 'yasir@gmail.com', '03001234528', 'Swat, KPK'),
('Fahad Khan', 'fahad@gmail.com', '03001234529', 'Abbottabad, KPK'),
('Shoaib Akhtar', 'shoaib@gmail.com', '03001234530', 'Quetta, Balochistan');



-- =========================================
-- INSERT DATA INTO FARM
-- =========================================

INSERT INTO Farm
(farmer_id, farm_name, farm_location, total_area)
VALUES

(1, 'Green Valley Farm', 'Lahore', 25.50),
(2, 'Punjab Agro Farm', 'Faisalabad', 40.00),
(3, 'Al Noor Farm', 'Multan', 18.75),
(4, 'Subhan Agriculture Farm', 'Sahiwal', 32.20),
(5, 'Zahid Smart Farm', 'Bahawalpur', 28.00),

(6, 'Raza Crops Farm', 'Okara', 22.40),
(7, 'Tariq Agriculture Land', 'Kasur', 35.60),
(8, 'Shahid Agro Farm', 'Gujranwala', 27.90),
(9, 'Ahmed Wheat Farm', 'Sheikhupura', 41.30),
(10, 'Javed Smart Fields', 'Rahim Yar Khan', 30.00),

(11, 'Khalid Farming Zone', 'Vehari', 20.50),
(12, 'Ali Green Farm', 'Mianwali', 24.10),
(13, 'Raza Cotton Farm', 'Narowal', 26.75),
(14, 'Imran Rice Farm', 'Sialkot', 29.50),
(15, 'Malik Agro Farm', 'Jhang', 34.60),

(16, 'Farooq Farms', 'Pakpattan', 38.40),
(17, 'Adeel Smart Farm', 'Attock', 21.70),
(18, 'Rizwan Agriculture Farm', 'DG Khan', 42.30),
(19, 'Haider Crops Farm', 'Muzaffargarh', 31.80),
(20, 'Ahmad Irrigation Farm', 'Chiniot', 19.90),

(21, 'Yousaf Green Land', 'Hyderabad', 33.00),
(22, 'Khan Farming System', 'Sukkur', 44.10),
(23, 'Butt Rice Farm', 'Larkana', 27.40),
(24, 'Iqbal Cotton Farm', 'Nawabshah', 23.50),
(25, 'Hussain Agro Farm', 'Mirpur Khas', 36.70),

(26, 'Ashraf Smart Agriculture', 'Peshawar', 25.90),
(27, 'Asad Green Farm', 'Mardan', 30.80),
(28, 'Yasir Wheat Farm', 'Swat', 28.60),
(29, 'Fahad Agro Land', 'Abbottabad', 22.90),
(30, 'Akhtar Farming Farm', 'Quetta', 40.20);



-- =========================================
-- INSERT DATA INTO FIELD
-- =========================================

INSERT INTO Field
(farm_id, field_name, soil_type, field_area)
VALUES

(1, 'Field A1', 'Loamy', 10.50),
(2, 'Field B1', 'Clay', 15.00),
(3, 'Field C1', 'Sandy', 8.75),
(4, 'Field D1', 'Silty', 12.20),
(5, 'Field E1', 'Loamy', 14.00),

(6, 'Field F1', 'Clay', 9.40),
(7, 'Field G1', 'Sandy', 16.60),
(8, 'Field H1', 'Loamy', 13.90),
(9, 'Field I1', 'Silty', 18.30),
(10, 'Field J1', 'Clay', 11.00),

(11, 'Field K1', 'Loamy', 12.50),
(12, 'Field L1', 'Sandy', 10.10),
(13, 'Field M1', 'Clay', 14.75),
(14, 'Field N1', 'Silty', 13.50),
(15, 'Field O1', 'Loamy', 15.60),

(16, 'Field P1', 'Clay', 17.40),
(17, 'Field Q1', 'Sandy', 8.70),
(18, 'Field R1', 'Loamy', 19.30),
(19, 'Field S1', 'Silty', 12.80),
(20, 'Field T1', 'Clay', 9.90),

(21, 'Field U1', 'Loamy', 16.00),
(22, 'Field V1', 'Sandy', 18.10),
(23, 'Field W1', 'Clay', 13.40),
(24, 'Field X1', 'Silty', 11.50),
(25, 'Field Y1', 'Loamy', 17.70),

(26, 'Field Z1', 'Clay', 14.90),
(27, 'Field AA1', 'Sandy', 12.80),
(28, 'Field AB1', 'Loamy', 15.60),
(29, 'Field AC1', 'Silty', 10.90),
(30, 'Field AD1', 'Clay', 18.20);



-- =========================================
-- INSERT DATA INTO CROP
-- =========================================

INSERT INTO Crop
(field_id, crop_name, planting_date, expected_harvest_date)
VALUES

(1, 'Wheat', '2025-01-10', '2025-05-20'),
(2, 'Rice', '2025-02-15', '2025-06-25'),
(3, 'Cotton', '2025-03-01', '2025-08-10'),
(4, 'Sugarcane', '2025-01-18', '2025-10-15'),
(5, 'Maize', '2025-02-20', '2025-06-18'),

(6, 'Wheat', '2025-01-12', '2025-05-22'),
(7, 'Rice', '2025-02-10', '2025-06-20'),
(8, 'Cotton', '2025-03-05', '2025-08-15'),
(9, 'Sugarcane', '2025-01-25', '2025-10-18'),
(10, 'Maize', '2025-02-28', '2025-06-30'),

(11, 'Wheat', '2025-01-08', '2025-05-18'),
(12, 'Rice', '2025-02-12', '2025-06-22'),
(13, 'Cotton', '2025-03-08', '2025-08-20'),
(14, 'Sugarcane', '2025-01-28', '2025-10-22'),
(15, 'Maize', '2025-02-26', '2025-06-28'),

(16, 'Wheat', '2025-01-15', '2025-05-25'),
(17, 'Rice', '2025-02-18', '2025-06-26'),
(18, 'Cotton', '2025-03-12', '2025-08-25'),
(19, 'Sugarcane', '2025-01-20', '2025-10-12'),
(20, 'Maize', '2025-02-22', '2025-06-24'),

(21, 'Wheat', '2025-01-11', '2025-05-19'),
(22, 'Rice', '2025-02-17', '2025-06-27'),
(23, 'Cotton', '2025-03-09', '2025-08-19'),
(24, 'Sugarcane', '2025-01-30', '2025-10-25'),
(25, 'Maize', '2025-02-25', '2025-06-29'),

(26, 'Wheat', '2025-01-14', '2025-05-24'),
(27, 'Rice', '2025-02-21', '2025-06-30'),
(28, 'Cotton', '2025-03-11', '2025-08-21'),
(29, 'Sugarcane', '2025-01-27', '2025-10-20'),
(30, 'Maize', '2025-02-24', '2025-06-26');

-- =========================================
-- INSERT DATA INTO SENSOR
-- =========================================

INSERT INTO Sensor
(field_id, sensor_type, installation_date, current_status)
VALUES

(1, 'Moisture', '2025-01-05', 'Active'),
(2, 'Temperature', '2025-01-06', 'Active'),
(3, 'pH', '2025-01-07', 'Maintenance'),
(4, 'Moisture', '2025-01-08', 'Active'),
(5, 'Temperature', '2025-01-09', 'Inactive'),

(6, 'pH', '2025-01-10', 'Active'),
(7, 'Moisture', '2025-01-11', 'Active'),
(8, 'Temperature', '2025-01-12', 'Maintenance'),
(9, 'pH', '2025-01-13', 'Active'),
(10, 'Moisture', '2025-01-14', 'Active'),

(11, 'Temperature', '2025-01-15', 'Inactive'),
(12, 'pH', '2025-01-16', 'Active'),
(13, 'Moisture', '2025-01-17', 'Active'),
(14, 'Temperature', '2025-01-18', 'Maintenance'),
(15, 'pH', '2025-01-19', 'Active'),

(16, 'Moisture', '2025-01-20', 'Active'),
(17, 'Temperature', '2025-01-21', 'Inactive'),
(18, 'pH', '2025-01-22', 'Active'),
(19, 'Moisture', '2025-01-23', 'Maintenance'),
(20, 'Temperature', '2025-01-24', 'Active'),

(21, 'pH', '2025-01-25', 'Active'),
(22, 'Moisture', '2025-01-26', 'Active'),
(23, 'Temperature', '2025-01-27', 'Maintenance'),
(24, 'pH', '2025-01-28', 'Active'),
(25, 'Moisture', '2025-01-29', 'Inactive'),

(26, 'Temperature', '2025-01-30', 'Active'),
(27, 'pH', '2025-01-31', 'Active'),
(28, 'Moisture', '2025-02-01', 'Maintenance'),
(29, 'Temperature', '2025-02-02', 'Active'),
(30, 'pH', '2025-02-03', 'Active');



-- =========================================
-- INSERT DATA INTO SOILDATA
-- =========================================

INSERT INTO SoilData
(sensor_id, moisture_level, temperature, ph_level, recorded_time)
VALUES

(1, 45.50, 28.40, 6.80, '2025-07-01 08:00:00'),
(2, 42.30, 30.10, 6.70, '2025-07-01 09:00:00'),
(3, 39.80, 29.50, 7.10, '2025-07-01 10:00:00'),
(4, 50.20, 27.80, 6.60, '2025-07-01 11:00:00'),
(5, 47.10, 31.20, 6.90, '2025-07-01 12:00:00'),

(6, 43.60, 28.90, 7.00, '2025-07-02 08:00:00'),
(7, 46.20, 29.80, 6.50, '2025-07-02 09:00:00'),
(8, 41.00, 30.50, 6.80, '2025-07-02 10:00:00'),
(9, 38.70, 31.00, 7.20, '2025-07-02 11:00:00'),
(10, 52.40, 27.20, 6.40, '2025-07-02 12:00:00'),

(11, 49.30, 28.00, 6.70, '2025-07-03 08:00:00'),
(12, 44.50, 29.40, 7.00, '2025-07-03 09:00:00'),
(13, 40.90, 30.60, 6.90, '2025-07-03 10:00:00'),
(14, 37.80, 31.50, 7.30, '2025-07-03 11:00:00'),
(15, 51.60, 27.50, 6.50, '2025-07-03 12:00:00'),

(16, 48.70, 28.30, 6.80, '2025-07-04 08:00:00'),
(17, 43.20, 29.90, 7.10, '2025-07-04 09:00:00'),
(18, 39.40, 30.80, 6.60, '2025-07-04 10:00:00'),
(19, 36.90, 31.80, 7.20, '2025-07-04 11:00:00'),
(20, 53.10, 27.00, 6.40, '2025-07-04 12:00:00'),

(21, 47.50, 28.70, 6.90, '2025-07-05 08:00:00'),
(22, 45.10, 29.60, 6.80, '2025-07-05 09:00:00'),
(23, 42.00, 30.20, 7.00, '2025-07-05 10:00:00'),
(24, 38.20, 31.40, 7.10, '2025-07-05 11:00:00'),
(25, 50.80, 27.40, 6.50, '2025-07-05 12:00:00'),

(26, 46.60, 28.50, 6.70, '2025-07-06 08:00:00'),
(27, 44.80, 29.70, 6.90, '2025-07-06 09:00:00'),
(28, 41.30, 30.90, 7.20, '2025-07-06 10:00:00'),
(29, 37.50, 31.60, 7.00, '2025-07-06 11:00:00'),
(30, 52.00, 27.10, 6.60, '2025-07-06 12:00:00');


-- =========================================
-- INSERT DATA INTO IRRIGATION SCHEDULE
-- =========================================

INSERT INTO IrrigationSchedule
(field_id, start_time, duration_minutes, water_amount)
VALUES

(1, '2025-07-01 06:00:00', 30, 120.50),
(2, '2025-07-01 06:30:00', 25, 100.00),
(3, '2025-07-01 07:00:00', 35, 140.75),
(4, '2025-07-01 07:30:00', 40, 160.20),
(5, '2025-07-01 08:00:00', 20, 90.40),

(6, '2025-07-02 06:00:00', 28, 110.30),
(7, '2025-07-02 06:30:00', 32, 135.60),
(8, '2025-07-02 07:00:00', 26, 105.25),
(9, '2025-07-02 07:30:00', 38, 150.00),
(10, '2025-07-02 08:00:00', 24, 98.70),

(11, '2025-07-03 06:00:00', 31, 125.80),
(12, '2025-07-03 06:30:00', 29, 118.40),
(13, '2025-07-03 07:00:00', 36, 145.90),
(14, '2025-07-03 07:30:00', 42, 170.30),
(15, '2025-07-03 08:00:00', 22, 92.10),

(16, '2025-07-04 06:00:00', 33, 132.00),
(17, '2025-07-04 06:30:00', 27, 108.50),
(18, '2025-07-04 07:00:00', 39, 158.60),
(19, '2025-07-04 07:30:00', 41, 165.90),
(20, '2025-07-04 08:00:00', 23, 95.40),

(21, '2025-07-05 06:00:00', 30, 122.70),
(22, '2025-07-05 06:30:00', 34, 138.20),
(23, '2025-07-05 07:00:00', 25, 101.50),
(24, '2025-07-05 07:30:00', 37, 149.80),
(25, '2025-07-05 08:00:00', 21, 89.60),

(26, '2025-07-06 06:00:00', 32, 130.40),
(27, '2025-07-06 06:30:00', 28, 112.90),
(28, '2025-07-06 07:00:00', 35, 143.10),
(29, '2025-07-06 07:30:00', 40, 162.50),
(30, '2025-07-06 08:00:00', 24, 97.30);



-- =========================================
-- INSERT DATA INTO WEATHER RECORD
-- =========================================

INSERT INTO WeatherRecord
(field_id, temperature, humidity, rainfall, record_date)
VALUES

(1, 31.50, 65.20, 12.40, '2025-07-01 09:00:00'),
(2, 32.10, 60.50, 8.30, '2025-07-01 10:00:00'),
(3, 33.20, 58.40, 5.10, '2025-07-01 11:00:00'),
(4, 30.80, 67.90, 15.60, '2025-07-01 12:00:00'),
(5, 34.00, 55.30, 3.20, '2025-07-01 01:00:00'),

(6, 31.90, 64.10, 11.70, '2025-07-02 09:00:00'),
(7, 32.50, 59.80, 7.50, '2025-07-02 10:00:00'),
(8, 33.60, 57.90, 4.80, '2025-07-02 11:00:00'),
(9, 30.40, 68.30, 16.20, '2025-07-02 12:00:00'),
(10, 34.20, 54.70, 2.90, '2025-07-02 01:00:00'),

(11, 31.70, 63.40, 10.90, '2025-07-03 09:00:00'),
(12, 32.80, 61.10, 9.00, '2025-07-03 10:00:00'),
(13, 33.40, 56.80, 4.20, '2025-07-03 11:00:00'),
(14, 30.60, 69.20, 17.10, '2025-07-03 12:00:00'),
(15, 34.50, 53.90, 3.50, '2025-07-03 01:00:00'),

(16, 31.30, 65.90, 12.80, '2025-07-04 09:00:00'),
(17, 32.00, 60.70, 8.10, '2025-07-04 10:00:00'),
(18, 33.80, 57.10, 5.60, '2025-07-04 11:00:00'),
(19, 30.20, 70.00, 18.40, '2025-07-04 12:00:00'),
(20, 34.70, 52.80, 2.40, '2025-07-04 01:00:00'),

(21, 31.80, 64.50, 11.20, '2025-07-05 09:00:00'),
(22, 32.40, 59.20, 7.80, '2025-07-05 10:00:00'),
(23, 33.10, 58.00, 4.60, '2025-07-05 11:00:00'),
(24, 30.90, 67.50, 15.90, '2025-07-05 12:00:00'),
(25, 34.10, 55.10, 3.10, '2025-07-05 01:00:00'),

(26, 31.60, 63.80, 10.50, '2025-07-06 09:00:00'),
(27, 32.70, 60.00, 8.70, '2025-07-06 10:00:00'),
(28, 33.50, 56.50, 5.00, '2025-07-06 11:00:00'),
(29, 30.50, 68.80, 16.80, '2025-07-06 12:00:00'),
(30, 34.30, 54.20, 2.70, '2025-07-06 01:00:00');