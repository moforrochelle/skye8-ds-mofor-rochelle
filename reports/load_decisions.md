# Data Loading Decisions

## Duplicate patient identifiers

The patients dataset contains duplicate `patient_id` values. The loader will keep the first occurrence of each patient identifier and discard subsequent duplicate rows.

This ensures that each patient identifier maps to exactly one patient record and allows the patient primary key constraint to hold.

## Duplicate appointment identifiers

The appointments dataset contains duplicate `appointment_id` values. The loader will keep the first occurrence of each appointment identifier and discard subsequent duplicate rows.

This ensures that each appointment identifier is unique and satisfies the appointment primary key constraint.

## Appointments with missing patients

Some appointments reference patient identifiers that are absent from the patient register. These appointments will be excluded from the database load rather than creating artificial patient records or weakening the foreign key constraint.

This decision preserves referential integrity because every loaded appointment must reference an existing patient.

The number of excluded appointments will be recorded during the loading process.


## Load verification

The PostgreSQL database was loaded from the three raw CSV files.

The loader was executed twice to verify idempotency. The row counts remained unchanged after the second execution, confirming that records were not duplicated.

The database also passed referential-integrity checks: loaded appointments did not contain patient IDs or facility IDs that were absent from their referenced tables.

The final row counts from the verification run are
:

- Facilities: 16
- Patients: 9000
- Appointments: 37793
- Orphan appointments: 0
- Orphan facilities: 0