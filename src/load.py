import os
from datetime import datetime
import psycopg2
import pandas as pd

def get_connection():
    return psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
        dbname=os.getenv("PGDATABASE", "skye8_health"),
        user=os.getenv("PGUSER"),
    )


def clean_boolean(value):
        if value is None:
            return None

        value = str(value).strip().lower()

        if value in {"true", "1", "yes"}:
           return True

        if value in {"false", "0", "no"}:
           return False

        return None


def clean_distance(value):
    if value is None:
        return None

    value = str(value).strip().lower().replace("km", "").strip()

    if value == "":
        return None

    return float(value)

def clean_integer(value):
    if value is None:
        return None

    value = str(value).strip().lower()

    if value == "" or value == "nan":
        return None

    value = value.replace("days", "").replace("day", "").strip()

    return int(float(value))


def clean_date(value):
    if value is None:
        return None

    value = str(value).strip()

    if value == "":
        return None

    for date_format in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, date_format).date()
        except ValueError:
            continue

    raise ValueError(f"Unrecognized date format: {value}")


def clean_timestamp(value):
    if value is None:
        return None

    value = str(value).strip()

    if value == "" or value.lower() == "nan":
        return None

    if value.isdigit():
        return datetime.fromtimestamp(int(value))

    for timestamp_format in (
        "%Y-%m-%d %H:%M:%S",
        "%d/%m/%Y %H:%M",
    ):
        try:
            return datetime.strptime(value, timestamp_format)
        except ValueError:
            continue

    raise ValueError(f"Unrecognized timestamp format: {value}")



def load_facilities(conn):
    facilities = pd.read_csv("data/raw/facilities.csv")

    with conn.cursor() as cursor:
        for row in facilities.itertuples(index=False):
            cursor.execute(
                """
                INSERT INTO facilities (
                    facility_id,
                    facility_name,
                    town,
                    facility_type,
                    catchment_population
                )
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (facility_id) DO NOTHING
                """,
                (
                    row.facility_id,
                    row.facility_name,
                    row.town,
                    row.facility_type,
                    row.catchment_population,
                ),
            )

    conn.commit()


def load_patients(conn):
    patients = pd.read_csv("data/raw/patients.csv")

    # Keep the first occurrence of each patient ID.
    patients = patients.drop_duplicates(subset="patient_id", keep="first")

    with conn.cursor() as cursor:
        for row in patients.itertuples(index=False):
            cursor.execute(
                """
                INSERT INTO patients (
                    patient_id,
                    facility_id,
                    sex,
                    age_band,
                    registered_on,
                    distance_km,
                    has_phone,
                    transport_mode
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (patient_id) DO NOTHING
                """,
                (
                    row.patient_id,
                    row.facility_id,
                    row.sex,
                    row.age_band if pd.notna(row.age_band) else None,
                    clean_date(row.registered_on),
                    clean_distance(row.distance_km),
                    clean_boolean(row.has_phone),
                    row.transport_mode if pd.notna(row.transport_mode) else None,
                ),
            )

    conn.commit()  


def load_appointments(conn):
    appointments = pd.read_csv(
    "data/raw/appointments.csv",
    dtype=str,
)

    # Keep the first occurrence of each appointment ID.
    appointments = appointments.drop_duplicates(
        subset="appointment_id",
        keep="first",
    )

    # Keep only appointments whose patient exists in the patient table.
    with conn.cursor() as cursor:
       cursor.execute("SELECT patient_id FROM patients")
       valid_patient_ids = {row[0] for row in cursor.fetchall()}

    appointments = appointments[
    appointments["patient_id"].isin(valid_patient_ids)
]

    with conn.cursor() as cursor:
        for row in appointments.itertuples(index=False):
            cursor.execute(
                """
                INSERT INTO appointments (
                    appointment_id,
                    patient_id,
                    facility_id,
                    service,
                    booked_ts,
                    scheduled_ts,
                    lead_days,
                    reminder_sent,
                    prior_no_shows,
                    attended
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (appointment_id) DO NOTHING
                """,
                (
                    row.appointment_id,
                    row.patient_id,
                    row.facility_id,
                    row.service,
                    clean_timestamp(row.booked_ts),
                    clean_timestamp(row.scheduled_ts),
                    clean_integer(row.lead_days),
                    clean_boolean(row.reminder_sent),
                    clean_integer(row.prior_no_shows),
                    clean_boolean(row.attended),
                ),
            )

    conn.commit() 


def main():
    conn = get_connection()

    try:
        load_facilities(conn)
        load_patients(conn)
        load_appointments(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()     