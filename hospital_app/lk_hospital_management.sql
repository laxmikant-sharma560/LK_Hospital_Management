CREATE DATABASE IF NOT EXISTS lk_hospital_db;
USE lk_hospital_db;

-- Appointments Table
CREATE TABLE IF NOT EXISTS appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(100),
    doctor_name VARCHAR(100),
    appointment_date DATE,
    symptoms TEXT
);

-- Patients Table
CREATE TABLE IF NOT EXISTS patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    address VARCHAR(255),
    contact VARCHAR(20),
    email VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Doctors Table
CREATE TABLE IF NOT EXISTS doctor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    specialty VARCHAR(100),
    gender VARCHAR(10),
    contact VARCHAR(20),
    email VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Billing Table
CREATE TABLE IF NOT EXISTS billing (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    amount DECIMAL(10, 2) NOT NULL,
    description VARCHAR(255),
    date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'unpaid',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    -- , FOREIGN KEY (patient_id) REFERENCES patients(id)
);

-- Only run these IF the column is missing!
ALTER TABLE doctors ADD COLUMN gender VARCHAR(10) AFTER specialty;
-- ALTER TABLE patients ADD COLUMN contact VARCHAR(20);
-- ALTER TABLE doctors ADD COLUMN contact VARCHAR(20);