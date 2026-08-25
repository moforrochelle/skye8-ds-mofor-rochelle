# SKYE8 Health No-Show Prediction

This project analyses healthcare appointment attendance patterns and focuses on predicting healthcare appointment no-shows.

## Project Goals

* Load and validate healthcare appointment data
* Build a PostgreSQL database with appropriate keys and constraints
* Answer operational questions using SQL
* Analyse appointment attendance and no-show patterns
* Build and compare classification models
* Select a prediction threshold using operational costs
* Test the loading, feature-building, and threshold functions

## Development Setup

Create and activate a Python virtual environment before installing the project dependencies.

Install the required packages with:

```bash
pip install -r requirements.txt
```

The project uses PostgreSQL installed locally through Postgres.app during development.

Database connection details are supplied through environment variables and are not stored in the repository.

## Running the Project

After creating the PostgreSQL database and setting the required environment variables, build the database schema using `sql/schema.sql`.

Load the source data with:

```bash
python -m src.load
```

To run the automated tests:

```bash
python -m pytest
```

## Security and Data Handling

Raw project data is stored in `data/` and excluded from version control.

Database credentials and connection details must never be hard-coded in source code or committed to the repository. They are supplied through environment variables.

The `.env` file, raw data, virtual environment, and other local files are excluded through `.gitignore`.

## Project Structure

```text
data/              Raw project data, excluded from version control
src/               Reusable Python source code
sql/               PostgreSQL schema and analytical queries
notebooks/         Jupyter notebooks for analysis and modelling
tests/             Automated tests
reports/           Project documentation and findings
README.md          Project documentation
requirements.txt   Python dependencies
.gitignore         Files excluded from version control
```

## Database

The project uses PostgreSQL for the database stage.

The database schema is defined in `sql/schema.sql`. The SQL exercises and analytical queries are stored in `sql/exercises.sql` and `sql/analytics.sql`.

The data-loading pipeline handles inconsistent date formats, distances containing units, different boolean representations, duplicated identifiers, and appointments referencing patients absent from the patient register. The load process is designed to be idempotent.

The final verified database contains:

* 16 facilities
* 9,000 patients
* 37,793 appointments
* 0 orphan appointments
* 0 orphan facility references

The loading decisions and data-quality handling are documented in `reports/load_decisions.md` and `reports/data_quality.md`.

## SQL Analysis

The project contains 25 SQL exercises covering filtering, grouping, joins, subqueries, set operations, and NULL behaviour in aggregates.

The analytical queries in `sql/analytics.sql` include:

* Monthly no-show rate per facility
* Seven-day moving average of daily attendance
* Top three services by no-show rate within each facility type using a window function
* Attendance by months since patient registration
* A nested-subquery analysis rewritten using CTEs

An index-performance investigation was also completed. The tested query changed from a sequential scan to an index-assisted bitmap scan after the `facility_id` index was added. Full EXPLAIN ANALYZE evidence and discussion are documented in `reports/index_performance.md`.

## Feature Engineering

The modelling table was constructed using validated merges and only features available at the moment of booking.

Features include:

* Lead days
* Distance
* Reminder sent
* Prior no-shows
* Service
* Facility
* Day of week
* Month of year

The modelling table was reduced from **35.1 MB to 11.9 MB**, representing a **66.09% reduction** in memory usage and exceeding the required 50% reduction.

The feature-building process is implemented in `src/features.py` and documented in the classification notebook.

## Classification

Four classifiers were evaluated for appointment no-show prediction:

* Logistic Regression
* Decision Tree
* K-Nearest Neighbours
* Naive Bayes

A majority-class baseline was also considered to demonstrate why accuracy alone is misleading for this imbalanced classification problem.

Model performance was evaluated using:

* Accuracy
* Precision
* Recall
* F1 score
* Precision-Recall AUC

Logistic Regression achieved the highest PR-AUC among the models tested and was selected for threshold optimisation. Precision-Recall was given particular emphasis because it provides a more informative view of classifier performance when the positive class is imbalanced (Saito & Rehmsmeier, 2015).

ROC and Precision-Recall curves were evaluated, with Precision-Recall providing the more useful view for the district because non-attendance is the minority class.

Probability calibration was also evaluated using Platt scaling, following the probability-calibration methods discussed by Niculescu-Mizil and Caruana (2005).

## Threshold Recommendation

The classification threshold was selected using the project's operational cost assumptions rather than the default threshold of 0.5.

**Recommended threshold: 0.11, implying approximately 59 reminder calls per week under the project's cost assumptions.**

Detailed classification results, threshold calculations, calibration findings, and the cost arithmetic supporting this recommendation are available in `reports/classification_findings.md`.

## Testing

The project contains automated tests covering the loading, feature-building, and threshold functions.

The test suite currently contains **16 tests**, all of which pass.

Run the tests with:

```bash
python -m pytest
```

The loading pipeline is idempotent: running it twice does not change the verified database row counts.

## Reports

The `reports/` directory contains:

* `load_decisions.md` — decisions made during data loading
* `data_quality.md` — source-data inconsistencies and cleaning decisions
* `index_performance.md` — EXPLAIN ANALYZE evidence and index-performance analysis
* `classification_findings.md` — model comparison, calibration, threshold optimisation, and recommendation
* `conflict-note.md` — documentation of the deliberate Git merge conflict and its resolution

## References

* Saito, T. & Rehmsmeier, M. (2015). *The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets*. PLOS ONE, 10(3), e0118432. https://doi.org/10.1371/journal.pone.0118432
* Niculescu-Mizil, A. & Caruana, R. (2005). *Predicting Good Probabilities With Supervised Learning*. Proceedings of the 22nd International Conference on Machine Learning, 625–632.
* PostgreSQL Global Development Group. *PostgreSQL Documentation*. https://www.postgresql.org/docs/current/
