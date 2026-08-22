import pandas as pd
from src.load import get_connection


patients = pd.read_csv("data/raw/patients.csv")

conn = get_connection()
cursor = conn.cursor()


# 1. Total number of patients
patients = patients.drop_duplicates(subset="patient_id")
pandas_total = len(patients)

cursor.execute("SELECT COUNT(*) FROM patients")
sql_total = cursor.fetchall()[0][0]


# 2. Number of female patients
pandas_female = patients["sex"].str.lower().isin(["f", "female"]).sum()

cursor.execute("""
    SELECT COUNT(*)
    FROM patients
    WHERE LOWER(sex) IN ('f', 'female')
""")
sql_female = cursor.fetchall()[0][0]


# 3. Number of patients more than 10 km away
pandas_over_10km = (
    pd.to_numeric(
        patients["distance_km"].astype(str).str.replace("km", "", regex=False).str.strip(),
        errors="coerce",
    ) > 10
).sum()

cursor.execute("""
    SELECT COUNT(*)
    FROM patients
    WHERE distance_km > 10
""")
sql_over_10km = cursor.fetchall()[0][0]


cursor.close()
conn.close()


# Compare SQL and pandas results
comparison = pd.DataFrame({
    "aggregate": [
        "patient_count",
        "female_patients",
        "patients_over_10km",
    ],
    "sql": [
        sql_total,
        sql_female,
        sql_over_10km,
    ],
    "pandas": [
        pandas_total,
        pandas_female,
        pandas_over_10km,
    ],
})

comparison["difference"] = comparison["sql"] - comparison["pandas"]

print(comparison)