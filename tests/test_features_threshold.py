import numpy as np
import pandas as pd

from src.features import build_feature_table
from src.threshold import find_cost_optimal_threshold


def make_test_data():
    appointments = pd.DataFrame({
        "appointment_id": ["A1", "A2", "A3"],
        "patient_id": ["P1", "P1", "P2"],
        "facility_id": ["F1", "F1", "F2"],
        "service": ["General", "Dental", "General"],
        "booked_ts": [
            "2025-01-01 08:00:00",
            "2025-01-02 08:00:00",
            "2025-01-03 08:00:00",
        ],
        "scheduled_ts": [
            "2025-01-08 08:00:00",
            "2025-01-09 08:00:00",
            "2025-01-10 08:00:00",
        ],
        "lead_days": [7, 7, 7],
        "reminder_sent": [0, 1, 0],
        "prior_no_shows": [0, 1, 0],
        "attended": [1, 0, 1],
    })

    patients = pd.DataFrame({
        "patient_id": ["P1", "P2"],
        "facility_id": ["F1", "F2"],
        "sex": ["F", "M"],
        "age_band": ["25-34", "35-44"],
        "registered_on": ["2024-01-01", "2024-02-01"],
        "distance_km": [5.0, 10.0],
        "has_phone": [True, True],
        "transport_mode": ["walk", "car"],
    })

    facilities = pd.DataFrame({
        "facility_id": ["F1", "F2"],
        "facility_name": ["Facility 1", "Facility 2"],
        "town": ["Town 1", "Town 2"],
        "facility_type": ["Hospital", "Clinic"],
        "catchment_population": [10000, 20000],
    })

    return appointments, patients, facilities


def test_feature_table_keeps_all_appointments():
    appointments, patients, facilities = make_test_data()

    result = build_feature_table(
        appointments,
        patients,
        facilities,
    )

    assert len(result) == len(appointments)


def test_feature_table_has_expected_columns():
    appointments, patients, facilities = make_test_data()

    result = build_feature_table(
        appointments,
        patients,
        facilities,
    )

    assert "distance_km" in result.columns
    assert "service" in result.columns
    assert "facility_type" in result.columns


def test_feature_table_creates_day_of_week():
    appointments, patients, facilities = make_test_data()

    result = build_feature_table(
        appointments,
        patients,
        facilities,
    )

    assert "day_of_week" in result.columns
    assert result["day_of_week"].notna().all()


def test_feature_table_creates_month_of_year():
    appointments, patients, facilities = make_test_data()

    result = build_feature_table(
        appointments,
        patients,
        facilities,
    )

    assert "month_of_year" in result.columns
    assert result["month_of_year"].tolist() == [8, 9, 10]


def test_feature_table_has_one_row_per_appointment():
    appointments, patients, facilities = make_test_data()

    result = build_feature_table(
        appointments,
        patients,
        facilities,
    )

    assert result["appointment_id"].nunique() == len(appointments)


def test_threshold_returns_one_percent_steps():
    y_true = np.array([0, 0, 1, 1])
    probabilities = np.array([0.1, 0.2, 0.8, 0.9])

    best, results = find_cost_optimal_threshold(
        y_true,
        probabilities,
    )

    assert results["threshold"].iloc[0] == 0.01
    assert results["threshold"].iloc[-1] == 0.99


def test_threshold_calculates_cost_correctly():
    y_true = np.array([0, 1])
    probabilities = np.array([0.9, 0.1])

    best, results = find_cost_optimal_threshold(
        y_true,
        probabilities,
        false_positive_cost=500,
        false_negative_cost=5000,
    )

    assert results["total_cost_xaf"].min() == 500


def test_threshold_returns_required_columns():
    y_true = np.array([0, 1, 1, 0])
    probabilities = np.array([0.1, 0.7, 0.8, 0.2])

    best, results = find_cost_optimal_threshold(
        y_true,
        probabilities,
    )

    required = {
        "threshold",
        "false_positives",
        "false_negatives",
        "true_positives",
        "true_negatives",
        "total_cost_xaf",
    }

    assert required.issubset(results.columns)


def test_threshold_best_value_is_in_results():
    y_true = np.array([0, 1, 1, 0])
    probabilities = np.array([0.1, 0.7, 0.8, 0.2])

    best, results = find_cost_optimal_threshold(
        y_true,
        probabilities,
    )

    assert best["threshold"] in results["threshold"].values


def test_threshold_changes_when_false_negative_is_more_expensive():
    y_true = np.array([0, 0, 1, 1])
    probabilities = np.array([0.2, 0.3, 0.4, 0.5])

    best_low_cost, _ = find_cost_optimal_threshold(
        y_true,
        probabilities,
        false_positive_cost=500,
        false_negative_cost=500,
    )

    best_high_cost, _ = find_cost_optimal_threshold(
        y_true,
        probabilities,
        false_positive_cost=500,
        false_negative_cost=5000,
    )

    assert (
         best_high_cost["threshold"]
         <= best_low_cost["threshold"]
    )