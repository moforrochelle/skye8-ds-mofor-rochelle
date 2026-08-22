-- Question 1: How many patients are registered?
SELECT COUNT(*) AS patient_count
FROM patients;


-- Question 2: How many patients are female?
SELECT COUNT(*) AS female_patients
FROM patients
WHERE LOWER(sex) IN ('f', 'female');


-- Question 3: How many female patients are aged 45–59?
SELECT COUNT(*) AS female_45_59
FROM patients
WHERE LOWER(sex) IN ('f', 'female')
  AND age_band = '45-59';


-- Question 4: How many patients are either aged 0–4 or 60+?
SELECT COUNT(*) AS patients_0_4_or_60_plus
FROM patients
WHERE age_band = '0-4'
   OR age_band = '60+';


-- Question 5: How many patients live more than 10 km from their facility?
SELECT COUNT(*) AS patients_over_10km
FROM patients
WHERE distance_km > 10;


-- Question 6: How many patients have a phone?
SELECT COUNT(*) AS patients_with_phone
FROM patients
WHERE has_phone = TRUE;


-- Question 7: How many appointments were booked at least 14 days before the scheduled date?
SELECT COUNT(*) AS appointments_with_long_lead
FROM appointments
WHERE lead_days >= 14;


-- Question 8: How many appointments did not receive a reminder?
SELECT COUNT(*) AS appointments_without_reminder
FROM appointments
WHERE reminder_sent = FALSE;


-- Question 9: How many patients are registered at each facility?
SELECT facility_id, COUNT(*) AS patient_count
FROM patients
GROUP BY facility_id
ORDER BY patient_count DESC;


-- Question 10: What is the average distance travelled by patients for each transport mode?
SELECT transport_mode, AVG(distance_km) AS average_distance_km
FROM patients
GROUP BY transport_mode
ORDER BY average_distance_km DESC;


-- Question 11: How many appointments are recorded for each service?
SELECT service, COUNT(*) AS appointment_count
FROM appointments
GROUP BY service
ORDER BY appointment_count DESC;


-- Question 12: Which facilities have more than 500 registered patients?
SELECT facility_id, COUNT(*) AS patient_count
FROM patients
GROUP BY facility_id
HAVING COUNT(*) > 500
ORDER BY patient_count DESC;


-- Question 13: What is the average number of prior no-shows for each service?
SELECT service, AVG(prior_no_shows) AS average_prior_no_shows
FROM appointments
GROUP BY service
ORDER BY average_prior_no_shows DESC;


-- Question 14: Which appointments have matching patient records?
SELECT a.appointment_id, a.patient_id, p.age_band
FROM appointments AS a
INNER JOIN patients AS p
    ON a.patient_id = p.patient_id;


-- Question 15: Show every patient and their appointment count, including patients with no appointments.
SELECT
    p.patient_id,
    COUNT(a.appointment_id) AS appointment_count
FROM patients AS p
LEFT JOIN appointments AS a
    ON p.patient_id = a.patient_id
GROUP BY p.patient_id
ORDER BY appointment_count DESC;


-- Question 16: Show every facility and its appointment count using a RIGHT JOIN.
SELECT
    f.facility_id,
    f.facility_name,
    COUNT(a.appointment_id) AS appointment_count
FROM appointments AS a
RIGHT JOIN facilities AS f
    ON a.facility_id = f.facility_id
GROUP BY f.facility_id, f.facility_name
ORDER BY appointment_count DESC;


-- Question 17: Show all facilities and all patients, including records that do not match.
SELECT
    f.facility_id AS facility_from_facilities,
    p.facility_id AS facility_from_patients,
    f.facility_name,
    p.patient_id
FROM facilities AS f
FULL OUTER JOIN patients AS p
    ON f.facility_id = p.facility_id;


-- Question 18: Find patients who have at least one appointment using a subquery.
SELECT patient_id
FROM patients
WHERE patient_id IN (
    SELECT patient_id
    FROM appointments
);


-- Question 19: Find facilities whose patient count is above the average patient count across facilities.
SELECT facility_id, patient_count
FROM (
    SELECT facility_id, COUNT(*) AS patient_count
    FROM patients
    GROUP BY facility_id
) AS facility_counts
WHERE patient_count > (
    SELECT AVG(patient_count)
    FROM (
        SELECT facility_id, COUNT(*) AS patient_count
        FROM patients
        GROUP BY facility_id
    ) AS counts
);


-- Question 20: Return all facility IDs that appear in either the patients or appointments tables.
SELECT facility_id
FROM patients
UNION
SELECT facility_id
FROM appointments;


-- Question 21: Return facility IDs that appear in both the patients and appointments tables.
SELECT facility_id
FROM patients
INTERSECT
SELECT facility_id
FROM appointments;


-- Question 22: Return facility IDs that have patients but no appointments.
SELECT facility_id
FROM patients
EXCEPT
SELECT facility_id
FROM appointments;


-- Question 23: Compare COUNT(*) with COUNT(distance_km) to show how NULL values affect aggregates.
SELECT
    COUNT(*) AS total_patients,
    COUNT(distance_km) AS patients_with_distance,
    COUNT(*) - COUNT(distance_km) AS patients_missing_distance
FROM patients;


-- Question 24: Calculate the attendance rate and no-show rate for each facility.
SELECT
    facility_id,
    COUNT(*) AS total_appointments,
    SUM(CASE WHEN attended = TRUE THEN 1 ELSE 0 END) AS attended_count,
    SUM(CASE WHEN attended = FALSE THEN 1 ELSE 0 END) AS no_show_count,
    AVG(CASE WHEN attended = TRUE THEN 1.0 ELSE 0.0 END) AS attendance_rate,
    AVG(CASE WHEN attended = FALSE THEN 1.0 ELSE 0.0 END) AS no_show_rate
FROM appointments
GROUP BY facility_id
ORDER BY no_show_rate DESC;


-- Question 25: Find the services with the highest number of no-shows within each facility.
SELECT facility_id, service, no_show_count
FROM (
    SELECT
        facility_id,
        service,
        SUM(CASE WHEN attended = FALSE THEN 1 ELSE 0 END) AS no_show_count,
        RANK() OVER (
            PARTITION BY facility_id
            ORDER BY SUM(CASE WHEN attended = FALSE THEN 1 ELSE 0 END) DESC
        ) AS service_rank
    FROM appointments
    GROUP BY facility_id, service
) AS ranked_services
WHERE service_rank = 1
ORDER BY facility_id;