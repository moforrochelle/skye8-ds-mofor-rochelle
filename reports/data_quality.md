# Data Quality

## Overview

The project data contains several inconsistencies that the loading pipeline must handle before the records can be stored reliably in PostgreSQL. The cleaning process is applied during loading so that the database receives consistent values while preserving the required constraints.

## Duplicate Identifiers

The patients dataset contains duplicate `patient_id` values. The loader keeps the first occurrence of each patient identifier and discards subsequent duplicates.

The appointments dataset also contains duplicate `appointment_id` values. The loader keeps the first occurrence of each appointment identifier.

This ensures that the primary key constraints remain valid and that repeated records are not loaded into the database.

## Date and Timestamp Formats

The source data contains more than one date representation.

Patient registration dates are accepted in:

- `DD/MM/YYYY`
- `YYYY-MM-DD`

Appointment timestamps are accepted in the supported source formats:

- `YYYY-MM-DD HH:MM:SS`
- `DD/MM/YYYY HH:MM`

The loader converts these values into Python date or datetime objects before inserting them into PostgreSQL.

## Distance Values

Some distance values contain the `km` unit rather than being stored as a plain numeric value.

The loader removes the `km` text, trims surrounding whitespace, and converts the remaining value to a numeric value before insertion.

## Boolean Values

Boolean fields can arrive in different representations, including:

- `TRUE`
- `True`
- `1`
- `yes`
- `FALSE`
- `False`
- `0`
- `no`

The loader normalises these representations into Python boolean values before they are inserted into PostgreSQL boolean columns.

## Other Numeric Values

Values such as `lead_days` may contain text such as `day` or `days`. The loader removes these units and converts the resulting value to an integer.

## Missing Patient References

Some appointment records reference patients who are not present in the patient register.

These appointments are excluded from the database load rather than creating artificial patient records. This allows the foreign key from appointments to patients to remain valid.

## Idempotency

The loader uses conflict handling when inserting records. It was executed twice against the database and the row counts remained unchanged after the second execution.

The final verification counts were:

- Facilities: 16
- Patients: 9,000
- Appointments: 37,793

No orphan appointments or orphan facility references remained after loading.

## Summary

The data-loading pipeline therefore addresses the main quality issues present in the source data while preserving primary-key and foreign-key constraints. The cleaned data is prepared for reliable storage in PostgreSQL and for the subsequent SQL analysis and classification stages.

