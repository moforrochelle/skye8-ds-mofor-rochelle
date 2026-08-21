CREATE TABLE facilities(
    facility_id VARCHAR(10) PRIMARY KEY,
    facility_name VARCHAR(150) NOT NULL,
    town VARCHAR(100) NOT NULL,
    facility_type VARCHAR(50) NOT NULL,
    catchment_population INTEGER NOT NULL CHECK (catchment_population >=0)
);

CREATE TABLE patients(
    patient_id VARCHAR(12) PRIMARY KEY,
    facility_id VARCHAR(10) NOT NULL,
    sex VARCHAR(10) NOT NULL,
    age_band VARCHAR(10),
    registered_on DATE NOT NULL,
    distance_km NUMERIC(6,2),
    has_phone BOOLEAN NOT NULL,
    transport_mode VARCHAR(30),
    CONSTRAINT fk_patients_facility
        FOREIGN KEY (facility_id)
        REFERENCES facilities(facility_id)
);

CREATE TABLE appointments (
    appointment_id VARCHAR(12) PRIMARY KEY,
    patient_id VARCHAR(12) NOT NULL,
    facility_id VARCHAR(10) NOT NULL,
    service VARCHAR(100) NOT NULL,
    booked_ts TIMESTAMP NOT NULL,
    scheduled_ts TIMESTAMP NOT NULL,
    lead_days INTEGER NOT NULL CHECK (lead_days >= 0),
    reminder_sent BOOLEAN NOT NULL,
    prior_no_shows INTEGER NOT NULL CHECK (prior_no_shows >= 0),
    attended BOOLEAN NOT NULL,
    CONSTRAINT fk_appointments_patient
        FOREIGN KEY (patient_id)
        REFERENCES patients(patient_id),
    CONSTRAINT fk_appointments_facility
        FOREIGN KEY (facility_id)
        REFERENCES facilities (facility_id)
    );