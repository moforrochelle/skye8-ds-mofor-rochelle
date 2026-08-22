-- Query 1: What is the monthly no-show rate for each facility?
SELECT
    facility_id,
    DATE_TRUNC('month', scheduled_ts) AS month,
    COUNT(*) AS total_appointments,
    SUM(CASE WHEN attended = FALSE THEN 1 ELSE 0 END) AS no_shows,
    ROUND(
        100.0 * SUM(CASE WHEN attended = FALSE THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS no_show_rate
FROM appointments
GROUP BY facility_id, DATE_TRUNC('month', scheduled_ts)
ORDER BY facility_id, month;


-- Query 2: What is the 7-day moving average of daily attendance?
WITH daily_attendance AS (
    SELECT
        DATE(scheduled_ts) AS attendance_date,
        AVG(
            CASE
                WHEN attended = TRUE THEN 1.0
                ELSE 0.0
            END
        ) AS daily_attendance_rate
    FROM appointments
    GROUP BY DATE(scheduled_ts)
)
SELECT
    attendance_date,
    daily_attendance_rate,
    AVG(daily_attendance_rate) OVER (
        ORDER BY attendance_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS seven_day_moving_average
FROM daily_attendance
ORDER BY attendance_date;


-- Query 3: What are the top three services by no-show rate within each facility type?
WITH service_rates AS (
    SELECT
        f.facility_type,
        a.service,
        COUNT(*) AS total_appointments,
        SUM(CASE WHEN a.attended = FALSE THEN 1 ELSE 0 END) AS no_shows,
        100.0 * SUM(CASE WHEN a.attended = FALSE THEN 1 ELSE 0 END)
            / COUNT(*) AS no_show_rate
    FROM appointments AS a
    INNER JOIN facilities AS f
        ON a.facility_id = f.facility_id
    GROUP BY f.facility_type, a.service
),
ranked_services AS (
    SELECT
        facility_type,
        service,
        total_appointments,
        no_shows,
        no_show_rate,
        RANK() OVER (
            PARTITION BY facility_type
            ORDER BY no_show_rate DESC
        ) AS service_rank
    FROM service_rates
)
SELECT
    facility_type,
    service,
    total_appointments,
    no_shows,
    ROUND(no_show_rate, 2) AS no_show_rate,
    service_rank
FROM ranked_services
WHERE service_rank <= 3
ORDER BY facility_type, service_rank;


-- Query 4: What is the attendance rate by months since patient registration?
WITH patient_appointments AS (
    SELECT
        p.patient_id,
        a.appointment_id,
        a.attended,
        (
            EXTRACT(
                YEAR FROM AGE(DATE(a.scheduled_ts), p.registered_on)
            ) * 12
            +
            EXTRACT(
                MONTH FROM AGE(DATE(a.scheduled_ts), p.registered_on)
            )
        )::INTEGER AS months_since_registration
    FROM patients AS p
    INNER JOIN appointments AS a
        ON p.patient_id = a.patient_id
)
SELECT
    months_since_registration,
    COUNT(*) AS total_appointments,
    SUM(CASE WHEN attended = TRUE THEN 1 ELSE 0 END) AS attended_count,
    ROUND(
        100.0 * SUM(CASE WHEN attended = TRUE THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS attendance_rate
FROM patient_appointments
WHERE months_since_registration >= 0
GROUP BY months_since_registration
ORDER BY months_since_registration;


-- Query 5A: Which facilities have a no-show rate above the overall average? Nested-subquery version.
SELECT
    facility_id,
    no_show_rate
FROM (
    SELECT
        facility_id,
        100.0 * SUM(CASE WHEN attended = FALSE THEN 1 ELSE 0 END)
            / COUNT(*) AS no_show_rate
    FROM appointments
    GROUP BY facility_id
) AS facility_rates
WHERE no_show_rate > (
    SELECT AVG(no_show_rate)
    FROM (
        SELECT
            facility_id,
            100.0 * SUM(CASE WHEN attended = FALSE THEN 1 ELSE 0 END)
                / COUNT(*) AS no_show_rate
        FROM appointments
        GROUP BY facility_id
    ) AS all_facility_rates
)
ORDER BY no_show_rate DESC;

-- Query 5B: The same analysis rewritten using CTEs.
WITH facility_rates AS (
    SELECT
        facility_id,
        100.0 * SUM(CASE WHEN attended = FALSE THEN 1 ELSE 0 END)
            / COUNT(*) AS no_show_rate
    FROM appointments
    GROUP BY facility_id
),
overall_rate AS (
    SELECT AVG(no_show_rate) AS average_no_show_rate
    FROM facility_rates
)
SELECT
    facility_rates.facility_id,
    facility_rates.no_show_rate
FROM facility_rates
CROSS JOIN overall_rate
WHERE facility_rates.no_show_rate > overall_rate.average_no_show_rate
ORDER BY facility_rates.no_show_rate DESC;
