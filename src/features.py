import pandas as pd


def build_feature_table(appointments, patients, facilities):
    patients_model = patients.drop_duplicates(
        subset="patient_id",
        keep="first",
    ).copy()

    model = appointments.merge(
        patients_model,
        on="patient_id",
        how="left",
        validate="many_to_one",
        suffixes=("", "_patient"),
    )

    if "facility_id_patient" in model.columns:
        model = model.drop(columns="facility_id_patient")

    model = model.merge(
        facilities,
        on="facility_id",
        how="left",
        validate="many_to_one",
    )

    model["booked_ts"] = pd.to_datetime(
        model["booked_ts"],
        errors="coerce",
    )

    model["scheduled_ts"] = pd.to_datetime(
        model["scheduled_ts"],
        format="mixed",
        dayfirst=True,
        errors="coerce",
    )

    model["day_of_week"] = model["scheduled_ts"].dt.dayofweek
    model["month_of_year"] = model["scheduled_ts"].dt.month

    return model